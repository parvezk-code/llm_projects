# Core — Services & Models Design Rules

App-specific rules for the Core layer: business logic and domain data that stay
independent of UI, application flow, state, and infrastructure, and run unchanged in
local or remote mode.

---

## Part A — Domain Model Rules

Models are passive domain data — the vocabulary the whole app shares.

1. **Frozen and immutable.** Every model is a `@dataclass(frozen=True)`. A change
   means a new instance. This makes models safe to pass across layers and store in
   state.

2. **Data only — no workflow, no serialisation.** A model holds fields and nothing
   else. No `to_dict()`, no provider shaping, no business steps. Transport shaping
   belongs in the action.

3. **Factory constructors for clean call sites.** Provide `@classmethod` factories
   (`ChatMessage.user(content)`, `ChatMessage.assistant(content)`,
   `ProjectIndex.create(...)`) so callers read clearly and construction stays in one
   place.

4. **Constants classes for shared string literals.** Domain string literals live in
   one place (`Role.USER`, `Role.ASSISTANT`) rather than being scattered as raw
   strings across actions and services.

5. **Opaque handles are allowed but typed `Any` and never inspected outside Core.**
   A model may wrap a third-party object (`ProjectIndex.store` holding a FAISS store)
   as an opaque handle. Only the Core service that created it ever inspects it;
   everything above treats it as passive data.

6. **No upward or sideways imports.** Models import nothing from UI, State, Actions,
   Gateways, or launchers. They are the bottom of the dependency graph.

---

## Part B — Core Service Rules

Services perform single, well-scoped business operations and own all third-party
library specifics.

1. **One service, one well-scoped capability.** A service does one job
   (`PlainChatService` generates, `FaissVectorStoreService` builds/searches,
   `CodeExecutor` runs code). Organise by capability under `core/services/<area>/`.

2. **Own the provider/library specifics.** All third-party SDK usage (OpenAI,
   LangChain, FAISS, PyMuPDF, subprocess) is confined to Core services. Nothing
   outside Core imports those libraries.

3. **Build their own provider clients from primitives.** A service takes config
   primitives (`api_key`, `model`, `temperature`, `max_tokens`) and constructs its
   own client internally. The launcher passes primitives, not pre-built provider
   objects — so the provider never leaks into the launcher.

4. **Accept pre-shaped input; return plain values or domain models.** A service
   receives input already shaped by the action (a `list[dict]` message list, a built
   message history) and returns a plain value or a domain model. It does not reach
   back into state or shape transport itself.

5. **No workflow orchestration.** Services apply business rules and operations; they
   do not sequence multi-step application workflows (that is the action's job) and do
   not decide *when* they run.

6. **Independent of all upper layers.** A service must not access UI, State, Actions,
   Gateways, or launcher code. It is callable identically in local and remote mode.

7. **Tools follow the simplest form that works.** Agent tools are module-level
   `@tool` functions; a helper with real logic (e.g. `CodeExecutor`) is a plain class
   with its constants inline. Tools are assembled into a `list[BaseTool]` in the
   launcher and injected into the agent service.

---

## Why this split

- **Models** are a shared, immutable vocabulary safe to pass anywhere.
- **Services** quarantine every provider/library detail in one layer, so swapping a
  provider or going remote touches Core only.
- Because services build their own clients from primitives and take pre-shaped input,
  the launcher stays provider-free and the action keeps ownership of shaping — each
  layer holds exactly its own concern.

# Core — Services & Models Design Rules