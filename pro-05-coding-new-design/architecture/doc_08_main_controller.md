# Main Controller & Launcher — Design Rules

App-specific rules for the composition root (`MainController`) and the launcher
(`desktop_local/main.py`). Together they are where everything is built and wired —
and the only place that knows local-vs-remote mode.

---

## Part A — Launcher Rules

The launcher is the entry point. It is the only place that loads config, builds Core
services, and decides mode.

1. **Load config first, fail fast.** Call `load_config()` before building anything;
   on a missing required value, print a friendly message and exit.

2. **Build Core services from primitives.** Construct each Core service from config
   primitives (`api_key`, `model`, `temperature`, …). The launcher passes primitives,
   never pre-built provider objects — services build their own clients.

3. **Decide mode by building the matching gateways.** `build_local_gateways(config)`
   wraps Core services directly (local). A future `desktop_remote` launcher builds
   gateways that wrap an API client. Mode is decided **only** here.

4. **Assemble tools and inject them.** Agent tools are collected into a
   `list[BaseTool]` in the launcher and injected into the agent service. The launcher
   owns this assembly.

5. **Build the GatewayBundle and hand it up.** The launcher constructs the frozen
   `GatewayBundle` and passes it to `MainController(gateways)`. It never builds state,
   actions, UI, or handlers.

6. **Start the app, then exec.** `MainController(gateways).start()` builds and wires
   everything; then the launcher enters the Qt event loop. The launcher does no
   wiring itself.

---

## Part B — Main Controller Rules

The MainController is the single composition root. It creates and wires every object
and holds no business logic.

1. **Exactly one composition root.** One `MainController` per app. It is the only
   place objects are created and dependencies wired.

2. **Receives gateways; never builds them or decides mode.** Its constructor takes
   the `GatewayBundle` and stores it. It never constructs gateways, reads config, or
   learns which mode produced the gateways.

3. **`start()` runs a named-step startup sequence.** One task per step, in order:

   ```
   _create_state → _create_actions → _create_ui → _create_style
   → _create_event_handlers → _wire_events → _apply_default_theme
   → _unlock_level → _show
   ```

   Each step is its own small method; `__init__` only stores the gateways.

4. **Holds no business logic.** It creates and wires only. It must not access Core,
   mutate State, call Gateways, manipulate widgets, or contain event-handling logic.

5. **Delegates all UI to the ScreenManager.** UI is built via
   `ScreenManager.build()` (returns the `UIBundle`); the controller never touches
   windows, pages, or widgets directly.

6. **Creates the StyleManager and applies the default theme.** The StyleManager is
   created here (not the launcher) and injected where needed; the default theme is
   applied as a startup step.

7. **Handlers are stored as instance attributes.** Every handler is held as
   `self._<name>_handler` to prevent garbage collection from silently killing its
   signal connection.

8. **All signal wiring lives in `_wire_events()`.** Binding component signals to
   handler methods happens in one place, using `self._` attributes only — the
   MainController, not the handler, connects signals.

9. **`_unlock_level()` reflects the current build level.** A single
   `UNLOCK_LEVEL` constant drives which UI capabilities are unlocked
   (`toolbar.unlock_level(...)`), so advancing a level is a one-line change.

---

## Why this split

- The **launcher** is the single mode decision point: load config, build Core, build
  the gateway bundle for this mode, start.
- The **MainController** is the single wiring point: a flat, named startup sequence
  that creates each layer once and connects them, with no logic of its own.
- Because the launcher owns config/mode and the MainController owns wiring, the two
  hardest things to reason about — *where does this object come from* and *what mode
  are we in* — each have exactly one home.

# Main Controller & Launcher — Design Rules