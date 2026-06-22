# Doc 03 — UI Composition (Generic)

## Purpose

- Define how the UI assembles itself and hands a controller bundle upward.
- Keep all window/page wiring inside `ui/`; the composition root above only receives the bundle and asks for the window to be shown.

---

## Directory Structure

```text
ui/
├── screen_manager.py   # selects + builds a screen, returns the controller bundle
├── main_window.py      # top-level window shell, single central widget
├── ui_bundle.py        # bundle of component controllers
└── pages/
    └── <screen>_page.py
```

---

## Roles

- **Screen Manager** — the UI composition root and the only UI object the Main Controller talks to.
  - `build()` selects a page (from a registry), builds it once, places it in the window, and returns its controller bundle.
  - `show()` displays the window.
- **Main Window** — a dumb shell holding one central widget; sets title/size; no components, no logic.
- **Page** — builds components + controllers + layout; exposes the controller bundle.
- **UI Bundle** — an immutable bundle of the component controllers (never raw components); contains no logic.
- **Style Manager (optional)** — applies a stylesheet/theme globally; injected where theme changes are handled.

## Screen Lifetime (typical)

- One screen is chosen and built at startup and lives for the process; no runtime switching.
- Multiple page classes may exist (same components, different layout/look); only one is instantiated per run.
- If runtime switching is needed, the Screen Manager hosts a stack and the Main Controller re-wires handlers to the new bundle on switch.

---

## Rules

- `ui/` owns all window, page, and component wiring; the composition root never touches widgets directly.
- The Screen Manager owns the window and knows nothing about Event Handlers, Actions, Gateways, Core, or mode.
- The bundle holds controllers only and contains no logic.
- The UI layer is mode-agnostic and identical across launchers.
