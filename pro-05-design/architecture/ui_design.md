# ChatPDF AI Agent — UI Layer Design Document

**`ui/` Directory — Architecture & Conventions** — Finalized as of June 17, 2026

## 1. Overview

This document records the architecture, conventions, and directory structure finalized for the `ui/` package of the ChatPDF application. For the top-level structure and how `ui/` fits with `core/`, `api_server/`, `api_client/`, `desktop_local/`, and `desktop_remote/`, see app_design.md.

## 2. Directory Structure

```
ui/
├── __init__.py
├── main_window.py
├── components/
├── controllers/
├── pages/
│   ├── __init__.py
│   ├── main_page.py
│   └── settings_page.py
└── styles/
```

> **Note:** The internal file breakdown of `components/`, `controllers/`, and `styles/` has not been finalized into specific filenames yet — the sections below define the rules each file in those folders must follow, regardless of how many files end up in each folder.

## 3. Layer Responsibilities

**`main_window.py`**
A thin `QMainWindow` shell. Owns the menu bar, status bar, and any application-level chrome. Sets `pages/main_page.py` as its central widget. Contains no business logic and no component logic.

**`components/`**
Pure, reusable PyQt6 widgets. See Section 4 for full responsibilities.

**`controllers/`**
Non-widget classes, one per component, that own all UI-level logic for that component. See Section 5 for full responsibilities.

**`pages/`**
Assembles one full application screen. A page:
- Imports only from `controllers/` (never from `components/` directly).
- Receives a backend engine object as a constructor argument, passed down from whichever app's entry point created it (`desktop_local/main.py` or `desktop_remote/main.py`) — see Section 6.
- Instantiates the controllers it needs, passing that backend object along, and receives each controller's `.component` handle.
- Adds each controller's `.component` handle into a layout to build the visible screen.

A page never knows or cares whether the backend object it was given is a `core/` object or an `api_client/` object — this is what makes `ui/` reusable across both `desktop_local/` and `desktop_remote/`. `main_page.py` is the primary application screen (sidebar + PDF viewer + chat panel). `settings_page.py` is the settings screen.

**`styles/`**
Holds the application's visual styling: QSS stylesheets and any shared style constants (colors, fonts, spacing) used to theme the PyQt6 widgets. Internal file breakdown not yet finalized.

## 4. Component — Key Responsibilities

A Component is a PyQt6 widget class. Its responsibilities are:

- Dumb Renderer: receive data and update the UI accordingly.
- Provide a method to create its UI elements.
- Provide a method to build its layout.
- Provide methods for signals/events, if needed.
- Emit an external signal (via a `bind_<event>` method — see Section 6) when a user interaction occurs.
- Provide clean methods to handle its own internal signals (scrolling, focus, hover, animations).
- Manage its own internal UI state only.

A Component must **not**:
- Decide what happens after an event — it only reports that the event happened.
- Access global or application state.

## 5. ComponentController — Key Responsibilities

A ComponentController is a non-widget class that manages exactly one UI component. Its responsibilities are:

- One controller per UI component.
- Contains only operation methods, called during event handling. There can be one or more methods corresponding to a single event.
- Owns all UI-level logic for that component.
- Manages the internal UI state of its component (by calling the component's own setter/getter methods — never by reaching into the component's internal widgets directly).
- Acts as the bridge between the UI component and whatever backend engine object it was given (in practice, a class from `core/` when running as `desktop_local/`, or a class from `api_client/` when running as `desktop_remote/` — the controller does not know or care which).
- Ensures the component remains dumb and passive.

A ComponentController must **not**:
- Contain business logic (that belongs in `core/`, regardless of deployment mode).
- Communicate with other ComponentControllers directly.

> **Note:** Because Python does not enforce interfaces, the "same shape" requirement between a `core/` engine object and an `api_client/` engine object is currently kept by naming convention only (both must expose the same method names, e.g. `ask_question`, `load_pdf`). A formal interface/Protocol describing this contract has been deliberately deferred — see app_design.md, Section 7, Open Items.

## 6. Construction & Wiring Convention (Final Decision)

- The ComponentController instantiates its own Component inside its `__init__` method and stores the instance on `self.component`.
- The Component exposes `bind_<event>` methods (example: `bind_clear_clicked(self, method)`), used to register a callback for a given user action. This is how a Component satisfies the "emit an external signal" responsibility from Section 4 without ever needing to know who is listening.
- The ComponentController calls these `bind_<event>` methods inside its own `__init__`, connecting each one to one of its own handler methods.
- A page never constructs a Component directly. It only constructs ComponentControllers, and reaches the actual widget through each controller's `self.component` handle when building its layout.
- The backend engine object a controller calls into is never imported by the controller module directly. It is passed in by the page that constructs the controller, which in turn received it from the app's entry point (`desktop_local/main.py` or `desktop_remote/main.py`). This is what keeps `ui/` identical across both deployment modes.

## 7. Data Flow Example: User Clicks "Clear" in Chat Panel

| Layer | What Happens |
|---|---|
| `components/` | `ChatPanel` defines `bind_clear_clicked(self, method)`, which connects its Clear button's `clicked` signal to whatever method is passed in. |
| `controllers/` | `ChatController.__init__` creates `self.component = ChatPanel()`, then calls `self.component.bind_clear_clicked(self.on_clear_clicked)`. |
| `controllers/` | `on_clear_clicked()` runs: tells the component to clear its messages, and/or resets related state via the injected backend engine object. |
| `pages/` | `main_page.py` never sees this exchange. It only added `self.chat_controller.component` into its layout once, at screen-assembly time. |

## 8. Key Design Decisions Log

- `ui/` split into `components/`, `controllers/`, and `pages/` (`pages/` chosen over `views/` and `screens/`).
- `styles/` added to hold QSS stylesheets and style constants, kept separate from component and page code.
- Controllers instantiate their own components — not the reverse, and not pages.
- Components expose behavior only through `bind_<event>` methods and plain getter/setter methods — never through direct widget access from outside the component.
- Pages depend only on controllers, never on components directly.
- Controllers never communicate with other controllers directly.
- `ui/` is shared across `desktop_local/` and `desktop_remote/`. Pages and controllers never import `core/` or `api_client/` directly — they receive a backend engine object via constructor injection from whichever app's entry point instantiates them.
- A formal interface/Protocol for that backend engine object has been deliberately deferred (contract kept by naming convention only, for now).

## 9. Open Items (Not Yet Finalized)

- Internal file breakdown of `components/`, `controllers/`, `styles/` (which specific files/widgets each will contain, beyond the examples used in discussion such as `chat_panel`, `pdf_viewer`, `sidebar`).
- Mechanism for indirect cross-controller communication, given that direct controller-to-controller calls are disallowed. Candidates discussed but not yet decided: routing through the owning page, or a shared event bus.
- Formal interface/Protocol for the injected backend engine object (deferred — see app_design.md, Section 7).