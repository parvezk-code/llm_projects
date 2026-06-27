# Action & Action Bundle — Design Rules

App-specific rules for how actions implement workflows and coordinate state and
gateways. These pair with the state-controller and event-handler rules: the action
is the orchestrator *below* the handler, and it calls **one event-shaped method**
on the StateController rather than a sequence of field writes.

---

## Part A — Action Rules

An action is one application workflow. It reads/writes state (via the StateController)
and reaches external systems (via Gateways), and returns a result to the handler.

1. **One action = one workflow.** Each action represents a single user-facing
   workflow and exposes exactly one `execute(...)`. Organise actions by domain topic
   (`actions/chat/`, `actions/project/`).

2. **No mode branching inside an action.** There is no `if mode ==` in any action.
   Mode routing is the handler's job; each action is a single clean path
   (`SendPlainMessageAction`, `SendRagMessageAction`, `SendAgentMessageAction`).

3. **Constructed with `(state_controller, gateways)`.** An action receives only the
   StateController and the GatewayBundle. Nothing else — no UI, no controllers, no
   handlers, no Core imports beyond domain models.

4. **The only layer that touches State and Gateways.** Actions are the sole readers
   and writers of state (through the StateController) and the sole callers of
   Gateways. Handlers and UI never do either.

5. **Transport shaping lives here.** Converting domain data into provider/transport
   form (`ChatMessage → dict`, `list[Chunk] → context string`,
   `ChatMessage → LangChain message`) happens in the action — never in the model,
   the gateway, or the Core service.

6. **Call one event-shaped StateController method, not many setters.** When a
   workflow's state change spans several fields, the action calls a single
   intent-named StateController method (`reset_on_clear_chat()`), mirroring the
   handler/controller rule. The action decides *when*; the StateController owns *how*.

7. **Atomic commit on success only.** Set the processing flag, do the external call,
   and commit state **only after** the call succeeds — so a failure leaves state
   unchanged. Reset the processing flag in `finally`.

   ```python
   def execute(self, user_text: str) -> tuple[ChatMessage, ChatMessage]:
       self._state.set_processing(True)
       try:
           messages = self._build_messages(self._state.get_chat_messages(), user_text)
           reply = self._gateways.chat.get_reply(messages)        # external call first
           user_msg = ChatMessage.user(user_text)
           assistant_msg = ChatMessage.assistant(reply)
           self._state.add_chat_message(user_msg)                 # commit only on success
           self._state.add_chat_message(assistant_msg)
           return user_msg, assistant_msg
       finally:
           self._state.set_processing(False)
   ```

8. **Return domain models, not primitives.** An action returns domain models (or a
   tuple of them) to the handler. The handler unpacks to primitives. An action never
   returns widget-ready strings or formats for display.

9. **Synchronous and UI-agnostic.** Actions never touch widgets, never decide
   threading, never format for display. Threading is the handler's concern; the
   action is a plain synchronous call.

10. **Raise on failure; leave state consistent.** Actions raise rather than returning
    an error object. Before raising, ensure no partial commit remains. The handler
    catches and routes the error.

---

## Part B — Action Bundle Rules

1. **One frozen bundle holds all actions.** A single `ActionBundle`
   (`@dataclass(frozen=True)`) carries every action, built by the MainController and
   injected into handlers.

2. **Fields named by workflow.** Bundle fields are the workflow verbs
   (`send_plain`, `send_rag`, `send_agent`, `clear_chat`, `load_project`), so a
   handler call reads as `self._actions.send_rag.execute(...)`.

3. **The bundle holds actions only — no logic.** It is a passive container. It never
   decides which action runs (the handler's router does) and contains no methods.

4. **Grows per level, never branches.** New capabilities add a new single-purpose
   action and a new bundle field; existing actions are never extended with mode
   conditionals.

---

## Why this split

- Each action is one clean workflow with one external call and one atomic commit.
- The action calls **one event-shaped StateController method**, so the "what state
  changes for this workflow" lives in exactly one place — consistent with the
  handler/controller one-method-per-event rule.
- The bundle keeps wiring trivial: build once, inject once, call by name.

# Action & Action Bundle — Design Rules