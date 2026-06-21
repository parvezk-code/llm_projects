# Doc 07 — Gateways

## Purpose

- Provide a stable interface between Actions and external systems (Core today, the API client in remote mode later).
- Hide whether functionality is provided locally or remotely.
- Give Actions domain-shaped results, independent of mode.

---

## Directory Structure

```text
desktop/gateways/
├── __init__.py
├── gateway_bundle.py       # GatewayBundle — holds all gateways
├── chat_gateway.py         # ChatGateway  — wraps LLMService
└── pdf_gateway.py          # PDFGateway   — wraps PDFService
```

Only the gateways with a backing Core service exist. `settings`/`session` gateways from the original design were omitted (no backing service in this app).

---

## Implementation

- **`ChatGateway(llm_service)`**
  - `get_reply(messages: list[dict]) -> str` — forwards the provider-neutral `[{"role","content"}]` message list to `LLMService.call`.
  - Building that list (`ChatMessage → dict`) is the Action's job, not the gateway's.
- **`PDFGateway(pdf_service)`**
  - `load_document(file_path: str) -> PDFDocument` — calls `PDFService.extract_text`, derives `filename` from the path basename, and returns a fully-built `PDFDocument`.
- **`GatewayBundle`** — frozen dataclass holding `chat: ChatGateway` and `pdf: PDFGateway`.
  - Built by the launcher and passed to the Main Controller, which hands it to the Actions.

## Local vs Remote

```text
LOCAL  :  Action → Gateway → Core
REMOTE :  Action → Gateway → API Client → API Server → Core   (future)
```

The gateway interface is identical in both; only the gateway's internals change.

---

## Rules

- One gateway per business/domain topic.
- Gateways expose only the operations Actions need and hide implementation/mode details.
- Gateways may access Core (and, in remote mode, the API client) but must not access UI, controllers, Event Handlers, or State.
- Gateways contain no business logic; they delegate to Core and adapt results to domain types.
- Local and remote gateways expose the same interface so Actions never change between modes.
