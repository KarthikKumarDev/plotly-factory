"""
Sample data loaders for the dashboard. Uses in-memory data for the sample; in production
replace with API/DB/file load per docs/06-DATA-PATTERNS.md.
"""
from __future__ import annotations

import random
from functools import lru_cache

import pandas as pd


@lru_cache(maxsize=None)
def load_sales_by_region() -> pd.DataFrame:
    """Load sample sales-by-region data. In production, load from API/file/DB."""
    return pd.DataFrame({
        "region": ["North", "South", "East", "West", "Central"],
        "sales": [120, 95, 140, 88, 110],
        "orders": [45, 38, 52, 35, 42],
    })


@lru_cache(maxsize=None)
def load_timeseries() -> pd.DataFrame:
    """Load sample time series data for line chart. month is pre-formatted as YYYY-MM string."""
    dates = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%Y-%m")
    return pd.DataFrame({
        "month": dates,
        "revenue": [100, 115, 108, 125, 132, 128, 140, 138, 145, 150, 148, 160],
        "costs": [70, 78, 75, 82, 88, 85, 92, 90, 95, 98, 96, 102],
    })


@lru_cache(maxsize=None)
def load_scatter_data() -> pd.DataFrame:
    """Sample data for scatter (e.g. units vs revenue by segment)."""
    return pd.DataFrame({
        "units": [12, 28, 35, 42, 55, 61, 48, 72, 80, 90],
        "revenue": [120, 280, 320, 410, 540, 600, 470, 710, 790, 880],
        "segment": ["A", "B", "A", "C", "B", "C", "A", "B", "C", "B"],
    })


@lru_cache(maxsize=None)
def load_pie_data() -> pd.DataFrame:
    """Sample data for pie (e.g. share by category)."""
    return pd.DataFrame({
        "category": ["Electronics", "Clothing", "Home", "Sports", "Other"],
        "share": [32, 24, 18, 14, 12],
    })


@lru_cache(maxsize=None)
def load_box_data() -> pd.DataFrame:
    """Sample data for box/violin (e.g. score distribution by team)."""
    random.seed(42)
    teams = ["Alpha", "Beta", "Gamma", "Delta"]
    data = []
    for i, t in enumerate(teams):
        data.extend([{"team": t, "score": random.gauss(70 + i * 5, 12)} for _ in range(25)])
    return pd.DataFrame(data)


@lru_cache(maxsize=None)
def load_histogram_data() -> pd.DataFrame:
    """Sample data for histogram (e.g. response times)."""
    random.seed(43)
    return pd.DataFrame({
        "response_ms": [random.expovariate(1 / 200) for _ in range(200)],
    })


@lru_cache(maxsize=None)
def load_heatmap_data() -> pd.DataFrame:
    """Sample data for heatmap (e.g. value by row and column)."""
    return pd.DataFrame({
        "quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4"],
        "region": ["North", "South", "East", "North", "South", "East", "North", "South", "East", "North", "South", "East"],
        "revenue": [80, 65, 90, 95, 70, 88, 102, 78, 95, 110, 85, 100],
    })
