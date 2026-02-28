# Contributing

Rules for adding or changing dashboards. For **updating the context library** (docs and patterns), see [README § Updating the context library](../README.md#updating-the-context-library-docs). Conventions: [02-CONVENTIONS.md](02-CONVENTIONS.md). Architecture: [03-ARCHITECTURE.md](03-ARCHITECTURE.md).

---

## 1. Adding a new dashboard (or page)

| Step | Action |
|------|--------|
| 1 | **Create** — Related: `pages/<name>.py` and register route in main app. Unrelated: `apps/<name>/` with own `app.py`, optional `pages/`, `assets/`. See [03-ARCHITECTURE.md](03-ARCHITECTURE.md). |
| 2 | **Register** — If multi-page, add route so `pathname` maps to the new page layout in the main app callback. |
| 3 | **Follow** — Ids and layout per [02-CONVENTIONS.md](02-CONVENTIONS.md). Reuse components from [07-COMPONENTS.md](07-COMPONENTS.md). |
| 4 | **Document** — New reusable component or pattern → add row in [07-COMPONENTS.md](07-COMPONENTS.md). Structure change → update [03-ARCHITECTURE.md](03-ARCHITECTURE.md). |
| 5 | **Verify** — Run `ruff check .` and `black .`. Fix failures before merge. |

**Do not** add related pages under `apps/`. **Do not** skip documenting new components in 07-COMPONENTS.

---

## 2. Changing an existing dashboard

| Rule | Action |
|------|--------|
| **Ids** | Keep format per [02-CONVENTIONS.md](02-CONVENTIONS.md). If you change an id, update every callback that references it. No broken callback contracts. |
| **New ids** | Document in the module or in 02-CONVENTIONS if they define a new pattern. |
| **Components** | New or changed reusable component → add or update row in [07-COMPONENTS.md](07-COMPONENTS.md) (name, purpose, id pattern, callback contract). |

---

## 3. Process checklist

Before merge:

- [ ] Code follows [02-CONVENTIONS.md](02-CONVENTIONS.md) (ids, layout, style)
- [ ] New/changed components in [07-COMPONENTS.md](07-COMPONENTS.md)
- [ ] New data or callback patterns in [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) or [05-DASH-GUIDE.md](05-DASH-GUIDE.md)
- [ ] [AGENTS.md](../AGENTS.md) and `.cursor/rules/*.mdc` updated if agent contract changed
- [ ] `ruff check .` and `black .` pass

---

## 4. Checklist before you ship

Before releasing or deploying a dashboard, verify:

- [ ] All visuals follow the documented theme and hierarchy ([04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md), [08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md)).
- [ ] Loading states and feedback are in place for slow or user-triggered updates ([05-DASH-GUIDE.md](05-DASH-GUIDE.md)).
- [ ] Navigation and purpose of each view are clear ([03-ARCHITECTURE.md](03-ARCHITECTURE.md), [07-COMPONENTS.md](07-COMPONENTS.md)).
- [ ] Accessibility basics are met: contrast, labels, titles ([08-UI-ACCESSIBILITY.md](08-UI-ACCESSIBILITY.md)).
- [ ] New components or patterns are documented in the context library (this doc, [07-COMPONENTS.md](07-COMPONENTS.md)).
- [ ] Run, test, and deploy steps are documented ([README](../README.md), [11-DEPLOYMENT.md](11-DEPLOYMENT.md)).

---

Add in the right place (pages/ or apps/); document components and patterns; when changing docs or conventions, follow [README § Updating the context library](../README.md#updating-the-context-library-docs).
