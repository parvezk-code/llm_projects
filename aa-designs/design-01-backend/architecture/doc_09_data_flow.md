# Data Flow

## Purpose

Describe how data moves through the system.

This document connects all architectural layers into a single flow model.

---

## Main Flow (User Action → Result)


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

## Response Flow (Result → UI Update)

```text 

Core
  ↓
Gateway
  ↓
Action
  ↓
State Controller (optional update)
  ↓
Event Handler
  ↓
Component Controller
  ↓
UI Component
  ↓
User
```

* Between Action and Event Handler, results may be Core models; from the Event
  Handler downward to the UI, only primitives or UI-local view types are
  passed. The Event Handler performs this unpacking.
  (See *Event Handlers → Core Model Translation Boundary*.)

---

## State Flow

```text id="c3q7mn"
Action
  ↓
State Controller
  ↓
State Objects
```

* State is never accessed directly by UI or Event Handlers.
* All state mutations happen inside Actions.

---

## Local Mode Flow

```text id="d7p1wa"
Action
  ↓
Gateway
  ↓
Core (local execution)
```

* Core runs in the same process.
* Gateways directly call core services.

---

## Remote Mode Flow

```text id="e5t9rk"
Action
  ↓
Gateway
  ↓
API Client
  ↓
API Server
  ↓
Core (remote execution)
```

* Core runs on a separate machine.
* Gateways abstract network communication.

---

## UI Update Flow

```text id="f2n6vc"
Event Handler
  ↓
Component Controller
  ↓
UI Component
```

* UI updates are always driven through controllers.
* Components remain passive renderers.

---

## Design Principles

* Data flows downward through architecture layers.
* Results flow upward through the same path.
* UI never accesses Core or State directly.
* UI never imports or names Core domain models; Event Handlers unpack them into primitives at the UI boundary.
* Event Handlers never access State directly.
* Actions are the only layer allowed to mutate State.
* Gateways abstract infrastructure complexity.
* Core remains independent of all upper layers.