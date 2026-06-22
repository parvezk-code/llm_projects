# Doc 02 — UI Layer (Generic)

## Purpose

- Render the interface, capture interaction, display data.
- Stay free of business logic and independent of all lower layers except through injected callbacks.
- Never import or name domain models; consume primitives only.

---

## Directory Structure

```text
ui/
├── components/
│   └── <feature>/
│       ├── <feature>_component.py     # dumb composing component
│       └── widgets/
│           └── <widget>_widget.py     # self-contained leaf widget
├── controllers/
│   └── <feature>_controller.py        # one per component
├── pages/
│   └── <screen>_page.py               # assembles components into a screen
├── screen_manager.py
├── main_window.py
└── ui_bundle.py
```

---

## Component (dumb renderer)

- Built in named steps: `_create_widgets()`, `_create_layout()`, `_connect_signals()`.
- Leaf widgets self-configure in `_setup()` and set an `objectName` for external styling.
- Emits external signals on user interaction; exposes public operation methods for its controller to call.
- Manages only internal UI state.
- Must not: contain business logic, decide workflow, access app state, talk to other components, or call its controller.

## Component Controller (one per component)

- Bridges the component and the rest of the app.
- Provides `bind_*` methods (one per component signal) and operation methods (one task each).
- Reads values from and updates the component; consumes primitives only.
- Must not: contain business logic, access Core/State, talk to other controllers, or run workflows.

## Page

- Creates components and their controllers, builds the screen layout, and returns a controller bundle.
- Must not: contain business logic, access state, or run workflows.

---

## Rules

- One controller per component; components stay dumb and passive.
- Components communicate only via signals; components never talk to each other and controllers never talk to each other.
- The UI layer contains no business logic and never accesses State or Core.
- The UI never imports or names domain models; controllers consume primitives (or UI-local view types).
- Appearance is driven by external styling (e.g. stylesheets) via object names, not inline styles.
- `ui/` owns all window/page/component wiring; upper layers only receive a controller bundle.
