# Doc 09 — Data Flow

## Purpose

- Describe how data moves through the system and connect all layers into one model.

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
 ↓ (returns Core model result)
Event Handler (unpacks model → primitives)
 ↓
Component Controller
 ↓
UI Component
 ↓
User
```

- An Action reads State, calls a Gateway, then writes State.
- Results flow back up; the Event Handler converts Core models to primitives before the UI sees them.

---

## State Flow

```text
Action → State Controller → State Object
```

- Only Actions mutate state. UI and Event Handlers never touch state directly.

---

## Local Mode Flow

```text
Action → Gateway → Core (same process)
```

- Gateways call Core services directly. (Remote mode would insert API Client → API Server before Core; not implemented.)

---

## Config Flow

```text
conf/env/.env* → pydantic Settings (ConfigBundle) → Launcher → LLMService/Gateways
```

- The launcher loads config and builds the Gateways from it. Config never reaches UI, Actions, or Core models.

---

## Theme Flow

```text
Toolbar theme_changed(filename) → ToolbarEventHandler.on_theme_changed → StyleManager.apply_theme → QApplication.setStyleSheet
```

- The default theme is applied once at startup by the Main Controller.

---

## UI Update Flow

```text
Event Handler → Component Controller → UI Component
```

- UI updates always go through controllers; components remain passive renderers.

---

## Error Flow

```text
Action raises → Event Handler catches →
  chat/LLM failure  → ChatArea error bubble
  PDF-load failure  → Status-bar banner
```

---

## Rules

- Data flows downward through the layers; results flow back up the same path.
- UI never accesses Core or State directly; Event Handlers never access State directly.
- Actions are the only layer that mutates State.
- Gateways abstract infrastructure and mode; Core stays independent of all upper layers.
- Config is loaded by the launcher only and flows down through the Gateways it builds.
