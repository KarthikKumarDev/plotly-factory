"""
Filter and control components. Ids follow docs/02-CONVENTIONS.md; callback contracts in docs/07-COMPONENTS.md.
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc


def dropdown(
    options: list[dict],
    value: str | None,
    component_id: str,
    label: str = "Select",
    placeholder: str = "Choose...",
) -> dbc.Card:
    """Single-select dropdown with label. Id pattern: {page}-dropdown-{name}."""
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Label(label, html_for=component_id),
                dcc.Dropdown(
                    id=component_id,
                    options=options,
                    value=value,
                    placeholder=placeholder,
                    clearable=False,
                ),
            ]
        ),
        className="shadow-sm",
    )


def refresh_button(button_id: str, label: str = "Refresh data") -> dbc.Button:
    """Refresh button for user-triggered reload. Id pattern: {page}-refresh-btn."""
    return dbc.Button(
        label,
        id=button_id,
        color="primary",
        outline=True,
        className="me-2",
        n_clicks=0,
    )
