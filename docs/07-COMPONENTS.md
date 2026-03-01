# Components

Rules for reusable building blocks: standard charts, control sets, and layout templates. Follow these so dashboards stay consistent. Chart APIs: [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md). IDs and naming: [02-CONVENTIONS.md](02-CONVENTIONS.md).

---

## 1. Standard charts

Reuse these patterns so chart style and behavior are consistent. Implement in `components/charts.py` (or equivalent); each returns a Plotly figure or a `dcc.Graph` with a standard id pattern.

| Component | Purpose | Id pattern | Notes |
|-----------|---------|------------|--------|
| **Bar chart** | Category comparisons; counts/totals | `{page}-bar-{suffix}` | Use `px.bar`; apply theme from [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md). |
| **Line chart** | Time series; trends | `{page}-line-{suffix}` | Use `px.line`; same theme. |
| **Scatter chart** | Two continuous variables; point clouds | `{page}-scatter-{suffix}` | Use `px.scatter` or `go.Scattergl` for large data. |
| **Metric card** | Single KPI (number + label) | `{page}-metric-{suffix}` | `dbc.Card` with title and value; optional sparkline. |

Use the same template and colorway for all charts (see [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md)). Pass `id` and data (e.g. DataFrame or aggregated dict) into the component; return `dcc.Graph` or the figure.

---

## 2. Control sets

Filters and controls used across pages. Define in `components/filters.py` (or equivalent). IDs must follow [02-CONVENTIONS.md](02-CONVENTIONS.md); document the callback contract (which Inputs/Outputs use these ids).

| Component | Purpose | Id pattern | Callback contract |
|-----------|---------|------------|-------------------|
| **Dropdown (single)** | Single selection (e.g. region, category) | `{page}-dropdown-{name}` | `Output`: options; `Input`: value. Callback updates dependent Store or figures. |
| **Dropdown (multi)** | Multi-select filter | `{page}-dropdown-multi-{name}` | Same; value is list. |
| **Date range picker** | Start/end date filter | `{page}-date-range` | `dcc.DatePickerRange`; `Input(..., "start_date")`, `Input(..., "end_date")`. |
| **Refresh button** | User-triggered data reload | `{page}-refresh-btn` | `Input(..., "n_clicks")` triggers reload; see [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §5. |
| **Theme toggle** | Light/dark theme switch | `theme-toggle` (switch), `theme-store` (Store) | Switch updates Store and wrapper class (`theme-light` / `theme-dark`); use distinct label classes (e.g. `navbar-theme-label-light`, `navbar-theme-label-dark`) and CSS `:has(.form-check-input:checked)` so the active label is bold and visible in both themes. See [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md) §2 Theme switch. |

When adding a control, add a row here with id pattern and how callbacks use it (Input/Output/State).

---

## 3. Layout templates

| Template | Use for | Implementation |
|----------|---------|----------------|
| **Page shell** | Consistent outer structure (navbar + content) | Function in `components/layout.py` that returns `dbc.Container` with navbar + `html.Div(id="page-content")` or equivalent. Reuse on every page. |
| **Cards / panels** | Metric blocks, chart containers | `dbc.Card` with `dbc.CardHeader` and `dbc.CardBody`. Use spacing and colors from [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md). |
| **Grid** | Aligning charts and cards | `dbc.Row` and `dbc.Col`; use consistent breakpoints (e.g. `md=6` for half width). Same gutter/padding across pages. |

Document any layout constants (e.g. column sizes, spacing classes) in this doc or in [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md) §3.

---

## 4. Where components live

| Type | Location | Rule |
|------|----------|------|
| **Charts** | `components/charts.py` | Functions that return figures or `dcc.Graph`; accept `id`, data, and optional layout overrides. |
| **Filters / controls** | `components/filters.py` | Functions that return `dcc` or `dbc` control components; accept `id` and optional props. |
| **Layout** | `components/layout.py` | Functions that return page shell, card wrappers, or grid helpers. |
| **Assets** | `assets/` | Shared CSS (e.g. `theme.css`), JS for clientside behavior. No component logic in assets; only styling and scripts. |

Keep one module per concern (charts, filters, layout). Import from `components.*` in pages or app layout.

---

## 5. Adding a new component

1. **Implement** in the right module (`components/charts.py`, `filters.py`, or `layout.py`) with a clear signature (e.g. `def bar_chart(id: str, df: pd.DataFrame, x: str, y: str, **kwargs) -> dcc.Graph`).
2. **Document** in this doc: add a row to the relevant table (§1, §2, or §3) with component name, purpose, id pattern, and callback contract or notes.
3. **Conventions** — Use ids and naming from [02-CONVENTIONS.md](02-CONVENTIONS.md). If the component is shared across apps, note it in [03-ARCHITECTURE.md](03-ARCHITECTURE.md) or `shared/`. See [09-CONTRIBUTING.md](09-CONTRIBUTING.md) for the full process.

---

Use the same chart and layout patterns everywhere; document every new component in the tables above and keep ids consistent.
