

## Domain Models

### `PDFDocument`

| Field | Type | Description |
|---|---|---|
| `filename` | `str` | Display name e.g. `annual_report_2024.pdf` |
| `full_text` | `str` | Full extracted text sent as system context |

---

### `ChatMessage`

| Field | Type | Description |
|---|---|---|
| `role` | `str` | `"user"` or `"assistant"` |
| `content` | `str` | Message text |

---

### `LLMTransaction`

| Field | Type | Description |
|---|---|---|
| `pdf_text`        | `str`                 | Full extracted PDF text sent as system context |
| `history`         | `list[ChatMessage]`   | Conversation history so far (excludes new user message) |
| `user_message`    | `ChatMessage`         | The new user message to be sent |
| `response`        | `ChatMessage`         | Reply sent by LLM |

---

## State Models

### `AppState`

| Field | Type | Description |
|---|---|---|
| `pdf` | `PDFDocument \| None` | `None` = no PDF loaded |
| `messages` | `list[ChatMessage]` | Full conversation history (in-memory) |
| `is_loading` | `bool` | `True` while waiting for API response |
| `error` | `str` | Current active error, or `None` |

---

### Removed following : AppError, AppState.error and ErrorKind.

> Errors are just strings passed directly to component controllers. No model required.
> Currently all errors are written but never read back.

01. `AppError`

| Field | Type | Description |
|---|---|---|
| `kind` | `ErrorKind` | `PDF_LOAD` or `API_FAILURE` or `EMPTY_QUERY` |
| `message` | `str` | Human-readable error text shown in UI |

---

02. `ErrorKind` (Enum)

| Value | Display Location | Description |
|---|---|---|
| `PDF_LOAD` | `StatusBarComponent` banner | Shown when PDF fails to load |
| `API_FAILURE` | `ChatAreaComponent` inline red bubble | Shown when OpenAI API call fails |
| `EMPTY_QUERY` | `ChatAreaComponent` inline red bubble | Shown when user sends empty message |
