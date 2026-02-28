"""
Sample data loaders for the dashboard. Uses in-memory data for the sample; in production
replace with API/DB/file load per docs/06-DATA-PATTERNS.md.
"""
from __future__ import annotations

import pandas as pd


def load_sales_by_region() -> pd.DataFrame:
    """Load sample sales-by-region data. In production, load from API/file/DB."""
    return pd.DataFrame({
        "region": ["North", "South", "East", "West", "Central"],
        "sales": [120, 95, 140, 88, 110],
        "orders": [45, 38, 52, 35, 42],
    })


def load_timeseries() -> pd.DataFrame:
    """Load sample time series data for line chart."""
    dates = pd.date_range("2024-01-01", periods=12, freq="MS")
    return pd.DataFrame({
        "month": dates,
        "revenue": [100, 115, 108, 125, 132, 128, 140, 138, 145, 150, 148, 160],
        "costs": [70, 78, 75, 82, 88, 85, 92, 90, 95, 98, 96, 102],
    })


def load_scatter_data() -> pd.DataFrame:
    """Sample data for scatter (e.g. units vs revenue by segment)."""
    return pd.DataFrame({
        "units": [12, 28, 35, 42, 55, 61, 48, 72, 80, 90],
        "revenue": [120, 280, 320, 410, 540, 600, 470, 710, 790, 880],
        "segment": ["A", "B", "A", "C", "B", "C", "A", "B", "C", "B"],
    })


def load_pie_data() -> pd.DataFrame:
    """Sample data for pie (e.g. share by category)."""
    return pd.DataFrame({
        "category": ["Electronics", "Clothing", "Home", "Sports", "Other"],
        "share": [32, 24, 18, 14, 12],
    })
