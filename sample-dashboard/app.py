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

from components.layout import make_config_panel, make_navbar, make_page_container
from pages import charts, config as config_page, insights
from utils.config import DEFAULT_CHART_CONFIG

# Bootstrap theme per docs/08-UI-ACCESSIBILITY
app = Dash(
    __name__,
    use_pages=False,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="config-store", data=DEFAULT_CHART_CONFIG),
        html.Div(
            [
                make_navbar(),
                make_page_container([
                    html.Div(id="page-content"),
                    make_config_panel(),
                ]),
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
    Output("config-store", "data"),
    Input("config-show-legend", "value"),
    Input("config-show-titles", "value"),
    Input("config-show-data-labels", "value"),
    Input("config-show-grid", "value"),
    Input("config-show-modebar", "value"),
)
def sync_config(
    show_legend: bool | None,
    show_titles: bool | None,
    show_data_labels: bool | None,
    show_grid: bool | None,
    show_modebar: bool | None,
) -> dict:
    """Sync config page toggles to config-store. Runs when user is on Config page."""
    return {
        "show_legend": bool(show_legend) if show_legend is not None else True,
        "show_titles": bool(show_titles) if show_titles is not None else True,
        "show_data_labels": bool(show_data_labels) if show_data_labels is not None else True,
        "show_grid": bool(show_grid) if show_grid is not None else True,
        "show_modebar": bool(show_modebar) if show_modebar is not None else True,
    }


@app.callback(
    Output("config-panel", "style"),
    Input("url", "pathname"),
)
def toggle_config_panel_visibility(pathname: str | None) -> dict:
    """Show config panel only on /config so config toggles are always in DOM for sync_config callback."""
    if pathname == "/config":
        return {"display": "block"}
    return {"display": "none"}


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("theme-store", "data"),
    Input("config-store", "data"),
)
def render_page_content(pathname: str | None, theme: str | None, chart_config: dict | None):
    """Route pathname to the correct page layout; pass theme and chart config."""
    theme = theme or "light"
    config = chart_config if isinstance(chart_config, dict) else DEFAULT_CHART_CONFIG
    if pathname in (None, "", "/", "/charts"):
        return charts.layout(theme, config)
    if pathname == "/insights":
        return insights.layout(theme, config)
    if pathname == "/config":
        return config_page.layout(theme, config)
    return html.Div("Not found", className="text-muted")


if __name__ == "__main__":
    app.run(debug=True, port=8050)
