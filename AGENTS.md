# Agent instructions — Plotly Factory

This project builds **Plotly-based dashboards** (Dash). When working on dashboard code or related assets, follow the context library below.

## Project type

- **Stack**: Plotly, Dash (and optionally Dash Bootstrap Components, Dash Enterprise).
- **Language**: Python for app logic; HTML/CSS/JS in `assets/` when needed.

## Where conventions live

- **Architecture & patterns**: Read `docs/03-ARCHITECTURE.md`, `docs/04-PLOTLY-GUIDE.md`, `docs/05-DASH-GUIDE.md`, `docs/06-DATA-PATTERNS.md`.
- **Naming, layout, style**: Read `docs/02-CONVENTIONS.md`.
- **Reusable pieces**: Read `docs/07-COMPONENTS.md`.
- **UI and accessibility**: Read `docs/08-UI-ACCESSIBILITY.md`.

When adding or changing dashboards, follow these docs and update them if you introduce new patterns.

## Commands

<!-- Fill in actual commands for this repo -->

- **Run app**: _TBD_ (e.g. `python app.py` or `dash run`)
- **Tests**: _TBD_ (e.g. `pytest`)
- **Lint/format**: _TBD_ (e.g. `ruff check .`, `black .`)

## Working on dashboards

1. Before editing dashboard Python or layout logic, read the relevant `docs/` files above.
2. Use existing components and patterns from `docs/07-COMPONENTS.md` and `docs/06-DATA-PATTERNS.md` where applicable.
3. Keep callback IDs and component IDs consistent with `docs/02-CONVENTIONS.md`.
4. After adding a new reusable component or pattern, document it in `docs/07-COMPONENTS.md` (and related docs) and update `docs/09-CONTRIBUTING.md` if the process changes.
