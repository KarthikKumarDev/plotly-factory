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


def layout() -> html.Div:
    """Charts page: 2×2 layout of bar, line, scatter, pie."""
    df_bar = load_sales_by_region()
    df_line = load_timeseries()
    df_line = df_line.copy()
    df_line["month"] = df_line["month"].dt.strftime("%Y-%m")
    df_scatter = load_scatter_data()
    df_pie = load_pie_data()

    fig_bar = bar_chart(
        df_bar,
        x="region",
        y="sales",
        title="Sales by region",
        color="region",
    )
    fig_line = line_chart(
        df_line,
        x="month",
        y=["revenue", "costs"],
        title="Revenue vs costs",
    )
    fig_scatter = scatter_chart(
        df_scatter,
        x="units",
        y="revenue",
        title="Units vs revenue by segment",
        color="segment",
    )
    fig_pie = pie_chart(
        df_pie,
        names="category",
        values="share",
        title="Share by category",
    )

    return html.Div(
        [
            html.H1("Charts", className="mb-3"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="charts-bar-tl", figure=fig_bar),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="charts-line-tr", figure=fig_line),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="charts-scatter-bl", figure=fig_scatter),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dcc.Graph(id="charts-pie-br", figure=fig_pie),
                        md=6,
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
