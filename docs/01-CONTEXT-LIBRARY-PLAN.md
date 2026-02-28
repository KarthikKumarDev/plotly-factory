# Plotly Dashboard Context Library — Plan

This plan defines the set of markdown (and Cursor) files that form a **context library** for Plotly-based dashboards: documentation and rules that guide both humans and AI when building or modifying dashboards.

---

## 1. Overview

| Layer | Purpose |
|-------|--------|
| **Root docs** | Entry points and agent instructions (README, AGENTS.md). |
| **Context docs** | Domain knowledge: architecture, conventions, patterns, components. |
| **Cursor rules** | File-scoped AI guidance so edits follow the library (.mdc in `.cursor/rules/`). |

All paths below are relative to the project root unless noted.

**Numbering**: Doc filenames use prefixes `01`–`11` in the order they are typically used during development (plan → conventions → … → deployment). Read in order when starting from scratch; reference by number when linking.

---

## 2. Required MD Files

### 2.1 Root

**`README.md`** and **`AGENTS.md`** — see README for overview, quick start, context library index, and usage; see AGENTS.md for agent instructions.

### 2.2 Context library (in `docs/`)

See **README § Context library** for the list of docs (01–11) and their purposes. Numbered 01–11 in recommended reading order (01 is this plan); 10 and 11 are optional (troubleshooting, deployment).

---

## 3. Cursor Rules (.mdc)

Use `.cursor/rules/` so the AI applies the context library when editing relevant files.

| Rule file | Globs | Purpose |
|-----------|--------|--------|
| **`plotly-dashboards.mdc`** | `**/*.py` (or narrower, e.g. `app/**/*.py`, `pages/**/*.py`) | Apply project conventions and point to `docs/`: architecture, conventions, Plotly/Dash guides, data patterns. |
| **`dashboard-assets.mdc`** | `assets/**/*` (CSS/JS) | Conventions for styling and scripts used by Dash (e.g. no inline critical layout hacks without doc note). |

Keep each rule under ~50 lines; link to the appropriate `docs/*.md` for detail.

---

## 4. File Tree

See **README § Project structure** for the full repo layout. The context library comprises **`docs/`** (01–11) and **`.cursor/rules/`** (plotly-dashboards.mdc, dashboard-assets.mdc).

---

## 5. Implementation order

1. **README.md** and **AGENTS.md** — so the project and agents know the context library exists and where to look.
2. **docs/02-CONVENTIONS.md** — foundation for all other docs.
3. **docs/03-ARCHITECTURE.md**, **docs/04-PLOTLY-GUIDE.md**, **docs/05-DASH-GUIDE.md** — core dashboard guidance.
4. **docs/06-DATA-PATTERNS.md**, **docs/07-COMPONENTS.md**, **docs/08-UI-ACCESSIBILITY.md** — patterns and reuse.
5. **docs/09-CONTRIBUTING.md** — process for evolving the library.
6. **.cursor/rules/*.mdc** — wire rules to the docs and file patterns.
7. **docs/10-TROUBLESHOOTING.md** and **docs/11-DEPLOYMENT.md** as needed.

---

## 6. Maintenance

- When adding a new dashboard or shared component, update **07-COMPONENTS.md** (and **03-ARCHITECTURE.md** if structure changes).
- When establishing a new pattern (e.g. caching, error handling), add it to the right doc (**06-DATA-PATTERNS.md**, **05-DASH-GUIDE.md**, etc.) and reference it from **02-CONVENTIONS.md** or **AGENTS.md** if it's mandatory.
- Keep **AGENTS.md** and the `.mdc` rules in sync with new docs (e.g. new file patterns or globs).

This set of MD files and Cursor rules forms the context library that empowers and guides Plotly dashboard development.
