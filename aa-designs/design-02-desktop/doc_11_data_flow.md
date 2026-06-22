# Doc 11 — Data Flow (Generic)

## Purpose

- Describe how data moves through the layers and connect them into one model.

---

## Main Flow (user action → result)

```text
User
 ↓
UI Component (emits signal)
 ↓
Event Handler
 ↓
Action ──→ State Controller (read)  ──→ State Object
       ──→ Gateway ──→ Core (process)
       ──→ State Controller (write) ──→ State Object
 ↓ (returns domain result)
Event Handler (unpacks model → primitives)
 ↓
Component Controller
 ↓
UI Component
 ↓
User
```

## State Flow

```text
Action → State Controller → State Object
```

Only Actions mutate state.

## Local vs Remote

```text
LOCAL  : Action → Gateway → Core (same process)
REMOTE : Action → Gateway → API Client → API Server → Core
```

## Config Flow

```text
.env files → typed Settings (bundle) → Launcher → Gateways / Core services
```

## UI Update Flow

```text
Event Handler → Component Controller → UI Component
```

## Error Flow

```text
Action raises → Event Handler catches → appropriate UI error surface
```

---

## Rules

- Data flows downward; results flow back up the same path.
- UI never accesses Core or State directly; Event Handlers never access State directly.
- Actions are the only layer that mutates State.
- Gateways abstract infrastructure and mode; Core stays independent of all upper layers.
- Config is loaded by the launcher only and flows down through the Gateways it builds.
