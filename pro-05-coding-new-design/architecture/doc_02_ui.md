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

   - Name the method for the **event**, prefixed by intent:
     `reset_on_clear_chat()`, `apply_on_project_loaded(name)`, etc.
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

6. **Same event-method name across controllers.** When one event fans out to
   several controllers, they all use the **same method name** (`reset_on_clear_chat`)
   for their slice. This makes the pattern obvious at the call site and signals
   "these calls all belong to one event."

7. **Fine-grained setters may still exist** for ops that genuinely stand alone
   (e.g. `set_enabled(bool)` during busy toggling, `get_text()`). The event-shaped
   method rule applies when an **event** drives **multiple** ops on one component;
   it does not force trivially single-op events into wrapper methods unless they
   are part of a fan-out group.

8. **Controllers expose, never orchestrate.** A controller groups *its own*
   component's work for an event. It never coordinates across components — that
   fan-out (calling each controller's event method) is the handler's job.

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
