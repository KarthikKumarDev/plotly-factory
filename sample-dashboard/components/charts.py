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

from utils.theme import get_palette, get_colorway


def apply_theme(fig: go.Figure, theme: str = "light") -> go.Figure:
    """Apply sample app theme (light or dark) to a figure. See docs/08-UI-ACCESSIBILITY.md."""
    palette = get_palette(theme)
    return fig.update_layout(
        template="plotly_dark" if theme == "dark" else "plotly_white",
        paper_bgcolor=palette["chart_paper"],
        plot_bgcolor=palette["chart_plot"],
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size=12,
            color=palette["text_primary"],
        ),
        title_font_size=16,
        colorway=get_colorway(theme),
        margin=dict(t=40, b=40, l=50, r=20),
    )


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    theme: str = "light",
) -> go.Figure:
    """Bar chart for category comparisons. Id pattern: {page}-bar-{suffix}."""
    fig = px.bar(df, x=x, y=y, color=color, text_auto=True)
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig, theme)


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str,
    theme: str = "light",
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
    return apply_theme(fig, theme)


def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    theme: str = "light",
) -> go.Figure:
    """Scatter chart for two continuous variables. Id pattern: {page}-scatter-{suffix}."""
    fig = px.scatter(df, x=x, y=y, color=color, size_max=12)
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig, theme)


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    theme: str = "light",
) -> go.Figure:
    """Pie chart for proportions. Id pattern: {page}-pie-{suffix}."""
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=get_colorway(theme))
    fig.update_layout(title=title)
    return apply_theme(fig, theme)


def box_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    theme: str = "light",
) -> go.Figure:
    """Box plot for distribution by category. Id pattern: {page}-box-{suffix}."""
    fig = px.box(df, x=x, y=y, color=color, color_discrete_sequence=get_colorway(theme))
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig, theme)


def violin_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    theme: str = "light",
) -> go.Figure:
    """Violin plot for distribution shape by category. Id pattern: {page}-violin-{suffix}."""
    fig = px.violin(df, x=x, y=y, color=color, box=True, color_discrete_sequence=get_colorway(theme))
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig, theme)


def strip_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    theme: str = "light",
) -> go.Figure:
    """Strip plot: individual points by category. Id pattern: {page}-strip-{suffix}."""
    fig = px.strip(df, x=x, y=y, color=color, stripmode="overlay", color_discrete_sequence=get_colorway(theme))
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title=y.replace("_", " ").title(),
    )
    return apply_theme(fig, theme)


def histogram_chart(
    df: pd.DataFrame,
    x: str,
    title: str,
    color: str | None = None,
    nbins: int | None = None,
    theme: str = "light",
) -> go.Figure:
    """Histogram for single-variable distribution. Id pattern: {page}-hist-{suffix}."""
    fig = px.histogram(df, x=x, color=color, nbins=nbins, color_discrete_sequence=get_colorway(theme))
    fig.update_layout(
        title=title,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title="Count",
    )
    return apply_theme(fig, theme)


def heatmap_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    title: str,
    theme: str = "light",
) -> go.Figure:
    """Heatmap for matrix / 2D density. Id pattern: {page}-heatmap-{suffix}."""
    palette = get_palette(theme)
    pivot = df.pivot_table(values=z, index=y, columns=x, aggfunc="sum")
    fig = px.imshow(
        pivot,
        labels=dict(x=x.replace("_", " ").title(), y=y.replace("_", " ").title(), color=z),
        color_continuous_scale=[palette["chart_paper"], palette["primary"]],
        aspect="auto",
    )
    fig.update_layout(title=title)
    return apply_theme(fig, theme)


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
