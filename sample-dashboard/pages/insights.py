"""
Insights page: 2×2 grid of different chart types (box, strip, histogram, heatmap).
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from components.charts import box_chart, strip_chart, histogram_chart, heatmap_chart
from data.loaders import (
    load_box_data,
    load_histogram_data,
    load_heatmap_data,
)


def layout(theme: str = "light", config: dict | None = None) -> html.Div:
    """Insights page: 2×2 layout of box, strip, histogram, heatmap. config from config-store controls chart behavior."""
    config = config or {}
    graph_config = {"displayModeBar": config.get("show_modebar", True)}
    df_box = load_box_data()
    df_hist = load_histogram_data()
    df_heat = load_heatmap_data()

    fig_box = box_chart(
        df_box,
        x="team",
        y="score",
        title="Score distribution by team",
        color="team",
        theme=theme,
        config=config,
    )
    fig_strip = strip_chart(
        df_box,
        x="team",
        y="score",
        title="Scores by team (strip plot)",
        color="team",
        theme=theme,
        config=config,
    )
    fig_hist = histogram_chart(
        df_hist,
        x="response_ms",
        title="Response time distribution",
        nbins=24,
        theme=theme,
        config=config,
    )
    fig_heat = heatmap_chart(
        df_heat,
        x="quarter",
        y="region",
        z="revenue",
        title="Revenue by quarter and region",
        theme=theme,
        config=config,
    )

    return html.Div(
        [
            html.H1("Insights", className="mb-3"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="insights-box-team", figure=fig_box, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="insights-strip-team", figure=fig_strip, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="insights-hist-response", figure=fig_hist, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="insights-heatmap-revenue", figure=fig_heat, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
