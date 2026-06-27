# State & State Controller — Design Rules

App-specific rules for how application state is stored and accessed, and how
event-driven state changes are organised. These refine the generic state doc with
the **one-method-per-event** principle, mirroring the UI component/controller split.

---

## Part A — State Object (AppState) Rules

`AppState` is the single in-memory container for all application data. It is pure
data — the dumb equivalent of a UI component at the state layer.

1. **Data only — no methods, no logic.** `AppState` is a plain dataclass of fields.
   It has no methods, no computed properties, no validation, no workflow. It only
   holds values.

2. **One state object for the app.** All application data lives in a single
   `AppState` instance (messages, processing flag, project path, project index).
   There is no second state object and no per-feature state scattered elsewhere.

3. **Fields are primitives or passive domain models.** A field is either a
   primitive/collection (`list[ChatMessage]`, `bool`, `str | None`) or a passive,
   frozen domain model from `core/models` (`ProjectIndex`). Never store live
   service objects, gateways, widgets, or controllers.

4. **May import `core/models` for typing only.** `AppState` imports domain models
   solely for field type annotations. It never imports Core logic, Gateways,
   Actions, or UI.

5. **No defaults that hide intent.** Mutable defaults use `field(default_factory=…)`.
   Optional-until-set fields default to `None` so "not yet set" is explicit and
   readable.

6. **Nothing touches `AppState` directly except the StateController.** No action,
   handler, gateway, or UI object reads or writes `AppState` fields. All access is
   mediated by the StateController.

---

## Part B — State Controller Rules

The StateController is the **only** object that touches `AppState`. It is the state
layer's equivalent of a component controller: the single, controlled vocabulary of
"what can happen to the state," expressed in operations.

1. **Single access point.** Exactly one StateController owns `AppState`, injected by
   constructor. Every read and write goes through it. No direct field access from
   anywhere else.

2. **No business or workflow logic.** The StateController does not orchestrate
   workflows, call Gateways, talk to Core, or decide *when* state changes. It only
   performs the state operations it is told to. Actions decide *when*; the
   StateController decides *how to apply* a change to the data.

3. **Reads return copies of mutable collections.** Any read that exposes a mutable
   collection returns a copy (`list(self._state.messages)`), so callers cannot
   mutate internal state by side effect.

4. **One operation method per event — the event-shaped method rule.**
   When an event requires several field writes, the StateController exposes **one
   method that performs all of that event's state changes**, rather than making the
   action issue several fine-grained writes.

   - Name the method for the **event**, prefixed by intent:
     `reset_on_clear_chat()`, `apply_on_project_loaded(path, index)`, etc.
   - The method bundles every field write that event needs into one cohesive call.
   - The action then calls **one StateController method per event** — never a
     sequence of low-level setters.

   Example — the clear-chat event resets three fields, so it becomes one method:

   ```python
   # StateController
   def reset_on_clear_chat(self) -> None:
       self._state.messages.clear()
       self._state.project_path = None
       self._state.project_index = None
   ```

   ```python
   # ClearChatAction
   def execute(self) -> None:
       self._state.reset_on_clear_chat()
   ```

5. **Atomic multi-write commits stay inside one method too.** Where an event commits
   several writes that must land together (e.g. appending both the user and
   assistant messages after a successful reply), expose them as one method or call
   them as one uninterrupted block inside the action's success path, so a failure
   never leaves a partial commit.

6. **Fine-grained accessors may still exist** for genuinely standalone reads/writes
   (`get_chat_messages()`, `get_project_path()`, `set_processing(bool)`,
   `is_processing()`). The event-shaped method rule applies when an **event** drives
   **multiple** field writes; it does not force single-write events into wrappers.

7. **Group by event, not by field.** Prefer one method that captures "all the state
   changes for this event" over several methods each touching one field, when those
   fields always change together for that event. This keeps the action thin and
   keeps the meaning of an event's state change in one place.

8. **The StateController exposes; the Action orchestrates.** The StateController
   groups the state writes for an event into one method. It never decides which
   events occur, never calls Gateways, never sequences a workflow — that is the
   Action's job.

---

## Why this split

- **AppState** stays a dumb data container: fields only, like a dumb component.
- **StateController** becomes the single, readable vocabulary of "what can happen
  to the state," expressed in event terms (`reset_on_clear_chat()`).
- **Actions** shrink to orchestration: read what they need, call the gateway, then
  call one event-shaped state method. No field-level detail leaks into actions.
- The same **one-method-per-event** principle now holds consistently across the
  app — StateController (`reset_on_clear_chat()`), component controllers
  (`reset_on_clear_chat()` each), and the handler/action that call them — so every
  layer has exactly one place that knows its own slice of an event.
