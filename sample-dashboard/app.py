"""
Sample Plotly Dash app. Follows docs: 02-CONVENTIONS, 03-ARCHITECTURE, 04–08.
Run: python run_sample.py (from repo root) or python app.py (from sample-dashboard/).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure sample-dashboard on path so local imports (components, pages, data, utils) resolve
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from components.layout import make_navbar, make_page_container
from pages import charts, insights

# Bootstrap theme per docs/08-UI-ACCESSIBILITY
app = Dash(
    __name__,
    use_pages=False,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                make_navbar(),
                make_page_container(html.Div(id="page-content")),
            ],
            id="theme-wrapper",
            className="theme-light",
        ),
    ]
)


@app.callback(
    Output("theme-store", "data"),
    Output("theme-wrapper", "className"),
    Input("theme-toggle", "value"),
)
def sync_theme(toggle_on: bool | None) -> tuple[str, str]:
    """Keep theme Store and wrapper class in sync. See docs/08-UI-ACCESSIBILITY.md §2."""
    theme = "dark" if toggle_on else "light"
    return theme, "theme-dark" if theme == "dark" else "theme-light"


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("theme-store", "data"),
)
def render_page_content(pathname: str | None, theme: str | None):
    """Route pathname to the correct page layout; pass theme for light/dark charts."""
    theme = theme or "light"
    if pathname is None or pathname == "/" or pathname == "" or pathname == "/charts":
        return charts.layout(theme)
    if pathname == "/insights":
        return insights.layout(theme)
    return html.Div("Not found", className="text-muted")


if __name__ == "__main__":
    app.run(debug=True, port=8050)
