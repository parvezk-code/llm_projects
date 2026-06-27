# Event Handler — Design Rules

App-specific rules for how event handlers are structured and how they orchestrate
an event across the state and UI layers. These refine the generic event-handler doc
with the **one-method-per-event** orchestration principle that pairs with the
state-controller and component-controller rules.

---

## Part A — Structure & Placement Rules

1. **Partitioned by emitting component.** Handlers live in a directory per emitting
   component, one handler file per event:

   ```
   desktop/event_handlers/
   ├── input_bar/     send_router_handler.py
   ├── toolbar/       clear_chat_handler.py, load_project_handler.py
   ├── folder_picker/ folder_selected_handler.py
   └── status_bar/    dismiss_handler.py
   ```

2. **One handler class per event** — with one exception: the **send router**, which
   holds `on_send` plus the per-mode methods (`on_send_plain`, `on_send_rag`,
   `on_send_agent`, …) because they are one cohesive routing unit that grows
   together across levels.

3. **Class names match files.** `ClearChatHandler`, `LoadProjectHandler`,
   `FolderSelectedHandler`, `DismissHandler`, `SendRouterHandler`.

4. **Method names are `on_<event>`.** `on_clear_clicked`, `on_folder_selected`,
   `on_send`, `on_dismissed`.

5. **Constructor injection only.** A handler receives the `ActionBundle` and the
   component controllers it needs as plain injected objects. It never imports the
   UI layer and never constructs controllers, actions, gateways, or state.

6. **Stored as instance attributes on the MainController.** Every handler is held as
   `self._<name>_handler` so it is not garbage-collected (which would silently kill
   its signal connection). The MainController, not the handler, binds signals to
   handler methods.

---

## Part B — Responsibility Rules

1. **The handler orchestrates one event across layers.** Its job is to sequence:
   read input → (guard) → call the Action → apply the result to the UI. It is the
   only layer that coordinates *across* components.

2. **May access only controllers and the ActionBundle.** A handler must not access
   Core, Gateways, or State directly. State/business changes go through Actions; UI
   changes go through component controllers.

3. **Unpack domain models to primitives.** Actions return domain models; the handler
   unpacks them (`msg.role`, `msg.content`, `index.project_path`) into primitives
   before calling any controller. The UI never sees a domain model.

4. **Route errors to the correct surface.** Chat/LLM failures → inline error bubble
   in the chat area. File/load failures → dismissible status-bar banner. The handler
   chooses the surface; the action only raises.

5. **Threading is a handler concern.** Slow actions run on a `Worker` thread; results
   and errors are delivered back on the main thread via the worker's `on_result` /
   `on_error` callbacks. Actions stay synchronous. The handler holds its `Worker`
   reference until it finishes.

6. **Handler-level guards live here, before the action.** Routing/UI-state guards
   (e.g. "RAG/Agent selected but no project loaded") are handler concerns and run
   before the action is called. On a failed guard, surface a status-bar message and
   do not call the action.

---

## Part C — Orchestration Rule (the one-method-per-event pairing)

This is the rule that pairs the handler with the event-shaped methods on the state
controller and the component controllers.

1. **Call one method per layer-object per event — never a sequence of fine-grained
   setters.** The handler does not issue widget-level or field-level calls. It calls:
   - **one Action** (which internally calls **one** event-shaped StateController
     method), and
   - **one event-shaped method per component controller** involved in the event.

2. **The handler is the only orchestrator.** Component controllers group *their own*
   component's work for an event; the StateController groups the state writes for an
   event; the **handler** is what calls each of them once, in order. Fan-out across
   components is the handler's job and only the handler's job.

3. **Shape: action first, then UI.** Apply the state change via the action, then
   apply the matching UI reset/update via one event-shaped method on each affected
   controller.

   **Example — the clear-chat event (synchronous):**

   ```python
   def on_clear_clicked(self) -> None:
       self._actions.clear_chat.execute()        # → state.reset_on_clear_chat()
       self._chat_area.reset_on_clear_chat()
       self._status_bar.reset_on_clear_chat()
       self._input_bar.reset_on_clear_chat()
       self._toolbar.reset_on_clear_chat()
   ```

   The handler reads as a flat list of "reset every layer for this event" — one call
   per layer-object, no widget or field detail visible.

   **Example — the send event (threaded, result + error split):**

   ```python
   def on_send_plain(self) -> None:
       user_text = self._input_bar.get_text()
       if not user_text:
           return
       self._status_bar.hide()
       self._set_busy(True)                       # busy gate (see C.6)
       self._worker = Worker(
           method=lambda: self._actions.send_plain.execute(user_text),
           on_result=self._on_result,
           on_error=self._on_error,
       )
       self._worker.start()

   def _on_result(self, result) -> None:
       user_msg, assistant_msg = result           # unpack domain model to primitives
       self._chat_area.reset_on_send_result(
           user_msg.role, user_msg.content,
           assistant_msg.role, assistant_msg.content,
       )
       self._input_bar.reset_on_send_cleared()
       self._set_busy(False)

   def _on_error(self, error: Exception) -> None:
       self._chat_area.reset_on_send_error(str(error))
       self._set_busy(False)
   ```

   The "apply result to UI" half moves into the callbacks, but it is still
   **one event-shaped method per controller** — not fine-grained setters.

4. **The `_on_<event>` suffix unifies all layers; the verb prefix reflects what each
   layer does.** Methods for one event share the `_on_<event>` tail across the
   Action, StateController, and component controllers — so the event is traceable
   end-to-end by one name. The verb prefix may differ where a layer's operation is
   semantically distinct:

   - `reset_on_clear_chat` — a reset; all layers use the same full name.
   - `add_message_on_send` (StateController), `reset_on_send_result` (chat_area),
     `reset_on_send_cleared` (input_bar) — the send event adds to state and resets
     UI; the prefix reflects each layer's own concept, not a single shared verb.

   When an event is purely a reset at every layer, the full name is identical
   everywhere. When layers do different things for the same event, only the suffix
   is guaranteed to align.

5. **Threaded events follow the same shape, split across callbacks.** Busy toggling
   wraps the operation; the semantic UI update is still one event-method per
   controller in `_on_result` / `_on_error`:

   ```python
   def _on_result(self, index) -> None:
       self._set_busy(False)                                          # busy gate off
       self._toolbar.reset_on_project_loaded(                        # one call per controller
           os.path.basename(index.project_path)
       )
       self._chat_area.reset_on_project_loaded()
   ```

6. **Busy toggling is the allowed fine-grained exception.** Enable/disable during a
   threaded run (`_set_busy` → `set_enabled(False/True)`) is a cross-cutting
   UI-state toggle, not an event reset, and stays as direct `set_enabled` calls in
   a private helper. The event-shaped rule applies to the event's *semantic* updates,
   not the busy gate.

---

## Why this split

- **Handlers** become thin, readable orchestrators: read input, guard, call one
  action, call one event-method per controller. No widget or field detail leaks in.
- The handler is the **single place** that knows *which* layers an event touches;
  each controller/state method is the single place that knows *what* its own layer
  does for that event.
- The `_on_<event>` suffix runs through the action, the StateController, and every
  component controller — so an entire event is traceable end-to-end by suffix, and
  each layer owns exactly its own slice.