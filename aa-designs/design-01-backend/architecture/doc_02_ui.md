# UI Layer

## Purpose

* Render the user interface.
* Capture user interactions.
* Display application data.
* Remain independent of business logic.

---

## Mode Independence

The UI layer is completely **mode-agnostic**. It is built and behaves
identically whether the application is launched by `desktop_local/` or
`desktop_remote/`.

* The UI never knows whether Core runs locally or remotely.
* The UI never builds, sees, or names Gateways, Actions, Core, or State.
* Mode is decided entirely below the UI, at the launcher/Gateway level.

This document therefore applies unchanged to both `desktop_local` and
`desktop_remote`. Only one launcher is being built first (`desktop_local`),
but nothing in this layer needs to change to support the other.

---

## Directory Structure

```text
ui/
│
├── screen_manager.py       # Selects + builds ONE screen at startup, returns UIBundle
│
├── main_window.py          # Top-level application window. QMainWindow shell, single central widget
│
├── ui_bundle.py            # UIBundle dataclass. Bundles all the component controllers
│
├── pages/                  # Screen composition. May contain multiple screen layouts
│   ├── main_page.py        # Default main application page
│   └── main_page_2.py      # Optional other look variant (same components, different layout)
│
├── components/             # Reusable UI components (one directory per component)
│
├── controllers/            # UI component controllers
│
└── styles/                 # UI styling resources
```

---

## Component

### Responsibilities

* Create UI elements.
* Build layouts.
* Define signals if needed.
* Display data provided by controllers.
* Emit external signals when user interaction occurs.
* Handle internal UI signals if needed (scrolling, focus, hover, animations).
* Manage internal UI-only state.
* Prefer external styling where possible.
* Provide one method to create UI elements if needed.
* Provide one method to build layout if needed.
* Provide methods for signals if needed.

### Must Not

* Contain business logic.
* Decide application workflow.
* Access application state.
* Interact with other components.
* Call component controllers directly.

---

## Component Controller

### Responsibilities

* One controller per component.
* Act as the bridge between application logic and the component.
* Act as the bridge between the component and the rest of the app.
* Own UI-level behavior of its component.
* Expose operation methods used during event handling.
* Expose methods to bind component events to external callback functions/methods.
* Read values from the component.
* Update component UI.
* Manage internal UI state.

### Must Not

* Contain business logic.
* Access Core directly.
* Access State directly.
* Communicate with other component controllers directly.
* Perform application workflows.
* Receive, name, or import Core domain models (e.g. `ChatMessage`, `PDFDocument`).

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


## Composition & Wiring Ownership

> The key principle: `ui/` owns all window, page, and component wiring.
> Main Controller never touches widgets, windows, or layouts — it asks `ui/`
> (through the ScreenManager) to build the screen, gets back a `UIBundle`,
> and wires Event Handlers to the controllers inside it.

```text
Launcher (desktop_local / desktop_remote)
        │  builds Gateways, starts Main Controller
        ▼
Main Controller
        │  creates ScreenManager(screen=<key>)
        ▼
ScreenManager
        │  builds the chosen Page  → Page returns UIBundle
        │  sets the Page as MainWindow's central widget
        ▲
        │  returns UIBundle
Main Controller
        │  wires Event Handlers ↔ controllers (once)
        │  ScreenManager.show()
        ▼
   Application running
```

* UI exposes **screen building** and returns a `UIBundle`.
* UI never knows about Event Handlers, Actions, Gateways, Core, or mode.
* Main Controller never builds pages, windows, or layouts itself.

---

## Screen Manager

The ScreenManager is the **composition root of the UI layer** and the single
object the Main Controller talks to.

### Responsibilities

* Select which `Page` to build at startup (by key or config value).
* Create the `MainWindow`.
* Build the chosen `Page` exactly once.
* Receive the `UIBundle` from the built page.
* Set the built page as the `MainWindow`'s central widget.
* Expose the `UIBundle` to the Main Controller.
* Expose a method to show the window (e.g. `show()`).

### Must Not

* Contain business logic or application workflows.
* Know about Event Handlers, Actions, Gateways, Core, or State.
* Decide local vs remote mode.
* Switch screens at runtime (single-screen lifetime).

---

## Main Window

### Responsibilities

* Provide the top-level `QMainWindow` shell.
* Hold a **single central widget** (the selected page).
* Set window title and initial size.

### Must Not

* Create components or controllers.
* Build screen layouts itself.
* Contain business logic.
* Know about modes, Event Handlers, Actions, or Core.

---

## UI Bundle

### Responsibilities

* Be an immutable (frozen) dataclass.
* Bundle every component controller into one object.
* Be returned by the `Page` and relayed by the ScreenManager, so the Main
  Controller can wire Event Handlers to controllers through a single object.

### Must Not

* Contain any logic.
* Hold components directly (it holds controllers, not raw components).

---

## Page

A page assembles components into a screen.

### Responsibilities

* Create components.
* Create component controllers.
* Build screen layout.
* Return a controller bundle (`UIBundle`).

### Must Not

* Contain business logic.
* Access application state.
* Perform application workflows.


---


---

## Screen Lifetime

Exactly **one screen** is selected at application startup and remains active
for the entire lifetime of the process.

* The active screen is chosen **once**, at startup.
* There is **no runtime screen switching**.
* Multiple `Page` classes may exist as alternative looks built from the same
  components, but **only one is instantiated per run**.
* Because the screen never changes, Event Handlers are wired to its
  controllers exactly once, for the life of the application.

---


## Design Rules

* One controller per component.
* Components remain dumb and passive.
* Controllers own UI-level behavior.
* Components communicate through signals.
* Components never communicate directly.
* Controllers never communicate directly.
* UI layer contains no business logic.
* UI layer never imports or names Core domain models; controllers consume
  primitives or UI-local view types only.
* `ui/` owns all window, page, and component wiring; Main Controller only
  receives a `UIBundle` and wires Event Handlers to it.
* Exactly one screen is built at startup and lives for the whole application
  lifetime; there is no runtime screen switching.
* The UI layer is mode-agnostic and identical for `desktop_local` and
  `desktop_remote`.