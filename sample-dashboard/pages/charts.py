"""
Charts page: 2×2 grid of different chart types (bar, line, scatter, pie) with color.
"""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from components.charts import bar_chart, line_chart, scatter_chart, pie_chart
from data.loaders import (
    load_sales_by_region,
    load_timeseries,
    load_scatter_data,
    load_pie_data,
)


def layout(theme: str = "light", config: dict | None = None) -> html.Div:
    """Charts page: 2×2 layout of bar, line, scatter, pie. config from config-store controls chart behavior."""
    config = config or {}
    graph_config = {"displayModeBar": config.get("show_modebar", True)}
    df_bar = load_sales_by_region()
    df_line = load_timeseries()
    df_scatter = load_scatter_data()
    df_pie = load_pie_data()

    fig_bar = bar_chart(
        df_bar,
        x="region",
        y="sales",
        title="Sales by region",
        color="region",
        theme=theme,
        config=config,
    )
    fig_line = line_chart(
        df_line,
        x="month",
        y=["revenue", "costs"],
        title="Revenue vs costs",
        theme=theme,
        config=config,
    )
    fig_scatter = scatter_chart(
        df_scatter,
        x="units",
        y="revenue",
        title="Units vs revenue by segment",
        color="segment",
        theme=theme,
        config=config,
    )
    fig_pie = pie_chart(
        df_pie,
        names="category",
        values="share",
        title="Share by category",
        theme=theme,
        config=config,
    )

    return html.Div(
        [
            html.H1("Charts", className="mb-3"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="charts-bar-region", figure=fig_bar, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="charts-line-revenue", figure=fig_line, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="charts-scatter-units", figure=fig_scatter, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="charts-pie-category", figure=fig_pie, config=graph_config),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
