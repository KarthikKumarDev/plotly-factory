"""
Layout components: navbar and page shell. See docs/07-COMPONENTS.md.
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from utils.config import DEFAULT_CHART_CONFIG


def make_theme_toggle(toggle_id: str = "theme-toggle", store_id: str = "theme-store") -> list:
    """Theme switch (light/dark) and Store. Use in navbar; wire in app callbacks."""
    return [
        dcc.Store(id=store_id, data="light"),
        html.Span("Light", className="navbar-theme-label navbar-theme-label-light"),
        dbc.Switch(id=toggle_id, value=False, className="navbar-theme-switch"),
        html.Span("Dark", className="navbar-theme-label navbar-theme-label-dark"),
    ]


def make_navbar(theme_toggle_id: str = "theme-toggle", theme_store_id: str = "theme-store") -> dbc.Navbar:
    """Navbar: modern layout with brand, nav links, and theme toggle pill."""
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    "Sample Dashboard",
                    href="/",
                    className="navbar-brand-custom",
                ),
                html.Div(
                    className="navbar-right",
                    children=[
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.NavLink("Charts", href="/", active="exact", className="nav-link-custom"),
                                ),
                                dbc.NavItem(
                                    dbc.NavLink("Insights", href="/insights", active="exact", className="nav-link-custom"),
                                ),
                                dbc.NavItem(
                                    dbc.NavLink("Config", href="/config", active="exact", className="nav-link-custom"),
                                ),
                            ],
                            navbar=True,
                            className="navbar-links",
                        ),
                        html.Div(
                            make_theme_toggle(toggle_id=theme_toggle_id, store_id=theme_store_id),
                            className="navbar-theme-pill",
                        ),
                    ],
                ),
            ],
            fluid=True,
            className="navbar-container",
        ),
        className="dashboard-navbar",
        dark=True,
    )


def make_config_panel() -> html.Div:
    """Config toggles panel; always in layout so sync_config callback has valid Inputs. Shown only on /config via style."""
    cfg = DEFAULT_CHART_CONFIG
    return html.Div(
        id="config-panel",
        children=[
            dbc.Card(
                [
                    dbc.CardHeader("Chart behavior", className="fw-bold"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Show legend", html_for="config-show-legend", className="mb-0"), md=8),
                                    dbc.Col(
                                        dbc.Switch(id="config-show-legend", value=cfg.get("show_legend", True), className="mb-2"),
                                        md=4,
                                        className="d-flex align-items-center justify-content-end",
                                    ),
                                ],
                                className="mb-2 align-items-center",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Show chart titles", html_for="config-show-titles", className="mb-0"), md=8),
                                    dbc.Col(
                                        dbc.Switch(id="config-show-titles", value=cfg.get("show_titles", True), className="mb-2"),
                                        md=4,
                                        className="d-flex align-items-center justify-content-end",
                                    ),
                                ],
                                className="mb-2 align-items-center",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Show data labels on charts", html_for="config-show-data-labels", className="mb-0"), md=8),
                                    dbc.Col(
                                        dbc.Switch(id="config-show-data-labels", value=cfg.get("show_data_labels", True), className="mb-2"),
                                        md=4,
                                        className="d-flex align-items-center justify-content-end",
                                    ),
                                ],
                                className="mb-2 align-items-center",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Show grid lines", html_for="config-show-grid", className="mb-0"), md=8),
                                    dbc.Col(
                                        dbc.Switch(id="config-show-grid", value=cfg.get("show_grid", True), className="mb-2"),
                                        md=4,
                                        className="d-flex align-items-center justify-content-end",
                                    ),
                                ],
                                className="mb-2 align-items-center",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Show chart toolbar", html_for="config-show-modebar", className="mb-0"), md=8),
                                    dbc.Col(
                                        dbc.Switch(id="config-show-modebar", value=cfg.get("show_modebar", True), className="mb-2"),
                                        md=4,
                                        className="d-flex align-items-center justify-content-end",
                                    ),
                                ],
                                className="align-items-center",
                            ),
                        ]
                    ),
                ],
                className="shadow-sm mt-3",
            ),
        ],
        style={"display": "none"},
    )


def make_page_container(children: list) -> dbc.Container:
    """Page content container with consistent padding. Uses same gutter as navbar for alignment."""
    return dbc.Container(children, fluid=True, className="py-3 main-content-container")
