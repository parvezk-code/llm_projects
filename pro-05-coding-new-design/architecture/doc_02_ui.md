# UI Component & Component Controller — Design Rules

App-specific rules for how UI components and their controllers are structured,
and how event-driven updates are organised across them. These refine the generic
UI layer docs with the **one-method-per-event** principle.

---

## Part A — UI Component Rules

The component is a dumb renderer. It owns widgets and layout, emits signals on
user interaction, and exposes methods for its controller to drive it.

1. **Dumb and passive.** A component contains no business logic, makes no workflow
   decisions, accesses no application state, and never calls its controller.
   It only renders, captures interaction, and exposes operations.

2. **Built in named steps.** Construction follows the fixed sequence
   `_create_widgets()` → `_create_layout()` → `_connect_child_signals()`.
   Each step does one job.

3. **Leaf widgets self-configure.** Each leaf widget sets its own `objectName`
   for external QSS styling and configures itself in its own `__init__`/`_setup`.
   No inline styles anywhere — appearance is driven by stylesheets via object names.

4. **Communicate only by signal.** A component emits an external signal on user
   interaction. It never references another component, and never reaches up to a
   controller, handler, action, or state.

5. **Expose primitive accessors only.** Public methods read or set primitive
   values on the component (`get_text()`, `set_enabled(bool)`, `set_project_name(str)`).
   Components never accept or return domain models.

6. **Manage internal UI state only.** A component may track its own widget-level
   state (e.g. enabling Send when text is present). It never tracks application
   state (loaded project, history, mode).

7. **One signal per distinct user intent.** Each meaningful interaction gets its
   own signal (`send_triggered`, `clear_clicked`, `mode_changed`). Don't overload
   one signal to mean several things.

8. **Display-only components emit nothing.** A component with no user interaction
   (e.g. the chat area) exposes only operation methods and has no signals and no
   handler.

---

## Part B — Component Controller Rules

The controller is the **only** object that touches its component from outside. It
bridges the component and the event handlers. It holds no business logic and never
talks to another controller.

1. **One controller per component.** Exactly one controller owns each component.
   Controllers never call or reference each other.

2. **Two kinds of methods only — `bind_*` and operations.**
   - `bind_<signal>(method)` — wires one component signal to a handler method.
     One bind method per component signal.
   - operation methods — drive the component (read values, update widgets).

3. **Consume and return primitives only.** Controllers translate between the
   handler and the component using primitives (or UI-local view types). A
   controller never accepts or returns a domain model — the handler unpacks
   models to primitives before calling the controller.

4. **No business logic, state, or workflow.** A controller never accesses Core,
   State, Actions, or Event Handlers. It does not decide *when* things happen —
   only *how* to apply a given instruction to its component.

5. **One operation method per event — the event-shaped method rule.**
   When an event requires several widget operations on a component, the controller
   exposes **one method that performs all of that component's work for that event**,
   rather than making the handler issue several fine-grained calls.

   - Name the method for the **event**, prefixed with `reset_on_`:
     `reset_on_clear_chat()`, `reset_on_project_loaded(name)`,
     `reset_on_send_result(...)`, etc. One prefix is used for every event method
     so the convention is uniform and instantly recognisable.
   - The method bundles every widget op that component needs for that event into
     one call.
   - The handler then calls **one method per controller per event** — never a
     sequence of low-level setters.

   Example — the clear-chat event touches four components, so each controller
   exposes its own `reset_on_clear_chat()`:

   ```
   chat_area.reset_on_clear_chat()    # clears bubbles, shows placeholder
   status_bar.reset_on_clear_chat()   # hides banner
   input_bar.reset_on_clear_chat()    # re-enables input
   toolbar.reset_on_clear_chat()      # disables Clear + clears project label
   ```

   The handler reads as "reset every layer for this event":

   ```python
   def on_clear_clicked(self):
       self._actions.clear_chat.execute()
       self._chat_area.reset_on_clear_chat()
       self._status_bar.reset_on_clear_chat()
       self._input_bar.reset_on_clear_chat()
       self._toolbar.reset_on_clear_chat()
   ```

   Example — the project-loaded event (success) touches two components:

   ```python
   def _on_result(self, index):
       self._set_busy(False)
       self._toolbar.reset_on_project_loaded(os.path.basename(index.project_path))
       self._chat_area.reset_on_project_loaded()
   ```

   Example — the send event (result / error) touches the chat area and input bar:

   ```python
   def _on_result(self, result):
       user_msg, assistant_msg = result
       self._chat_area.reset_on_send_result(
           user_msg.role, user_msg.content,
           assistant_msg.role, assistant_msg.content,
       )
       self._input_bar.reset_on_send_cleared()
       self._set_busy(False)

   def _on_error(self, error):
       self._chat_area.reset_on_send_error(str(error))
       self._set_busy(False)
   ```

6. **Event-method names: same name on a uniform fan-out, distinct names when the
   slices differ.**
   - When one event fans out to several controllers that each perform the *same
     kind* of reset, they all use the **same method name** (e.g. every controller
     in the clear event exposes `reset_on_clear_chat()`). This makes the pattern
     obvious at the call site and signals "these calls all belong to one event."
   - When an event drives genuinely *different* work on each controller, each
     keeps its own descriptive `reset_on_<event>_<slice>` name. The send event is
     the example: `chat_area.reset_on_send_result(...)` adds the bubbles while
     `input_bar.reset_on_send_cleared()` clears the box — different slices, so
     different names, still under the same `reset_on_` prefix.

7. **Fine-grained setters may still exist** for ops that genuinely stand alone
   (e.g. `set_enabled(bool)` during busy toggling, `get_text()`). The event-shaped
   method rule applies when an **event** drives **multiple** ops on one component;
   it does not force trivially single-op events into wrapper methods unless they
   are part of a fan-out group. (A single event that fans out to several
   controllers — like clear — does give even single-op controllers an
   event-method, so the handler reads uniformly.)

8. **Controllers expose, never orchestrate.** A controller groups *its own*
   component's work for an event. It never coordinates across components — that
   fan-out (calling each controller's event method) is the handler's job.

---

## Part C — The Same Principle in the State Layer

The one-method-per-event principle is not UI-only. The **StateController** applies
it too: when an event needs several state writes, the controller exposes **one
coarse method** that performs them together, and the Action calls just that method.

- `reset_on_clear_chat()` — drops chat, project, and index together.
- `reset_on_project_loaded(path, index)` — stores project + index and starts a
  fresh chat.
- `add_message_on_send(user_msg, assistant_msg)` — appends both turns together;
  this is the atomic send-commit point (reached only after a successful reply).

State-method names describe the **state change for the event**. The send commit is
named `add_message_on_send` (what it does to state) rather than after any UI
surface. Fine-grained writes (`clear_chat`, `set_project_path`, `add_chat_message`,
`set_processing`) still exist as building blocks the coarse methods compose, and
are used directly when an event needs only a single write.

---

## Why this split

- **Components** stay swappable dumb views: object names + signals + setters.
- **Controllers** become the single, readable vocabulary of "what can happen to
  this component," expressed in event terms.
- **Handlers** shrink to orchestration: call the action, then call one
  event-shaped method per controller. No widget-level detail leaks into handlers.
- The same **one-method-per-event** principle now holds in three places —
  StateController (`reset_on_clear_chat()`), component controllers
  (`reset_on_clear_chat()` each), and the handler that calls them — so each layer
  has exactly one place that knows its own slice of an event.

# ui_component_controller_rules.md