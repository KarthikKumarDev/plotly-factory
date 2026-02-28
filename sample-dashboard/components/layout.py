"""
Layout components: navbar and page shell. See docs/07-COMPONENTS.md.
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html


def make_navbar() -> dbc.Navbar:
    """Navbar with app title and links to pages."""
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Sample Dashboard", href="/", className="ms-2"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Charts", href="/", active="exact")),
                        dbc.NavItem(dbc.NavLink("Insights", href="/insights", active="exact")),
                    ],
                    navbar=True,
                    className="ms-auto",
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-3",
    )


def make_page_container(children: list) -> dbc.Container:
    """Page content container with consistent padding."""
    return dbc.Container(children, fluid=True, className="py-3")
