# UI Layer

## Purpose

* Render the user interface.
* Capture user interactions.
* Display application data.
* Remain independent of business logic.

---

## Directory Structure

```

ui/
│
├── screen_manager.py       # selects + builds ONE screen at startup, returns UIBundle
│
├── main_window.py          # Top-level application window. QMainWindow shell, single central widget
│
├── ui_bundle.py            # UIBundle dataclass. bundels all the component controllers
│
├── pages/                  # Screen composition. can contain multiple screens for the app.
│   ├── main_page.py        # Default main application page
│   └── main_page_2.py      # optional other look variants
│
├── components/             # Reusable UI components
│
├── controllers/            # UI component controllers
│
└── styles/                 # UI styling resources
```

---

## Component

> Responsibilities

* Create UI elements.
* Build layouts.
* Define signals if needed.
* Display data provided by controllers.
* Emit external signals when user interaction occurs.
* Handle internal UI signals if needed. (scrolling, focus, hover, animations)
* Manage internal UI-only state.
* Prefer external styling where possible.
- Provide one method to create UI Elements if needed
- Provide one method to build Layout if needed
- Methods for signals if needed

> Must Not

* Contain business logic.
* Decide application workflow.
* Access application state.
* Interact with other components.
* Call component controllers directly.

---

## Component Controller

> Responsibilities

* One controller per component.
* Act as the bridge between application logic and the component.
* Act as the bridge between the component and the rest of the app.
* Own UI-level behavior of its component.
* Expose operation methods used during event handling.
* Expose methods to bind component events to external callback functions/methods.
* Read values from the component.
* Update component UI.
* Manage internal UI state.

> Must Not

* Contain business logic.
* Access core directly.
* Access state directly.
* Communicate with other component controllers directly.
* Perform application workflows.
* Receive, name, or import Core domain models (e.g. `ChatMessage`, `PDFDocument`).

---

```
The key principle: ui/ owns all window/page wiring. Main Controller never touches widgets, windows, or layouts — it only asks ui/ to activate a screen and gets back a UIBundle to wire handlers to.
```

---

## Data Contract

Component Controller methods accept **only primitive values or UI-local view
types**. Core domain models are never passed into the UI layer; they are
unpacked by the Event Handler before the controller is called (see
*Event Handlers → Core Model Translation Boundary*).

This guarantees the UI layer has no import dependency on Core, satisfying the
dependency-direction rule (UI never depends on Core).

If a payload grows large enough that long primitive argument lists become
unwieldy, a **UI-local view object** may be used instead — a dumb dataclass
owned by the UI layer, not by Core. The boundary rule is unchanged: no Core
type crosses into the UI layer.

---

## Page Responsibilities

A page assembles components into a screen.

### Responsibilities

* Create components.
* Create component controllers.
* Build screen layout.
* Return controller bundle.

### Must Not

* Contain business logic.
* Access application state.
* Perform application workflows.

---

## Design Rules

* One controller per component.
* Components remain dumb and passive.
* Controllers own UI-level behavior.
* Components communicate through signals.
* Components never communicate directly.
* Controllers never communicate directly.
* UI layer contains no business logic.
* UI layer never imports or names Core domain models; controllers consume primitives or UI-local view types only.