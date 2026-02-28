# Conventions

Rules for naming, layout, and style. Follow these when creating or editing dashboard code.

---

## 1. Component IDs

| Rule | Value |
|------|--------|
| **Pattern** | `{page}-{component}-{suffix}` |
| **Chars** | Lowercase letters, digits, hyphens only. No spaces, no underscores. |
| **Uniqueness** | One `id` per component in the app. Never reuse an id. |

**Valid:** `sales-chart-main`, `filters-date-range`, `overview-metrics-cards`  
**Invalid:** `SalesChart`, `filters_date_range`, `chart 1`

When adding a component, choose an id that matches the pattern. If the component is shared across pages, use a logical page name (e.g. `shared-` or the primary page).

---

## 2. Files and modules

| Kind | Location | Rule |
|------|----------|------|
| Main app | `app.py` (root) | Single entry for related dashboards. |
| Page | `pages/<name>.py` | One file per route; `<name>` = route or page name (e.g. `analytics.py`, `overview.py`). |
| Reusable UI | `components/<name>.py` | Charts, filters, layout helpers (e.g. `charts.py`, `filters.py`). |
| Data | `data/<name>.py` | Loaders, data utilities (e.g. `loaders.py`). |
| Helpers | `utils/<name>.py` | Config, cache, shared helpers (e.g. `cache.py`, `config.py`). |
| Unrelated app | `apps/<dashboard_name>/` | Own `app.py`, `pages/`, `assets/`; see [03-ARCHITECTURE.md](03-ARCHITECTURE.md). |

Do not put dashboard pages in the root; use `pages/`. Do not put shared UI in `pages/`; use `components/`.

---

## 3. Callbacks and variables

- **Callback names:** Verb + object, e.g. `update_chart`, `sync_filters`, `render_page_content`. One callback per logical update; name after what it does.
- **DataFrames:** Use `df` for the primary DataFrame in scope. Use descriptive names for derived or cached data: `filtered_df`, `cached_sales`, `agg_by_region`.
- **No** single-letter names except `df` in short blocks.

---

## 4. Project layout (summary)

Full tree: **README § Project structure**.

- Root: `app.py`, `requirements.txt`, `README.md`, `AGENTS.md`
- Related app: `pages/`, `assets/`, `components/`, `data/`, `utils/`
- Unrelated apps: `apps/<name>/` (each with its own `app.py`, `pages/`, `assets/`)
- Shared code: `shared/` (optional)
- Docs: `docs/` (01–11), `.cursor/rules/`

---

## 5. Code style

| Item | Rule |
|------|------|
| **Format** | Black, line length 88. Run `black .` before commit. |
| **Lint** | Ruff. Run `ruff check .`; fix all reported issues. |
| **Imports** | Order: stdlib → third-party → local. Blank line between groups. No `from x import *`. |
| **Docstrings** | Required for: (1) every callback registered with `@app.callback`, (2) data loaders and transform functions. One line is enough unless logic is non-obvious. |
| **Types** | Add type hints to callbacks and data loaders when straightforward (e.g. `def update_chart(region: str, df: pd.DataFrame) -> go.Figure`). Not required for trivial helpers. |

---

## 6. Commands

- Format: `black .`
- Lint: `ruff check .`
- CI: run both; merge only when they pass.

---

When in doubt, match existing files in the repo and keep IDs unique.
