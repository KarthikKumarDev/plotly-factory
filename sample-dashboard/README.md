# Sample Plotly dashboard

A minimal Dash app that follows the context library in `../docs/`. Use it as a reference when building new dashboards.

## What’s included

- **App entry**: `app.py` — `dcc.Location`, navbar, page-content routing.
- **Pages**: `pages/charts.py` (2×2 bar, line, scatter, pie).
- **Components**: `components/charts.py` (bar, line, scatter, pie, metric card), `components/filters.py` (dropdown, refresh button), `components/layout.py` (navbar, container).
- **Data**: `data/loaders.py` — in-memory sample data (replace with API/DB in production).
- **Theme**: `utils/theme.py` and `assets/theme.css` — light palette per docs/08-UI-ACCESSIBILITY.md.

## Run

Use one of these; **always start from the repository root** (the folder that contains the `sample-dashboard` directory).

**Option A — launcher script (recommended):**

```bash
pip install -r sample-dashboard/requirements.txt
python run_sample.py    # or: python3 run_sample.py
```

**Option B — run from sample-dashboard folder:**

```bash
cd sample-dashboard
pip install -r requirements.txt
python app.py    # or: python3 app.py
```

If you get import errors, run from the repo root using Option A, or ensure you are inside `sample-dashboard/` when running `python app.py`.

Then open http://127.0.0.1:8050/

## Conventions used

- **IDs**: `charts-bar-tl`, `charts-line-tr`, `charts-scatter-bl`, `charts-pie-br` (see docs/02-CONVENTIONS.md).
- **Routing**: Single callback on `url.pathname` → `page-content` (docs/03-ARCHITECTURE.md).
- **Charts**: Plotly Express + `apply_theme()` for paper/plot colors and colorway (docs/04-PLOTLY-GUIDE.md, 08-UI-ACCESSIBILITY.md).

## Extending

- Add a page: create `pages/<name>.py` with a `layout()` and register the path in `app.py` in `render_page_content`.
- Add a chart type: add a function in `components/charts.py` and document in docs/07-COMPONENTS.md.
- Replace sample data: implement loaders in `data/loaders.py` (API/DB/file) and add caching if needed (docs/06-DATA-PATTERNS.md).
