"""
Config page: control panel to toggle chart behaviors (legends, titles, data labels, grid).
Toggles live in a persistent panel (components/layout.make_config_panel) so the sync_config callback
always has valid Inputs; this page shows the heading and the panel is revealed below via app callback.
"""
from __future__ import annotations

from dash import html


def layout(theme: str = "light", config: dict | None = None) -> html.Div:  # noqa: ARG001
    """Config page: intro text; actual toggles are in the persistent config-panel (shown when pathname=/config).
    theme and config are accepted to match the shared layout() signature used by render_page_content.
    """
    return html.Div(
        [
            html.H1("Config", className="mb-3"),
            html.P(
                "Toggle the options below to change how charts behave on the Charts and Insights pages.",
                className="text-muted mb-2",
            ),
        ]
    )
