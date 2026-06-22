# Doc 04 — Main Controller / Composition Root (Generic)

## Purpose

- Be the single composition root that creates and wires every object.
- Receive ready-made Gateways from the launcher; never build them or decide the mode.

---

## Directory Structure

```text
desktop/
└── main_controller.py
```

---

## Responsibilities

- Receive the Gateway bundle from the launcher.
- Create State and the State Controller.
- Create Actions and pack them into the Action bundle.
- Build the UI (via the Screen Manager) and obtain the controller bundle.
- Create supporting services (e.g. a Style Manager) if any.
- Create Event Handlers, injecting controllers + the Action bundle (+ services).
- Bind every component signal to a handler method.
- Define the startup sequence and show the window.

## Startup Sequence (one task per step)

```text
create_state → create_actions → create_ui → create_services
→ create_event_handlers → wire_events → (post-build steps) → show
```

## Launcher Boundary

```text
desktop_local  → builds LOCAL Gateways  → runs MainController
desktop_remote → builds REMOTE Gateways → runs MainController
```

The Main Controller only ever receives Gateways; it never learns which mode produced them.

---

## Rules

- Exactly one composition root per application.
- It creates objects and wires dependencies; it holds no business logic.
- It must not access Core, mutate State, manipulate widgets directly, or contain event-handling logic.
- It must not build Gateway implementations or decide local-vs-remote mode.
- All UI work is delegated to the Screen Manager and controllers.
