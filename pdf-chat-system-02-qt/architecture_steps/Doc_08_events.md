# Step 08 — User Events

---

| # | Event Name | Trigger | Component that emits |
|---|---|---|---|
| E-01 | `pdf_upload_requested` | User clicks **Upload PDF** button | `ToolbarComponent` |
| E-02 | `pdf_loaded` | File picker closes with a valid `.pdf` file selected | `ToolbarComponent` |`ToolbarComponent` |
| E-03 | `status_bar_dismissed` | User clicks **×** on the error status bar | `StatusBarComponent` |
| E-04 | `message_send_requested` | User clicks **Send** button | `InputBarComponent` |
| -    | `message_send_requested` | User presses **Enter** key in input field | `InputBarComponent` |
| E-05 | `chat_cleared` | User clicks **Clear** button | `ToolbarComponent` |

---

| # | Error Name | Trigger | 
|---|---|---|
| E-01 | `pdf_load_failed`       | Selected file fails to parse (corrupt / password-protected) |
| E-01 | `api_call_failed`       | LLM call failed |  
| E-01 | `empty_query_submitted` | used submited empty question for llm to answer |  

## Notes

| Note | Detail |
|---|---|
| E-04          | Event triggered by two triggers. Both map to the same handler in `MainController`. |
| E-02 and E-03 | These are outcomes of E-01. The file picker is opened by E-01; success → E-02, failure → E-03. |
| No E for API response | API call is blocking on main thread (NFR-01). No async event needed — response arrives inline. |
| No E for scroll | Scrolling is internal UI behavior managed by `ChatAreaController`. Not a user event. |
