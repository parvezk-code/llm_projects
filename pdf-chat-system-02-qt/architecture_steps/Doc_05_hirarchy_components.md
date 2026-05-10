

## 📂 Project Structure

```
MainWindow  (QMainWindow — top-level shell, no logic)
│
├── ToolbarComponent                        [SMART]
│   ├── upload_btn                          [QPushButton]
│   ├── filename_label                      [QLabel]
│   └── clear_btn                           [QPushButton]
│
├── StatusBarComponent                      [SMART]  ← hidden by default
│   ├── warning_icon                        [QLabel  — icon]
│   ├── error_message_label                 [QLabel  — text]
│   └── dismiss_btn                         [QPushButton  — "×"]
│
├── ChatAreaComponent                       [SMART]
│   ├── scroll_area                         [QScrollArea]
│   │   └── scroll_content_widget           [QWidget  — container]
│   │       ├── PlaceholderWidget           [DUMB]  ← shown when no PDF
│   │       │   ├── icon_label              [QLabel  — PDF icon]
│   │       │   └── hint_label              [QLabel  — "Upload a PDF..."]
│   │       ├── MessageBubbleWidget × N     [DUMB]  ← one per message
│   │       │   └── bubble_label            [QLabel  — message text]
│   │       └── LoadingBubbleWidget         [DUMB]  ← shown during API call
│   │           └── dots_label              [QLabel  — "• • •"]
│   └── (layout manages bubble stacking)    [QVBoxLayout]
│
└── InputBarComponent                       [SMART]
    ├── message_input                       [QLineEdit / QTextEdit]
    └── send_btn                            [QPushButton]

```