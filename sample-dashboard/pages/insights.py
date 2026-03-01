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


def layout(theme: str = "light") -> html.Div:
    """Insights page: 2×2 layout of box, strip, histogram, heatmap."""
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
    )
    fig_strip = strip_chart(
        df_box,
        x="team",
        y="score",
        title="Scores by team (strip plot)",
        color="team",
        theme=theme,
    )
    fig_hist = histogram_chart(
        df_hist,
        x="response_ms",
        title="Response time distribution",
        nbins=24,
        theme=theme,
    )
    fig_heat = heatmap_chart(
        df_heat,
        x="quarter",
        y="region",
        z="revenue",
        title="Revenue by quarter and region",
        theme=theme,
    )

    return html.Div(
        [
            html.H1("Insights", className="mb-3"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="insights-box-tl", figure=fig_box),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="insights-strip-tr", figure=fig_strip),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="insights-hist-bl", figure=fig_hist),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="insights-heatmap-br", figure=fig_heat),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
