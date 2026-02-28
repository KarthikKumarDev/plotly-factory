# Architecture

Rules for layout, callbacks, routing, and how **related** vs **unrelated** dashboards are created, stored, linked, and deployed. Follow these when adding or changing dashboard structure.

---

## 1. Related vs unrelated — decision

| Type | Meaning | When to use |
|------|--------|-------------|
| **Related** | Same app, same process, shared navbar/theme/data. Multiple pages, one deployable. | New view or page that shares navigation and theme with existing app. |
| **Unrelated** | Standalone app, own process, own URL. Deployable separately. | New product or dashboard that does not share navigation with the main app. |

**Rule:** Decide before coding. Related → add under main app. Unrelated → add under `apps/<name>/`.

---

## 2. Where to create and store

| Type | Create | Store | Entry point |
|------|--------|--------|-------------|
| **Related** | New page/route in existing app | `pages/<name>.py`; layout in main `app` | Root `app.py` (single entry) |
| **Unrelated** | New app in its own folder | `apps/<dashboard_name>/` with own `app.py`, `pages/`, `assets/` | `apps/<name>/app.py` |

- **Related:** One codebase, one process. Register the route in the main app. Share `assets/`, navbar, theme. Do **not** put related pages under `apps/`.
- **Unrelated:** One folder per app. Each has its own `app.py`, `assets/`, optional `pages/`. No shared `dcc.Location` or navbar with other apps. May import from `shared/` but must not depend on another app’s `app` or routes.

---

## 3. Folder layout (unrelated apps)

Each unrelated app is self-contained so it can be deployed alone:

```
apps/<name>/
├── app.py           # Entry point for this app only
├── pages/           # Optional: multi-page inside this app
├── assets/
└── requirements.txt # Optional: app-specific deps

shared/              # Optional: code shared across apps/
├── components/
├── data/
└── theme/
```

- Deploy: one process or image per `apps/<name>/`. Document in [11-DEPLOYMENT.md](11-DEPLOYMENT.md).
- Shared code: in `shared/`; unrelated apps may import it. Do not put unrelated apps inside another app’s folder.

---

## 4. Linking

| From → To | How | Do not |
|-----------|-----|--------|
| **Related page → related page** | `dcc.Link(..., href="/path")` with path from your routing | Full URLs; links to unrelated apps |
| **Unrelated app → unrelated app** | External link only (hub, bookmark, or portal). Use full URL from config/env | In-app `dcc.Link` between apps |
| **Cross-link to unrelated app** | Full URL (base URL from config/env + path). No hardcoded hosts | Hardcoded domains or ports |

Routing applies **per app**. Unrelated dashboards have separate URLs; they do not share routing.

---

## 5. Deployment (unrelated)

- **Run:** `python apps/<name>/app.py` (or equivalent). One process per app.
- **Docker:** One image per app, or one Dockerfile with build arg for app name.
- **Config:** Each app may have its own env (e.g. `apps/<name>/.env`). Document in [11-DEPLOYMENT.md](11-DEPLOYMENT.md).

---

## 6. Layout (single app)

- **Root layout:** `dcc.Location(id="url")` + container (e.g. `dbc.Container`) with navbar + `html.Div(id="page-content")`. Page content is swapped by a callback on `url.pathname`.
- **Page content:** One callback: `Input("url", "pathname")` → `Output("page-content", "children")`. Return the layout for the current path (e.g. from `pages/<name>.py`).
- **Structure:** Use a grid (e.g. `dbc.Row`, `dbc.Col`) and consistent padding. Document any layout constants in this doc or in [07-COMPONENTS.md](07-COMPONENTS.md).

---

## 7. Callbacks

| Rule | Action |
|------|--------|
| **Inputs → Outputs** | Each callback: one or more `Output`; one or more `Input` (and optionally `State`). No output is the target of more than one callback. |
| **State** | Use `State` for values needed in the callback that must **not** trigger it (e.g. current filters). Use `Input` for triggers (e.g. button click, dropdown change). |
| **prevent_initial_call** | Set `prevent_initial_call=True` when the callback must not run on initial page load (e.g. only on user action). Document in the callback or here if non-obvious. |
| **Circular deps** | Avoid: Output A → Input B → Output A. If needed, document and use a single source of truth (e.g. `dcc.Store`) to break the cycle. |

---

## 8. URL routing (multi-page)

- **Scope:** Routing is per app. Unrelated apps have separate pathnames and do not share routing.
- **Mechanism:** `dcc.Location(id="url")`; callback reads `pathname` and returns the correct layout for `page-content`. Map path to module (e.g. `/analytics` → layout from `pages.analytics`).
- **Links:** Use `dcc.Link(children=..., href="/path")`. Use paths, not full URLs, for same-app navigation.

---

## 9. Assets and config

| Item | Rule |
|------|------|
| **Assets** | `assets/` at app root (or inside `apps/<name>/` for unrelated). CSS/JS/images loaded automatically by Dash. |
| **Config / env** | Use a config module or `.env` for API base URLs, feature flags, secrets. No hardcoded URLs or secrets. Document in [11-DEPLOYMENT.md](11-DEPLOYMENT.md) which env vars each app needs. |

---

When adding a dashboard: (1) Choose related or unrelated. (2) Create in the right place (pages/ or apps/). (3) Use the linking and routing rules above.
