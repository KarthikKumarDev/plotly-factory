"""
Reusable chart builders. Returns Plotly figures; apply theme from docs/08-UI-ACCESSIBILITY.md.
See docs/07-COMPONENTS.md and docs/04-PLOTLY-GUIDE.md.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html

from utils.theme import CHART_COLORWAY, LIGHT


def apply_theme(fig: go.Figure) -> go.Figure:
    """Apply sample app theme (light) to a figure."""
    return fig.update_layout(
        template="plotly_white",
        paper_bgcolor=LIGHT["chart_paper"],
        plot_bgcolor=LIGHT["chart_plot"],
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size=12,
            color=LIGHT["text_primary"],
        ),
        title_font_size=16,
        colorway=CHART_COLORWAY,
        margin=dict(t=40, b=40, l=50, r=20),
    )


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
) -> go.Figure:
    """Bar chart for category comparisons. Id pattern: {page}-bar-{suffix}."""
    fig = px.bar(df, x=x, y=y, color=color, text_auto=True)
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig)


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str,
) -> go.Figure:
    """Line chart for time series. Id pattern: {page}-line-{suffix}."""
    if isinstance(y, str):
        y = [y]
    fig = px.line(df, x=x, y=y, markers=True)
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title="Value",
        legend_title="",
    )
    return apply_theme(fig)


def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
) -> go.Figure:
    """Scatter chart for two continuous variables. Id pattern: {page}-scatter-{suffix}."""
    fig = px.scatter(df, x=x, y=y, color=color, size_max=12)
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig)


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
) -> go.Figure:
    """Pie chart for proportions. Id pattern: {page}-pie-{suffix}."""
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=CHART_COLORWAY)
    fig.update_layout(title=title)
    return apply_theme(fig)


def metric_card(
    title: str,
    value: str | int | float,
    card_id: str,
) -> dbc.Card:
    """Build a metric card (dbc.Card). Id pattern: {page}-metric-{suffix}."""
    return dbc.Card(
        [
            dbc.CardHeader(title, className="text-muted small"),
            dbc.CardBody(html.H4(str(value), className="mb-0"), id=card_id),
        ],
        className="shadow-sm",
    )
