# Troubleshooting

Common issues, causes, and fixes for Dash/Plotly dashboards. Use this when callbacks, layout, data, or deployment misbehave. Patterns: [05-DASH-GUIDE.md](05-DASH-GUIDE.md), [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md), [11-DEPLOYMENT.md](11-DEPLOYMENT.md).

---

## 1. Callbacks

### Callback not firing

| Check | Action |
|-------|--------|
| **Ids match** | Every `Input`/`Output`/`State` id must match the component `id` in the layout exactly (case-sensitive). Search the codebase for the id string; fix typos. |
| **prevent_initial_call** | If you expect the callback to run on load but it doesn’t, set `prevent_initial_call=False` (or remove it). If it runs on load and shouldn’t, set `prevent_initial_call=True`. |
| **Browser console** | Open dev tools (F12) → Console. Look for JavaScript errors or Dash callback errors. Fix the reported issue. |

### Duplicate callback outputs

| Rule | Action |
|------|--------|
| **One callback per Output** | Each `Output(id, property)` may be targeted by only one callback. If two callbacks update the same output, combine them (one callback, multiple Inputs) or split the output (e.g. two different components). |
| **Reference** | See [05-DASH-GUIDE.md](05-DASH-GUIDE.md) §2–3 and Dash docs on duplicate outputs. |

### Callback order / circular dependency

| Check | Action |
|-------|--------|
| **Detect** | A → B → A: Output of callback 1 is Input of callback 2, and callback 2’s output is Input of callback 1. Trace the callback graph. |
| **Break cycle** | Use `State` instead of `Input` for values that should not trigger a callback. Or use `dcc.Store`: one callback writes to Store, another reads from Store and updates the UI. See [03-ARCHITECTURE.md](03-ARCHITECTURE.md) §7. |

---

## 2. Layout and IDs

### Component not found / ID typos

| Check | Action |
|-------|--------|
| **Exact match** | Ids are case-sensitive. Layout and callback must use the same string (e.g. `"sales-chart-main"` everywhere). |
| **Dynamic ids** | If you use pattern-matched or dynamic ids, use `dash.callback` with `pattern_match` or document the approach in the module. Prefer static ids from [02-CONVENTIONS.md](02-CONVENTIONS.md) when possible. |

### Layout flash or flicker

| Cause | Fix |
|-------|-----|
| **Figure cleared then set** | Avoid returning an empty figure and then updating; return the final figure in one callback return. Or use `dcc.Loading` around the graph so the transition is masked. |
| **No initial data** | Provide initial content or use `dcc.Store` for data so the first render isn’t empty. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §6. |

---

## 3. Data

### Stale or missing data

| Check | Action |
|-------|--------|
| **Cache** | If data is stale, check cache TTL and invalidation. Shorten TTL or add a refresh button. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §4–5. |
| **Network/API** | If data is missing, check callback error handling. Add try/except, timeout, and user-visible error message. Log the exception. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §2. |

### Large payload / slow response

| Cause | Fix |
|-------|-----|
| **Store too big** | Do not put 100k+ rows in `dcc.Store`. Aggregate or sample on the server; return only what’s needed for the view. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §6. |
| **Chart overload** | Use WebGL (`go.Scattergl`) or downsample for large scatter/line data. See [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md) §4. |

---

## 4. Deployment and environment

| Issue | Check | Action |
|-------|--------|-------|
| **App won’t run** | Port, host, command | See [11-DEPLOYMENT.md](11-DEPLOYMENT.md). Run with the documented command (e.g. `python app.py` or `dash run`). Check port is free. |
| **Missing config** | Env vars | Ensure required env vars are set (e.g. API key, base URL). No hardcoded secrets. Document in [11-DEPLOYMENT.md](11-DEPLOYMENT.md). |
| **Wrong base URL** | API or links | Base URL must match environment (dev vs prod). Use config or env; do not hardcode. |

---

## 5. Getting help

- **Dash/Plotly:** [Dash Forum](https://community.plotly.com/c/dash/16), [Plotly community](https://community.plotly.com/).
- **This project:** Document recurring issues and fixes in this doc. If your team has an internal channel or issue tracker, link it here.

---

When a callback doesn’t fire, check ids and `prevent_initial_call`. When data is wrong, check cache and error handling. When the app won’t run, check [11-DEPLOYMENT.md](11-DEPLOYMENT.md) and env vars.
