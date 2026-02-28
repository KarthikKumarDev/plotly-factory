# Plotly guide

Rules for Plotly APIs, chart types, theming, performance, and Dash integration. Follow these when creating or updating charts.

---

## 1. Preferred APIs

| API | Use when | Do not use when |
|-----|----------|-------------------|
| **Plotly Express (px)** | Standard charts (bar, line, scatter, box, histogram). Single data source, minimal custom config. | You need subplots, complex annotations, or fine control over every trace/layout key. |
| **graph_objects (go)** | Subplots, custom layout, multiple trace types in one figure, or when px cannot express the chart. | Simple single-trace charts that px supports (prefer px for consistency). |

**Examples:**
- **px:** `fig = px.bar(df, x="category", y="value", color="region")` then `fig.update_layout(...)` for theme.
- **go:** `fig = go.Figure(data=[go.Scatter(...)], layout=go.Layout(...))` for full control.

Use one or the other per figure; avoid mixing px and go trace construction in the same figure.

---

## 2. Common chart types

| Chart | Use case | API |
|-------|----------|-----|
| **Bar** | Comparisons across categories; counts or totals. | `px.bar` |
| **Line** | Time series; trends over a continuous x. | `px.line` |
| **Scatter** | Two continuous variables; correlation; point clouds. | `px.scatter` (or `go.Scattergl` for large data) |
| **Box / Violin** | Distributions; quartiles; outliers. | `px.box`, `px.violin` |
| **Histogram** | Single-variable distribution; bins. | `px.histogram` |
| **Pie / Donut** | Proportions of a whole (use sparingly). | `px.pie` |
| **Heatmap** | Matrix or 2D density; correlation matrices. | `px.imshow` or `go.Heatmap` |

Choose the chart that matches the message (e.g. time → line; categories → bar). Keep axes and legends readable; avoid clutter.

---

## 3. Theming

| Item | Rule |
|------|------|
| **Template** | Use `template="plotly_white"` (or a project default). Set once per figure via `fig.update_layout(template="plotly_white", ...)`. |
| **Colors** | Use a consistent color sequence (e.g. `px.colors.qualitative.Set2` or project palette). Align with [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md) for contrast. |
| **Fonts** | Set `font_family` and `font_size` in `fig.update_layout()` for title and axes if the project defines them; otherwise keep Plotly defaults. |

Apply the same template and color logic across all charts in the app so dashboards look consistent.

---

## 4. Performance

| Situation | Action | Do not |
|-----------|--------|--------|
| **Large scatter (e.g. 10k+ points)** | Use `go.Scattergl` (WebGL) or downsample (aggregate or sample) before plotting. | Use `px.scatter` or `go.Scatter` on huge point counts. |
| **Large series or many categories** | Aggregate or sample on the server before building the figure. Return a pre-aggregated DataFrame to the callback. | Send raw 100k+ rows to the browser. |
| **Large tables** | Use `dash_table.DataTable` with paging (`page_size`) and optional filtering. | Render 10k+ rows in one table without paging. |

Keep figures and payloads small enough that the UI stays responsive. Prefer server-side aggregation over client-side for big data.

---

## 5. Integration with Dash

| Rule | Action |
|------|--------|
| **Returning figures** | Return the `fig` object from the callback to `Output(..., "figure")`. Do not store large figures in `dcc.Store` or app state. |
| **Loading state** | Wrap `dcc.Graph` in `dcc.Loading` when the figure is produced by a callback (e.g. data from API or DB). Use `dcc.Loading([dcc.Graph(...)], type="default")`. |
| **IDs** | Give each `dcc.Graph` a unique `id` that follows [02-CONVENTIONS.md](02-CONVENTIONS.md) (e.g. `{page}-chart-{suffix}`). |

When updating a chart via callback, return a new figure; avoid mutating a stored figure in place.

---

Use px for standard charts; use go when you need subplots or full control. Apply one theme and color set across the app. Keep data and figures small for performance.
