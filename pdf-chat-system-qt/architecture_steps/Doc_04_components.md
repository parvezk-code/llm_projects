# Chat PDF App — Requirements Document

A Python desktop application that lets a user upload a PDF file and have a conversational Q&A session with its contents, powered by the OpenAI API.

---

```
┌─────────────────────────────────────────┐
│              ToolbarComponent           │  ← Region 1
├─────────────────────────────────────────┤
│              StatusBarComponent         │  ← Region 2 (conditional)
├─────────────────────────────────────────┤
│                                         │
│              ChatAreaComponent          │  ← Region 3
│                                         │
├─────────────────────────────────────────┤
│              InputBarComponent          │  ← Region 4
└─────────────────────────────────────────┘
```

---

### Summary Table

| Component | Widgets | Conditional? |
|---|---|---|
| `ToolbarComponent` | Button, Label, Button | Always visible |
| `StatusBarComponent` | Icon, Label, Button | Only on PDF load error |
| `ChatAreaComponent` | ScrollArea, Bubbles, Spinner, Placeholder | Always visible, content varies |
| `InputBarComponent` | TextInput, Button | Always visible, enabled/disabled |

---

### 01 `ToolbarComponent` (2 buttons and 1 label)

| Screen State | Behavior |
|---|---|
| No PDF loaded | Filename label shows "No PDF loaded" · Clear button disabled |
| PDF loaded | label shows `filename` · Clear button enabled |

---

### 02 `StatusBarComponent` (Warning icon, Error label, Dismiss(×) button)

| Screen State | Behavior |
|---|---|
| No error | Entire bar hidden |
| PDF load error | Bar visible with red/orange error text and dismiss button |

> Only appears in **Screen 2b** (PDF load error). Hidden in all other states.

---

### 03 `ChatAreaComponent` 

**Widgets inside:** Scrollable container · User message bubbles · AI message bubbles · Loading indicator (`• • •`) · Empty state placeholder (icon + text)

| Screen State | Behavior |
|---|---|
| No PDF loaded | Shows centered placeholder icon + "Upload a PDF to start chatting" |
| PDF loaded, no messages | Empty scrollable area |
| Active conversation | Scrollable bubble list (user right, AI left) |
| Waiting for AI | `• • •` loading bubble shown at bottom left |
| API error | Red error bubble inline in chat stream |

---

### 04 `InputBarComponent` (Text input field, Send button)

| Screen State | Behavior |
|---|---|
| No PDF loaded | Input disabled · Send button disabled/greyed |
| PDF loaded | Input active · Send button active |
| Waiting for AI response | Both disabled during API call (blocking) |

---

