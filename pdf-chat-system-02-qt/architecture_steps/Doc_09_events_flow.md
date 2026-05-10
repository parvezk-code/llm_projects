
## ⚡ User Events


## Generic Event Flow

1. **Capture user event**
2. **Collect required input**
3. **Validate input**
4. **Run domain operation**
5. **Convert domain result into state data**
6. **Update store/state**
7. **Decide affected UI sections**
8. **Render affected components**
9. **Show status/result**

---

> Event-01 : upload_pdf_requested

Trigger: User clicks **Upload PDF** button.

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Update UI | Open native file picker filtered to `.pdf` files | — |

---
<br>

> Event-02 : pdf_loaded

Method: load_new_doc()

Trigger: User selects a valid `.pdf` file from the file picker.

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Read Data | Read file path returned by event | — |
| 2 | Parse PDF | Extract full text from PDF file | PDFService |
|   | On Error  | pdf_load_failed | PDFService |
| 3 | Update State | Store PDF info (filename, text, no of pages) | AppState |
| 4 | Update State | Clear chat history | AppState |
| 5 | Update State | Clear errors | AppState |
| 6 | Update UI | Render PDF details | Toolbar |
| 7 | Update UI | Render chat history (empty) | ChatArea |
| 8 | Update UI | Dismiss any previous error | StatusBar |
| 9 | Update UI | Enable question input | InputBar |

---
<br>

> Event-03 : status_bar_dismissed

Method: remove_status_bar()

Trigger: User clicks × on the error status bar.

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Update State | Clear error from state | AppState |
| 2 | Update UI | Hide error banner | StatusBar |

---
<br>

> Event-04 : message_send_requested

Method: invokeLLM(), addNewMessage()

Trigger: User clicks Send button or presses Enter in the input field.

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Read Data     | Read question text                        | InputBar |
|   | On Error      | `empty_query_submitted`                   |    —     |
| 2 | Create Obj    | Create `ChatMessage` with role: user, content: input text | — |
| 3 | Update State  | Set is_loading to True                    | AppState |
| 4 | Update UI     | Show loading indicator                    | ChatArea |
| 5 | Update UI     | Disable input and Send button             | InputBar |
| 6 | Invoke LLM    | Send question, text, chat histroy         | LLMService |
|   | On Error      | `api_call_failed`                         |    —     |
| 7 | Create Obj    | Create `ChatMessage` with role: assistant, content: response | — |
| 8 | Update State  | Append user message to chat history       | AppState |
| 9 | Update State  | Append assistant message to chat history  | AppState |
|10 | Update State  | Set is_loading to False                   | AppState |
|11 | Update UI     | Hide loading indicator                    | ChatArea |
|12 | Update UI     | Render user message bubble                | ChatArea |
|13 | Update UI     | Render assistant message bubble           | ChatArea |
|14 | Update UI     | Enable input and Send button              | InputBar |
|15 | Update UI     | Clear input field                         | InputBar |

---
<br>

> Event-05 : chat_cleared

Method: clear_chat_history()

Trigger: User clicks the Clear button in the toolbar.

|No | Label         | Description                   | Target   |
|---|---|---|---|
| 1 | Update State  | Clear chat history            | AppState |
| 2 | Update State  | Clear errors                  | AppState |
| 3 | Update UI     | Remove all message bubbles    | ChatArea |
| 4 | Update UI     | Hide error banner             | StatusBar |

---


## ❗ System / Internal Reactions

> Error-01 : pdf_load_failed

Method: handlePDFLoadError()

Trigger: Selected file fails to parse (corrupt or password-protected).

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Update State  | Store error (str:message)                     | AppState |
| 2 | Update UI     | Show error banner with message                | StatusBar|
| 3 | Update UI     | Keep question input disabled                  | InputBar |

---
<br>

> Error-02 : api_call_failed

Method: handleLLMCallError()

Trigger: OpenAI API call raises an exception (network error, timeout, invalid key).

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Update State  | Store error (str:message)                     | AppState |
| 2 | Update State  | Set is_loading to False                       | AppState |
| 3 | Update UI     | Hide loading indicator                        | ChatArea |
| 4 | Update UI     | Render red error bubble with message          | ChatArea |
| 5 | Update UI     | Enable input and Send button                  | InputBar |

---
<br>

> Error-03 : empty_query_submitted

Trigger: User attempts to send an empty input field.

| No | Label | Description | Target |
|---|---|---|---|
| 1 | Update State  | Store error (str:message)                     | AppState |
| 2 | Update UI     | Render inline red error bubble with message   | ChatArea |


## 🔄 state change reactions

> we do not use State-driven event updates
---


---