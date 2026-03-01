"""
Layout components: navbar and page shell. See docs/07-COMPONENTS.md.
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html


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
        className="dashboard-navbar mb-4",
        dark=True,
    )


def make_page_container(children: list) -> dbc.Container:
    """Page content container with consistent padding."""
    return dbc.Container(children, fluid=True, className="py-3")
