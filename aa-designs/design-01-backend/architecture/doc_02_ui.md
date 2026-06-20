# UI Layer

## Purpose

* Render the user interface.
* Capture user interactions.
* Display application data.
* Remain independent of business logic.

---

## Directory Structure

```text
ui/
├── main_window.py          # Top-level application window
│
├── pages/                 # Screen composition
│   └── main_page.py       # Main application page
│
├── components/            # Reusable UI components
│
├── controllers/           # UI component controllers
│
└── styles/                # UI styling resources
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
* Each ui component lives in its seprate directory inside the components/ directory.
