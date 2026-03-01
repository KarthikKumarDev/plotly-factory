"""
Theme constants for the sample dashboard. Aligns with docs/08-UI-ACCESSIBILITY.md (light and dark).
"""

# Light theme palette (rich royal pastels)
LIGHT = {
    "background": "#faf8ff",
    "surface": "#f0ebfa",
    "text_primary": "#3d3551",
    "text_secondary": "#7a6b8a",
    "primary": "#7b68ee",
    "border": "#e0d8f0",
    "chart_paper": "#faf8ff",
    "chart_plot": "#f0ebfa",
}

# Dark theme palette (rich royal pastels)
DARK = {
    "background": "#1a1625",
    "surface": "#252035",
    "text_primary": "#e8e4f0",
    "text_secondary": "#a89bb8",
    "primary": "#a78bfa",
    "border": "#3d3551",
    "chart_paper": "#1a1625",
    "chart_plot": "#252035",
}

# Color sequence for Plotly charts — light theme
CHART_COLORWAY = [
    "#7b68ee",
    "#6b5bbd",
    "#9f8eed",
    "#5a4a9e",
    "#b8a9f0",
]

# Color sequence for Plotly charts — dark theme
CHART_COLORWAY_DARK = [
    "#a78bfa",
    "#8b5cf6",
    "#c4b5fd",
    "#7c3aed",
    "#ddd6fe",
]


def get_palette(theme: str) -> dict:
    """Return LIGHT or DARK palette by theme name."""
    return DARK if theme == "dark" else LIGHT


def get_colorway(theme: str) -> list[str]:
    """Return chart colorway for the given theme."""
    return CHART_COLORWAY_DARK if theme == "dark" else CHART_COLORWAY
