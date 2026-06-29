# Part X — Asynchronous Operations

Some operations (loading a project, building an index, calling an external API,
reading large files, or performing other long-running work) can take noticeable
time. Running these operations on the main UI thread would freeze the interface.
To keep the application responsive, long-running work is executed on a background
thread.

## Responsibilities

1. **Threading is an Event Handler responsibility.** Actions, Gateways, Core
   Workflows, and Core Services remain completely synchronous.
2. The Event Handler decides **whether** an operation should run on a background
   thread. Fast operations run directly; slow operations use a Worker.
3. An Action must never create threads, start workers, or manage concurrency.
   It simply performs its work from start to finish and either returns a result
   or raises an exception.
4. A Worker executes one synchronous method on a background thread and delivers
   either the returned result or the raised exception back to the main thread.
5. All UI updates happen **only on the main thread** after the Worker completes.
   Background threads never update widgets or controllers directly.
6. Event Handlers must keep a reference to each running Worker until it finishes,
   otherwise the Worker may be garbage collected while still running.
7. Workers are infrastructure only. They contain no business logic, no state
   management, and no UI logic.

## Runtime Infrastructure

Concurrency support belongs to the application's runtime infrastructure rather
than to the Event Handler layer.

Create a dedicated folder under `desktop/` to hold reusable concurrency
utilities.

```text
desktop/
├── state/
├── state_controller/
├── gateways/
├── actions/
├── action_bundles/
├── event_handlers/
├── concurrency/
│   ├── worker.py
│   ├── worker_pool.py        # optional future extension
│   └── __init__.py
└── main_controller.py
```

The `concurrency/` folder contains only infrastructure for executing work in the
background. It contains no business logic, no UI code, and no application
workflow logic.

Event Handlers use these utilities, but they do not own them.

## Typical Flow

For a long-running operation:

```text
User Event
    │
    ▼
Event Handler
    │
    ├── update temporary UI state (busy indicator)
    ├── create Worker
    └── start Worker
             │
             ▼
      Background Thread
             │
             ▼
     synchronous Action
             │
             ▼
          Gateway
             │
             ▼
      Core Workflow
             │
             ▼
      Core Services
             │
             ▼
 return result or raise exception
             │
             ▼
 Worker delivers result/error
             │
             ▼
       Main UI Thread
             │
             ├── update controllers
             ├── show success/error
             └── clear busy state
```

## Error Handling

1. Actions report failures by **raising exceptions**.
2. The Worker catches any exception raised on the background thread.
3. The Worker delivers the exception back to the Event Handler on the main thread.
4. The Event Handler decides how the error should be presented to the user.
5. The Worker never displays errors or performs recovery.

## Busy State

Long-running operations should temporarily indicate that the application is busy.

Typical sequence:

```text
clear previous errors
        │
        ▼
set_busy(true)
        │
        ▼
start Worker
        │
        ▼
(wait)
        │
        ▼
on_result / on_error
        │
        ▼
set_busy(false)
```

Busy indicators are temporary UI state and are **not** considered part of the
"one method per event" rule.

## Worker Design Rules

A Worker should remain a small infrastructure utility.

A Worker should:

* execute one synchronous callable on a background thread,
* capture either the returned result or the raised exception,
* deliver that outcome back to the main thread.

A Worker should **not**:

* contain business logic,
* modify application state,
* call controllers,
* update widgets,
* decide how errors are displayed,
* coordinate application workflows.

## Design Principle

The application's business logic always remains synchronous.

```text
Event Handler
        │
        ▼
 Worker (optional)
        │
        ▼
      Action
        │
        ▼
     Gateway
        │
        ▼
  Core Workflow
        │
        ▼
  Core Services
```

Threading is purely an application-level concern managed by the Event Handler.
Removing or replacing the Worker implementation (for example, using a thread
pool instead of individual threads) should never require changes to Actions,
Gateways, Core Workflows, or Core Services.
