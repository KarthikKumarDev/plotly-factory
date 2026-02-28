# Dash guide

Rules for Dash components, callbacks, and integration. Follow these when building or editing dashboard UI and logic.

---

## 1. Components

| Library | Use for | Examples |
|---------|--------|----------|
| **dcc** | Data-driven and core UI | `dcc.Graph`, `dcc.Dropdown`, `dcc.DatePickerRange`, `dcc.Store`, `dcc.Location`, `dcc.Link`, `dcc.Loading`, `dcc.Tabs`, `dash_table.DataTable` |
| **dbc** | Layout and structure | `dbc.Container`, `dbc.Row`, `dbc.Col`, `dbc.Navbar`, `dbc.Card`, `dbc.Modal`, `dbc.Button` |

- **Custom / reusable:** See [07-COMPONENTS.md](07-COMPONENTS.md) for project-specific components. Use `id` per [02-CONVENTIONS.md](02-CONVENTIONS.md).

---

## 2. Callback signature and registration

| Rule | Action |
|------|--------|
| **Decorator** | `@app.callback(Output(...), [Input(...), ...], [State(...), ...])`. List Output(s) first, then Input(s), then State(s). |
| **Multiple outputs** | List all `Output(id, property)` in order; return a tuple in the **same order** (one value per Output). |
| **prevent_initial_call** | Set `prevent_initial_call=True` when the callback must **not** run on initial page load (e.g. only on button click or dropdown change). Default is `False` (runs on load). |

**Example:** `@app.callback(Output("graph", "figure"), Input("dropdown", "value"), State("store", "data"), prevent_initial_call=False)`

---

## 3. Input, Output, State

| Type | Role | Use when |
|------|------|----------|
| **Output** | Component property the callback **writes** to. | Updating a graph’s figure, a div’s children, a dropdown’s options. |
| **Input** | Component property that **triggers** the callback when it changes. | User action (click, select, date change) or another callback’s output. |
| **State** | Component property **read** when the callback runs but does **not** trigger it. | Extra context (e.g. current filters, Store data) that the callback needs but should not fire on. |

- **Rule:** Every callback has at least one Output and at least one Input. State is optional.
- **No duplicate outputs:** No Output may be targeted by more than one callback. See [03-ARCHITECTURE.md](03-ARCHITECTURE.md).

---

## 4. Return values

| Situation | Return | Do not |
|------------|--------|--------|
| **Update this output** | The value for that Output (e.g. a figure, a list of options, `children`). | — |
| **Leave this output unchanged** | `dash.no_update` for that output. In multi-output callbacks, return a tuple with `no_update` in the slot for the output you want to skip. | Mutate the component in place or return None to “skip” (use `no_update`). |
| **Cancel all updates** | `raise dash.exceptions.PreventUpdate` (no output is updated). | Use for “do nothing” when no Input change should trigger a visible update. |

**Example (multi-output):** `return (new_figure, dash.no_update)` — first Output updated, second unchanged.

---

## 5. Clientside callbacks

| Rule | Detail |
|------|--------|
| **When to use** | Simple UI sync that does not need server data (e.g. toggle visibility, local state). Prefer server callbacks when you need data, DB, or API. |
| **Where** | Define in `assets/` as JS, or use `ClientsideFunction(namespace, function_name)` with JS in `assets/`. |
| **Limitation** | No access to server-side data, secrets, or Python. Use for pure front-end behavior only. |

Document in the module or in this doc when a callback is clientside and why.

---

## 6. Best practices

| Topic | Rule |
|-------|------|
| **ID consistency** | Every `id` in the layout must match the `id` used in callback `Input`/`Output`/`State`. Typos cause silent failures. Follow [02-CONVENTIONS.md](02-CONVENTIONS.md) for id format. |
| **Circular dependencies** | Avoid: Output A → Input B → Output A. Break cycles with `dcc.Store` or by restructuring. See [03-ARCHITECTURE.md](03-ARCHITECTURE.md). |
| **Long-running callbacks** | If a callback may run >30s, use `dash.long_callback` (or background jobs) and show loading state. Document the pattern in this doc or in the app. |
| **Error handling** | Catch exceptions in callbacks; return a user-visible message (e.g. error div or toast) or `no_update` and log the error. Do not let uncaught exceptions break the app. |
| **Data refresh** | For data refresh, use a button or `dcc.Interval` that triggers a callback to reload data. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) for refresh configuration and user-triggered refresh patterns. |

---

Register callbacks with correct Output/Input/State order; return tuples for multiple outputs; use `no_update` to skip an output. Keep IDs consistent and avoid circular dependencies.
