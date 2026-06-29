# Layered App — Design Rules (Generic)

A simple rulebook for building a layered desktop app. It covers five parts:

1. UI Component
2. UI Component Controller
3. State (data object)
4. State Controller
5. Event Handler

The big idea that runs through all of them is the **one-method-per-event rule**:
for any event (a button click, a selection, a send), each layer has **one method**
that does all of that layer's work for that event. The event handler then calls
one method per layer. This keeps every file small and easy to read.

Replace the example names (`clear_chat`, `project`, `chat_area`) with your own.

---

## Part 1 — UI Component

A UI component is the visible thing on screen (a toolbar, an input box, a chat
area). Think of it as a "dumb" view. It shows widgets and tells the rest of the
app when the user did something.

1. A component only draws widgets and reports user actions. It holds no app logic.
2. Build it in three small steps: create the widgets, lay them out, connect their
   signals.
3. Each small widget sets its own name (an `objectName`) so styling can come from
   a separate stylesheet. Do not write colors or styles inside the code.
4. When the user does something, the component sends a **signal** (an event). It
   does not do the work itself.
5. A component never talks to another component. It only sends signals out.
6. A component never talks to its controller, the state, or the business logic.
7. Give the component simple methods that take or return **plain values** only
   (text, true/false, a name). Never pass it a complex data object.
8. A component may track tiny visual state (like "is the Send button enabled"),
   but never app data (like the chat history).
9. Each different user action gets its **own** signal. Do not make one signal mean
   many things.
10. If a component never reacts to the user (it only displays things), it has no
    signals and needs no event handler.
11. A Component shoud have seprate methods for following task:
    - **to create the widgets** 
    - **lay them(widgets) out** 
    - **connect their signals**

---

## Part 2 — UI Component Controller

A controller is the one object allowed to touch its component from outside. It is
the "remote control" for that component. There is exactly one controller per
component.

1. One controller controls exactly one component. Controllers never talk to each
   other.
2. A controller has only two kinds of methods:
   - **bind methods**: connect one component signal to a handler method.
   - **operation methods**: tell the component to do something.
3. A controller only uses **plain values** (text, true/false). It never takes or
   returns a complex data object.
4. A controller holds no business logic and no app data. It does not decide *when*
   things happen — only *how* to update its component.
5. **One method per event (the main rule):** if an event needs several changes on
   one component, put them all in **one** method named after the event. Example:
   `reset_on_clear_chat()` clears the messages and shows the empty placeholder.
6. When one event touches several controllers, give each controller the same event-named 
   method even if that controller's slice is just one call. Consistency of naming matters 
   more than avoiding trivial wrappers — it lets you follow one event name across the whole app
7. When one event affects several components, give each controller a method with
   the **same name** for its own part. Example: every controller has its own
   `reset_on_clear_chat()`.
8. You may still keep small single-purpose methods for actions that stand alone
   (like `set_enabled(true)` or `get_text()`). The one-method rule is only for when
   an event needs **several** changes at once.
9. A controller only handles **its own** component. It never calls another
   controller. Combining many controllers for one event is the handler's job.

---

## Part 3 — State (the data object)

State is one object that holds all the app's current data in memory (like the chat
history, a loaded file path, a "busy" flag). Think of it as a plain box of data.

1. The state object holds **data only**. It has no methods and no logic.
2. Keep all app data in **one** state object. Do not scatter data around the app.
3. Each field is either a plain value/list or a simple, read-only data model. Never
   store live tools, services, windows, or controllers inside state.
4. State may import data models only to label its field types. It never imports
   business logic, services, or UI.
5. Use clear defaults: empty list for lists, and `None` for "not set yet", so it is
   obvious what is empty.
6. Nothing in the app reads or writes the state fields directly — except the State
   Controller.

---

## Part 4 — State Controller

The State Controller is the one object allowed to touch the state. It is the
"remote control" for the data. Everything that reads or changes data goes through
it.

1. There is exactly one State Controller, and it is the only thing that touches the
   state object.
2. It holds no business logic. It does not call services or decide *when* data
   changes. It only knows *how* to change the data when told.
3. When it returns a list, it returns a **copy**, so callers cannot change the
   real data by accident.
4. **One method per event (the main rule):** if an event needs to change several
   fields, put all those changes in **one** method named after the event. Example:
   `reset_on_clear_chat()` clears the history, the file path, and the index together.
5. Changes that must happen together (like saving both the question and the answer
   after a successful reply) go in one method or one unbroken block, so a failure
   never leaves half-saved data.
6. You may still keep small single-field methods for standalone reads/writes (like
   `get_messages()` or `set_busy(true)`). The one-method rule is only for events
   that change **several** fields.
7. Group methods by **event**, not by field, when the fields always change together
   for that event.
8. The State Controller only **applies** changes. It never decides which events
   happen and never runs a workflow — that is the Action's / handler's job.

---

## Part 5 — Event Handler

The event handler is the "conductor". When the user does something, the handler
runs the steps in order: read input, check conditions, change the data, update the
screen. It is the only place that coordinates several components at once.

1. Organize handlers by the component that sends the event: one folder per
   component, one handler file per event.
2. Name handler methods after the event, like `on_clear_clicked` or
   `on_file_selected`.
3. A handler receives the things it needs (the actions and the controllers) handed
   to it. It never builds them and never imports the UI directly.
4. Keep each handler stored as a normal attribute on the main controller, so it is
   not deleted by accident (which would break its signal).
5. A handler may use only the **controllers** and the **actions**. It never touches
   the data or the business logic directly.
6. The action returns a data model; the handler pulls out the plain values from it
   before passing them to a controller. The screen never sees a data model.
7. The handler picks where errors show up: a chat error shows in the chat area; a
   load error shows in the status bar.
8. Slow work runs on a background thread so the screen does not freeze. The handler
   manages this; the action stays simple and synchronous.
9. Checks that block an event (like "you must load a file first") happen in the
   handler, **before** the action runs.
10. **One method per layer (the main rule):** the handler does not make many tiny
    calls. For an event it calls:
    - one **action** (which calls one state method inside), and
    - one **event-named method on each controller** that the event touches.
11. Do the data change first (the action), then update the screen (one method per
    controller). Example:

    ```python
    def on_clear_clicked(self):
        self.actions.clear_chat.execute()      # changes the data
        self.chat_area.reset_on_clear_chat()   # updates each component
        self.status_bar.reset_on_clear_chat()
        self.input_bar.reset_on_clear_chat()
        self.toolbar.reset_on_clear_chat()
    ```

12. Use the **same event name** across all layers (the action, the state method, and
    every controller method). Then you can follow one event through the whole app by
    searching one name, like `reset_on_clear_chat`.
13. Turning the screen "busy" on/off during slow work can stay as small
    enable/disable calls. The one-method rule is only for the event's real updates,
    not the busy on/off switch.
14. Create a event handling bundle for clean design.


---

## Part 6 — Action

An action is one job the app can do (send a message, load a file, clear the chat).
It is the "worker" that changes data and talks to the outside world. The handler
tells it to run; it does the steps and returns a result.

1. One action does **one job**. If you have two jobs, make two actions.
2. Build each action with the State Controller and the Gateways. It uses only
   these two things.
3. An action has one main method, usually called `execute(...)`.
4. The action is the **only** layer allowed to change the data (through the State
   Controller) and to call the outside world (through a Gateway).
5. An action never touches the screen, the controllers, or the handlers.
6. If the data needs shaping before sending it out (like turning a model into a
   plain dictionary), do that shaping **inside the action**, not in the model or
   the gateway.
7. Change the data **only after** the outside call succeeds. If the call fails,
   leave the data exactly as it was.
8. When several changes must happen together, do them in one unbroken block, so a
   failure never leaves half-finished data.
9. If something goes wrong, **raise an error**. Do not hide it. The handler will
   catch it and show it.
10. An action runs straight through (synchronous). It does not manage threads —
    that is the handler's job.
11. The action returns a data model (or a small group of them) to the handler. It
    does not return screen-ready text; the handler turns the model into plain
    values.

---

## Part 7 — Gateway

A gateway is the door between your app and the outside world (a database, an API,
a library, the file system, or a Core capability). It hides *how* the outside work is done.
The action calls the gateway and gets back a clean result.

1. One gateway covers one outside concern (one API, one store, one service group,
   or one domain capability).
2. Only make a gateway when there is real work to expose. Do not make empty
   gateways.
3. The gateway shows the action only the few methods it needs. It hides all the
   messy implementation details inside.
4. The gateway takes ready-to-use input from the Action and delegates it to the appropriate Core Service or Core Workflow. It does not reshape the data itself.
5. For **simple, atomic work**, the gateway may call a single Core service directly.
6. For **larger domain processes**, the gateway delegates to a Core workflow, which
   coordinates multiple Core services.
7. Whether the gateway calls one service or one workflow is an internal detail.
   The action should not know or care. A Gateway should normally expose either a Service or a Workflow, never both for the same operation.
8. The gateway returns clean results (plain values or data models), never raw
   replies from an external library or provider.
9. The gateway holds **no business logic**. It only delegates the work and tidies
   up the result.
10. The gateway never touches the screen, the controllers, the handlers, the
    state, or the actions.
11. Keep the gateway's public methods the **same** whether the work is done
    locally or remotely (local library now, remote API later). Then the action
    never has to change.
12. All gateways are gathered into one bundle, built once at startup and handed to
    the app.

---

## Part 8 — Core

Core is where the real work and the real data shapes live (the business logic and
the data models). Core knows nothing about the screen, the app's flow, or where it
runs. You could reuse Core in a totally different app.

Core has three main parts:

* **models** — simple, read-only data shapes.
* **services** — small, reusable capabilities that each perform one job.
* **workflows** — higher-level domain processes that combine several services to
  solve one business problem.

### Models

1. A **model** is a simple, read-only data holder. It just stores values. It has
   no logic and does no saving or formatting.
2. Give models easy "factory" shortcuts to create them (like `Message.user(text)`),
   and keep all the fixed text constants (like role names) in one small place.

### Services

3. A **service** performs one clear, reusable capability (call an LLM, extract
   text from a PDF, split text into chunks, generate embeddings, store vectors,
   perform OCR, etc.).
4. Services should be independent. A service should not coordinate several other
   services to perform a larger workflow. If several services need to be coordinated to solve a domain problem, that coordination belongs in a Core Workflow, not inside a service.
5. All the outside-library third-party libraries and provider-specific code(the API client, the PDF reader) live **inside** services.
   Nothing outside Core imports those libraries.
6. A service takes ready input and returns a plain value or a data model.

### Core Workflows

7. A **workflow** represents one domain process composed of multiple services.
   Examples include building a RAG index, retrieving relevant documents,
   generating an AI answer, or summarizing a collection of files.
8. A workflow owns the sequence of domain steps. For example, a RAG index builder
   may call the extractor service, then the chunker service, then the embedding
   service, and finally the vector store service.
9. Workflows may call multiple services, but services should not call workflows.
10. Workflows never touch the screen, the state, the handlers, the actions, or
    the gateways.
11. Workflows return plain values or data models.
12. Workflows may call other helper methods inside themselves, but they should 
    not call other Workflows. If two workflows need common logic, extract it into a Core Service.
13. A workflow should normally expose one public entry method (for example,
    execute() or build()). Any additional methods are private helper
    methods that support that workflow.

### General Rules

13. Core never touches the screen, the state, the actions, the gateways, or the
    startup code.

14. Core does not know whether the app runs locally or remotely. Core must work the same way whether the app runs locally or remotely.

15. Core contains reusable business/domain knowledge only. Application workflows
    (such as updating state or coordinating UI) belong in Actions, while domain
    workflows belong in Core.


---

## Part 9 — Config

Config is the app's settings, loaded from `.env` files (like the API key, the
model name, the chunk size). It keeps secrets out of the code and lets you change
settings without touching the code.

1. Settings are typed and checked when the app starts (use a settings library so a
   wrong type fails early).
2. Make one settings group per area (one for the app, one for the API, one for the
   search settings, and so on).
3. Required secrets (like an API key) have **no default**. If they are missing, the
   app stops right away with a clear message.
4. Keep secrets in a separate file that is **not** committed (like `.env.local`).
   Keep the safe, non-secret settings in committed files.
5. When two files set the same value, the local secret file wins.
6. Put all the settings groups into one bundle, and load them with one
   `load_config()` function.
7. **Only the startup code (the launcher) reads config.** The UI, handlers,
   actions, state, gateways, and core never import config.
8. The launcher reads the config, then uses it to build the core services and the
   gateways.
9. The settings file paths are relative to where you start the app, so always run
   the app from the project's main folder.
10. Config lives at the top of the project so every version of the app (local or
    remote) can share it unchanged.
11. from pydantic_settings import BaseSettings, SettingsConfigDict

---

## How These Fit Together

```

Launcher
  ├─ Config (startup only)
  ├─ builds Core services
  ├─ builds Core workflows (if needed)
  ├─ builds Gateways
  └─ starts Main Controller

Event → Handler → Action → Gateway → Core(Service/Workflow)
                    │
                    └─> State Controller (change data)
Core(Service / Workflow) → Gateway → Action → (result) → Handler → screen
```

* **Config** sets everything up once at startup.
* **Core Services** provide small, reusable capabilities. does the real work and holds the data shapes.
* **Core Workflows** combine one or more Core Services into a higher-level domain
  process.
* **Gateways** are the doors to the outside, so Core can be swapped or moved. expose a clean interface to the application. A gateway may delegate
  directly to a Core Service for simple work, or to a Core Workflow for more
  complex domain processes.
* **Actions** are the workers that run one job, change the state data, and call a gateway.


---

## Part 10 — Main Controller (the wiring root)

The Main Controller is the place where the whole app is put together. It builds
every object and connects them. Think of it as the person who plugs all the cables
in before the show starts. It does no real work itself.

1. There is exactly **one** Main Controller in the app. It is the single place that
   builds and connects everything.
2. It receives the ready-made **Gateways** from the launcher. It never builds the
   gateways itself and never decides where the app runs (local or remote).
3. It builds things in a clear order, one small step at a time:
   1. create the **state** and the **state controller**,
   2. create the **actions** (and put them in one bundle),
   3. create the **UI** (and get back the bundle of controllers),
   4. create any **helpers** (like a style/theme manager),
   5. create the **event handlers**,
   6. **connect** each component signal to a handler method,
   7. apply the first **theme/setup**,
   8. **show** the window.
4. Each step is its own small method (like `_create_state`, `_create_actions`,
   `_wire_events`). One step does one job.
5. It connects signals to handler methods in **one place** (a `wire_events` step).
   The components and handlers never connect themselves.
6. **Keep every handler as an attribute** (like `self._clear_handler`). If you store
   a handler in a local variable, it gets deleted and its signal stops working.
7. The Main Controller holds **no business logic**. It does not change data, call
   core, or touch widgets directly.
8. All UI work is handed to the screen/UI objects and the controllers. The Main
   Controller only wires; it never draws.

---

## Part 11 — Launcher (`desktop_local/main.py`)

The launcher is the app's starting point — the file you actually run. It loads the
settings, builds the Core, builds the outside-world doors (gateways) for this mode,
and then starts the Main Controller.

1. The launcher is the **only** place that reads the config.
2. It loads the config first. If a required setting (like the API key) is missing,
   it prints a clear message and stops.
3. It builds the **Core services** from the config (the AI client, the PDF reader and so on).
4. If the application uses **Core workflows**, it builds them by supplying the
   required Core services.
5. It builds the **gateways** for this mode (local now, remote later) and puts them
   in one bundle. A gateway may receive one Core service or one Core workflow,
   depending on what it exposes. **This is the only place that decides local vs
   remote.**
6. It creates the Main Controller, hands it the gateways, and tells it to start.
7. The launcher does **no business logic** and **no wiring** of signals. It only
   sets up and hands off.
8. To run a different mode (for example a remote version), you write a **different
   launcher**. Nothing above the gateways has to change.


---

## Part 12 — Top-Level Directory Structure

Keep the project split into clear top-level folders. Each folder matches one layer
of the app. The example names below are placeholders — rename them to fit your app.

```

app_root/
├── conf/                       # settings, loaded from .env files (launcher only)
│   ├── settings/               # one settings group per area + a loader
│   └── env/                    # .env files (secrets kept out of the committed ones)
│
├── core/                       # reusable domain logic (independent of the app)
│   ├── services/               # hide outside libraries here; atomic capabilities; one job per service
│   ├── workflows/              # domain processes built from one or more services
│   └── models/                 # simple, read-only data shapes
│
├── desktop/                    # the app runtime (works the same in any mode)
│   ├── state/                  # the one data object (data only)
│   ├── state_controller/       # the only thing that touches the data
│   ├── gateways/               # doors to the outside + one bundle
│   ├── actions/                # one job per file, grouped by topic
│   ├── action_bundles/         # one bundle holding all actions
│   ├── event_handlers/         # one folder per component, one file per event
│   └── main_controller.py      # the wiring root
│
├── desktop_local/              # the launcher you run (decides local mode)
│   └── main.py
│
├── desktop_remote/             # another launcher for remote mode (optional)
│   └── main.py
│
└── ui/                         # everything on screen (dumb views + controllers)
    ├── components/             # the dumb views, grouped by feature
    ├── controllers/            # one controller per component
    ├── pages/                  # builds a screen from components
    ├── styles/                 # stylesheets (.qss) for looks
    ├── screen_manager.py       # builds one screen, returns the controllers
    ├── main_window.py          # the empty window shell
    ├── ui_bundle.py            # one bundle holding all UI controllers
    └── style_manager.py        # applies a theme
```

### Simple rules for the folders

1. Each folder is one layer. Do not mix layers in one folder.
2. **Lower layers never import higher layers.** UI does not import handlers; Core does not import actions; and so on. Imports only point downward.
3. `conf/` is read only by the launcher. No other folder imports it.
4. `core/models/` contains only passive, read-only data models.
5. `core/services/` contains reusable, single-purpose capabilities.
6. `core/workflows/` contains domain workflows that coordinate one or more Core services. Workflows never know about Actions, State, UI, or Gateways.
7. `core/` sits at the bottom and depends on nothing else in the app.
8. `desktop/` is the same no matter where the app runs. The mode is chosen only in the launcher folders (`desktop_local/`, `desktop_remote/`).
9. `ui/` is also the same in every mode. It hands out a bundle of controllers and nothing more.
10. Each layer hands the next one a **bundle** (a gateway bundle, an action bundle, a UI bundle) so the wiring stays simple.


---

## The Whole Picture

```
You run:  desktop_local/main.py   (the launcher)
   │
   ├─ load config            (settings)
   ├─ build core services    (the real work)
   ├─ build Core workflows   (if needed)
   ├─ build gateways         (doors to the outside; local mode chosen here)
   └─ start Main Controller
         │
         ├─ build state + state controller
         ├─ build actions (bundle)
         ├─ build UI (controllers bundle)
         ├─ build event handlers
         └─ connect signals → handlers → show window

Then, for each user action:
   Event → Handler → Action → Gateway → Core(Service/Workflow)
                       └→ State Controller (change data)

   Core → Gateway → Action → result → Handler → Update UI screen  through Controllers
```

* The **launcher** starts everything and chooses the application's runtime mode.
* The **Main Controller** builds and wires everything together, once.



## The One Idea Behind Everything

For every event, each layer has **one method** that does that layer's part:

```
Event (user action)
  → Handler  : calls one action + one method per controller
      → Action          : calls one State Controller method
          → State Ctrl  : changes all the needed fields in one method
      → Controllers     : each updates its own component in one method
```

- The **component** and the **state object** are dumb: they just hold widgets or
  data.
- The **controllers** (UI and state) are remote controls: one event-named method
  each.
- The **handler** is the conductor: it calls one method per layer, in order.

Use the **same event name** in every layer, and the whole app stays small, tidy,
and easy to follow.


Here’s a clean section you can paste directly into your MD file.

---

## Part 13 — Improved Design of the Core Directory (Feature-Oriented Structure)

As the application grows, organizing `core/` by **artifact type** (services, workflows, models) can become harder to maintain. Related logic for a single domain gets scattered across multiple folders, making it difficult to understand or extend a feature end-to-end.

To improve scalability and cohesion, `core/` can be structured by **domain or feature area** instead of by technical layer.

### Key Idea

Each domain (or feature area) owns its own:

* models
* services
* workflows

This keeps all related business logic together in one place, improving clarity and maintainability.

---

### Recommended Structure

```
core/
│
├── <domain_a>/
│   ├── models/
│   ├── services/
│   └── workflows/
│
├── <domain_b>/
│   ├── models/
│   ├── services/
│   └── workflows/
│
├── <domain_c>/
│   ├── models/
│   ├── services/
│   └── workflows/
│
└── shared/
    ├── models/
    └── services/
```

---

### Design Rules

1. Each domain folder represents a **self-contained business area**.
2. All logic related to a domain stays inside that domain folder.
3. Services and workflows inside a domain should not be scattered across other domains.
4. The `shared/` folder is used only for reusable components that do not belong to any single domain.
5. Cross-domain dependencies should be minimized and should go through well-defined interfaces.
6. The `core/` layer remains independent of UI, state, actions, gateways, and application flow.

---

### Benefits

* Improves feature locality (everything for a feature is in one place)
* Reduces cross-folder navigation
* Makes onboarding easier for new developers
* Scales cleanly as the number of features grows
* Encourages clear domain boundaries and better modular design
