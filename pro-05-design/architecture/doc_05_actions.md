# Actions

## Purpose

Actions implement application workflows.

They are responsible for coordinating state changes and business operations.

---

## Directory Structure

```text id="j1s4nv"
actions/
├── chat/                    # Chat-related workflows
│   ├── send_message_action.py
│   ├── clear_chat_action.py
│   └── regenerate_message_action.py
│
├── document/                # Document-related workflows
│   ├── upload_document_action.py
│   ├── remove_document_action.py
│   └── load_document_action.py
│
├── settings/                # Settings-related workflows
│   └── change_setting_action.py
│
└── session/                 # Session-related workflows
    ├── start_session_action.py
    └── close_session_action.py
```

---

## Organization Rule

Actions are organized by business/domain topic.

```text id="j9qfuy"
Topic
    ↓
Action
```

---

## Responsibilities

* Implement application workflows.
* Read state through State Controller.
* Update state through State Controller.
* Call Gateways.
* Process workflow steps.
* Return results to Event Handlers.

---

## Typical Flow


```
                                  User Interaction generate events
                                              ↓
                                        Event Handler
                                              ↓
                                           Action
                                       ┌─────┼─────┐
                                       │     │     │
                                       ↓     ↓     ↓
                       State Controller   Gateway   State Controller
                            (read)                      (write)
                              │             │              │
                              ↓             ↓              ↓
                          State Object    Core         State Object
                          (read data)  (process)      (save result)
```

* the Action branches three ways, one after another — read
  State, call Gateway, then write State.

* Results flow back up the same branches to the Action, which then returns
  upward through Event Handler → Component Controller → UI Component → User.

---

## May Access

* State Controller
* Gateway Bundle

---

## Must Not

* Access UI Components.
* Access Component Controllers.
* Perform widget manipulation.
* Access Event Handlers.
* Contain UI logic.

---

## Design Rules

* Organize by business/domain topic.
* One action should represent one workflow.
* State changes happen through Actions.
* Core access happens through Gateways.
* UI updates are not performed by Actions.
* Actions remain independent of UI implementation.
* Only Actions may read State and call a Gateway within the same workflow step. Event Handlers and Gateways never access State directly.