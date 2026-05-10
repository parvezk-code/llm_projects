

### Diagram 1: UIComposer creates UIBundle for MainController

```

+------------------------+                         +------------------------+
|                        |       UIBundle          |                        |
|       UIComposer       | ----------------------> |     MainController     |
|                        |                         |                        |
+------------------------+                         +------------------------+

                    UIBundle = all application controllers

```



### Diagram 2: ServiceComposer creates ServiceBundle for MainController


```

+------------------------+                         +------------------------+
|                        |      ServiceBundle      |                        |
|    ServiceComposer     | ----------------------> |     MainController     |
|                        |                         |                        |
+------------------------+                         +------------------------+

                    ServiceBundle = all service controllers

```



### Diagram 3: PDF loading flow

```
+------------------+     1. file_path     +-----------------+    2. file_path    +--------------+
|                  | -------------------> |                 |------------------->|              |
|  MainController  |                      |  PDFController  |                    |  PDFService  |
|                  | <------------------- |                 |<-------------------|              |
+------------------+    4. PDFDocument    +-----------------+    3. text(str)    +--------------+

```

### Diagram 4: Display uploaded PDF name in Toolbar


```

+--------------------+                  +--------------------+                 +------------------+
|                    |   PDFDocument    |                    |   file_name     |                  |
|   MainController   |----------------->| ToolbarController  |---------------->| ToolbarComponent |
|                    |                  |                    |                 |                  |
+--------------------+                  +--------------------+                 +------------------+

```

### Diagram 5: LLM transaction flow

```

+------------------+  1. LLMTransaction   +------------------+  2. raw request fields +---------------+
|                  | -------------------> |                  | ---------------------> |               |
|  MainController  |                      |  LLMController   |                        |  LLMService   |
|                  | <------------------- |                  | <--------------------- |               |
+------------------+  4. LLMTransaction   +------------------+     3. raw response    +---------------+

                        raw request fields = pdf_text + history + user_message

```

### Diagram 6: Render user and assistant messages in ChatArea

```

+------------------+  1. user ChatMessage     +---------------------+   2. chat data   +-------------------+
|                  | -----------------------> |                     | ---------------> |                   |
|  MainController  |                          | ChatAreaController  |                  | ChatAreaComponent |
|                  | -----------------------> |                     | ---------------> |                   |
+------------------+ 3. assistant ChatMessage +---------------------+   4. chat data   +-------------------+

                                        chat data = (role, content)

```



### Diagram 7: PDF load error reaches MainController

```

+------------------------+                                   +------------------------+
|                        |   raises PDFLoadError(message)    |                        |
|     PDFController      | --------------------------------> |     MainController     |
|                        |                                   |                        |
+------------------------+                                   +------------------------+


```

### Diagram 8: Display PDF load error in StatusBar


```

+------------------+                     +-----------------------+                    +--------------------+
|                  |   error_msg(str)    |                       |   error_msg(str)   |                    |
|  MainController  | ------------------> |  StatusBarController  | -----------------> | StatusBarComponent |
|                  |                     |                       |                    |                    |
+------------------+                     +-----------------------+                    +--------------------+

```



### Diagram 9: LLM call error reaches MainController


```

+------------------------+                                   +------------------------+
|                        |   raises LLMCallError(message)    |                        |
|     LLMController      | --------------------------------> |     MainController     |
|                        |                                   |                        |
+------------------------+                                   +------------------------+

```


### Diagram 10: Display LLM call error in StatusBar


```

+------------------+                   +---------------------+                   +--------------------+
|                  |  error_msg(str)   |                     |  error_msg(str)   |                    |
|  MainController  |------------------>| ChatAreaController  |------------------>| ChatAreaComponent  |
|                  |                   |                     |                   |                    |
+------------------+                   +---------------------+                   +--------------------+

```