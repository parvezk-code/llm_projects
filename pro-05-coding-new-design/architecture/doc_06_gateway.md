# Gateway & Gateway Bundle — Design Rules

App-specific rules for how gateways sit between actions and external systems, hiding
local-vs-remote mode and keeping Core swappable. The gateway is a thin delegating
boundary — it adds no logic of its own.

---

## Part A — Gateway Rules

A gateway is the stable interface an action calls to reach an external system. It
delegates to a Core service (local) or an API client (remote) and returns
domain-shaped results.

1. **One gateway per external concern.** Group by capability:
   `ChatGateway` (plain + RAG generation), `IndexGateway` (build + retrieve),
   `AgentGateway` (tool-using agent). Create a gateway only where a backing
   capability exists — never an empty placeholder.

2. **Thin: delegate and adapt only.** A gateway contains no business logic, no
   workflow, no transport shaping. It receives already-shaped input from the action,
   calls the Core service, and returns the result (a domain model or plain value).

3. **Receives pre-shaped data from the action.** The action shapes domain data into
   provider/transport form before calling. The gateway passes that through; it does
   not build prompts, convert models, or assemble context.

4. **Returns domain-shaped results.** A gateway returns domain models (or plain
   values), never raw provider responses. This keeps actions independent of provider
   detail and of mode.

5. **Hides local-vs-remote mode.** The same gateway interface works whether the
   backing call is in-process Core (local) or an API client (remote). Actions never
   change between modes; only the gateway's internals differ.

   ```
   LOCAL  : Action → Gateway → Core service
   REMOTE : Action → Gateway → API client → API server → Core
   ```

6. **Exposes only what actions need.** Method names are action-facing verbs
   (`get_reply`, `get_rag_reply`, `get_agent_reply`, `build_index`, `retrieve`).
   No internal/provider methods leak through.

7. **Touches Core (or the API client) only.** A gateway must not access UI,
   controllers, handlers, or State. Its only collaborators are the Core services (or
   remote client) it wraps.

8. **Built by the launcher, never self-constructing.** A gateway is constructed in
   the launcher with its Core service(s) injected. It does not build its own
   services, read config, or decide mode.

---

## Part B — Gateway Bundle Rules

1. **One frozen bundle holds all gateways.** A single `GatewayBundle`
   (`@dataclass(frozen=True)`) carries every gateway, built by the launcher and
   passed to the MainController, which forwards it to actions.

2. **Fields named by concern.** Bundle fields are the concern names (`chat`, `index`,
   `agent`), so an action call reads as `self._gateways.index.retrieve(...)`.

3. **The bundle holds gateways only — no logic.** A passive container with no methods
   and no decisions.

4. **The bundle is the mode boundary.** The launcher builds the bundle for its mode
   (local now, remote later) and hands it up. Nothing above the bundle knows or asks
   which mode produced it.

---

## Why this split

- Gateways keep actions provider-agnostic and mode-agnostic: an action calls
  `get_rag_reply` the same way regardless of where the model runs.
- Because shaping lives in the action and logic lives in Core, the gateway stays a
  one-line delegator — the easiest layer to swap when going remote.
- The bundle makes mode a single decision point in the launcher.

# Gateway & Gateway Bundle — Design Rules