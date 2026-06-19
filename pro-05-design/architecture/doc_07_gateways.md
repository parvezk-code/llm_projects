# Gateways

## Purpose

Provide a stable interface between Actions and external systems.

Gateways hide whether functionality is provided locally or remotely.

---

## Directory Structure

```text id="w8m3tk"
gateways/
├── gateway_bundle.py       # Collection of all gateways
├── chat_gateway.py         # Chat operations
├── pdf_gateway.py          # Document operations
├── settings_gateway.py     # Settings operations
└── session_gateway.py      # Session operations
```

---

## Organization Rule

Gateways are organized by business/domain topic.

```text id="72xgda"
Topic
    ↓
Gateway
```

---

## Responsibilities

* Expose operations needed by Actions.
* Hide implementation details.
* Hide local/remote differences.
* Delegate work to underlying services.
* Provide a stable interface.

---

## Typical Flow

```text id="wzht1j"
Action
    ↓
Gateway
    ↓
Core
```

or

```text id="vjzv1h"
Action
    ↓
Gateway
    ↓
API Client
    ↓
API Server
    ↓
Core
```

---

## Gateway Bundle

### Purpose

Provide a single object containing all gateways.

### Example

```text id="t2o7zw"
Gateway Bundle
├── Chat Gateway
├── PDF Gateway
├── Settings Gateway
└── Session Gateway
```

---

## May Access

* Core
* API Client

---

## Must Not

* Access UI.
* Access Component Controllers.
* Access Event Handlers.
* Access State directly.
* Contain business logic.

---

## Design Rules

* One gateway per business/domain topic.
* Actions access external functionality through gateways.
* Gateways hide infrastructure details.
* Local and remote modes should expose the same gateway interface.
* UI remains unaware of gateway implementations.
