# LangGraph Notes

# What is LangGraph

LangGraph is used to build workflow based AI applications.

A LangGraph consists of:

- State
- Nodes
- Edges
- Execution flow

Graphs execute step by step through connected nodes.

---

# Basic Workflow

```text
START → Node → Node → END
```

Example:

```text
START → process_input → generate_response → END
```

---

# State

State is shared automatically across all nodes.

State stores data during graph execution.

State is usually defined using:

- TypedDict
- State schema class

---

# State Syntax

## TypedDict Syntax

```python
class State(TypedDict):
    key_name: data_type
```

## Example

```python
from typing import TypedDict

class State(TypedDict):
    message: str
    result: str
```

---

# Nodes

Nodes are functions.

Each node receives the current state.

Nodes return dictionaries that update state values.

---

# Node Syntax

## Basic Syntax

```python
def node_name(state: State):

    return {
        "key": value
    }
```

## Example

```python
def process_message(state: State):

    text = state["message"]

    return {
        "result": text.upper()
    }
```

---

# Edges

Edges connect nodes together.

Edges define graph execution flow.

LangGraph provides:

- START
- END

START connects to the first node.

The last node connects to END.

---

# Edge Syntax

## Basic Edge Syntax

```python
builder.add_edge(source_node, target_node)
```

## Example

```python
builder.add_edge(START, "process")
builder.add_edge("process", END)
```

---

# Graph Builder

Graphs are created using `StateGraph`.

---

# Graph Builder Syntax

## Basic Syntax

```python
builder = StateGraph(State)
```

## Example

```python
from langgraph.graph import StateGraph

builder = StateGraph(State)
```

---

# Adding Nodes

Nodes are added using `add_node()`.

---

# add_node Syntax

## Basic Syntax

```python
builder.add_node("node_name", node_function)
```

## Example

```python
builder.add_node("process", process_message)
```

---

# Adding Edges

Edges are added using `add_edge()`.

---

# add_edge Syntax

## Basic Syntax

```python
builder.add_edge("source", "target")
```

## Example

```python
builder.add_edge(START, "process")
builder.add_edge("process", END)
```

---

# Compiling Graphs

Graphs must be compiled before execution.

---

# compile Syntax

## Basic Syntax

```python
graph = builder.compile()
```

---

# Executing Graphs

Execution starts only after:

- invoke()
- ainvoke()
- stream()

---

# invoke Syntax

## Synchronous Execution

```python
result = graph.invoke(initial_state)
```

## Example

```python
result = graph.invoke({
    "message": "hello",
    "result": ""
})
```

---

# ainvoke Syntax

## Asynchronous Execution

```python
result = await graph.ainvoke(initial_state)
```

## Example

```python
result = await graph.ainvoke({
    "message": "hello",
    "result": ""
})
```

---

# Creating a Basic Graph

This example demonstrates a simple graph with one node.

---

# Simple Graph Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str
    result: str


def process_message(state: State):

    text = state["message"]

    return {
        "result": text.upper()
    }


builder = StateGraph(State)

builder.add_node(
    "process",
    process_message
)

builder.add_edge(
    START,
    "process"
)

builder.add_edge(
    "process",
    END
)

graph = builder.compile()

result = graph.invoke({
    "message": "hello world",
    "result": ""
})

print(result)
```

---

# Graph Execution Flow

```text
START
   ↓
process
   ↓
END
```

---

# Multi Node Graph Example

This example demonstrates multiple connected nodes.

---

# Multi Node Graph Code

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str
    upper_text: str
    final_text: str


def convert_upper(state: State):

    return {
        "upper_text": state["message"].upper()
    }


def add_prefix(state: State):

    return {
        "final_text": f"Output: {state['upper_text']}"
    }


builder = StateGraph(State)

builder.add_node(
    "upper",
    convert_upper
)

builder.add_node(
    "prefix",
    add_prefix
)

builder.add_edge(
    START,
    "upper"
)

builder.add_edge(
    "upper",
    "prefix"
)

builder.add_edge(
    "prefix",
    END
)

graph = builder.compile()

result = graph.invoke({
    "message": "hello",
    "upper_text": "",
    "final_text": ""
})

print(result)
```

---

# Multi Node Graph Flow

```text
START
   ↓
upper
   ↓
prefix
   ↓
END
```

---

# Conditional Routing

Conditional routing allows graphs to choose different paths.

Router functions decide the next node.

Router functions receive state as input.

Router functions return:

- Node names
- Path keys
- Lists depending on configuration

---

# Router Function Syntax

## Basic Syntax

```python
def router(state: State):

    return "node_name"
```

## Example

```python
def router(state: State):

    if state["role"] == "admin":
        return "admin"

    return "user"
```

---

# add_conditional_edges Syntax

## Basic Syntax

```python
builder.add_conditional_edges(
    node_name,
    router_function
)
```

## Example

```python
builder.add_conditional_edges(
    "check_role",
    router
)
```

---

# Conditional Graph Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    role: str
    result: str


def check_role(state: State):
    return {}


def admin_node(state: State):

    return {
        "result": "Admin Access"
    }


def user_node(state: State):

    return {
        "result": "User Access"
    }


def router(state: State):

    if state["role"] == "admin":
        return "admin"

    return "user"


builder = StateGraph(State)

builder.add_node(
    "check_role",
    check_role
)

builder.add_node(
    "admin",
    admin_node
)

builder.add_node(
    "user",
    user_node
)

builder.add_edge(
    START,
    "check_role"
)

builder.add_conditional_edges(
    "check_role",
    router
)

builder.add_edge(
    "admin",
    END
)

builder.add_edge(
    "user",
    END
)

graph = builder.compile()

result = graph.invoke({
    "role": "admin",
    "result": ""
})

print(result)
```

---

# Conditional Graph Flow

```text
                 → admin → END
START → check_role
                 → user  → END
```

---

# Important Points

- State is shared automatically.
- Nodes update state using dictionaries.
- Graphs execute through edges.
- START and END are predefined constants.
- Graphs must be compiled before execution.
- Router functions control conditional execution.
- invoke() runs synchronously.
- ainvoke() runs asynchronously.
