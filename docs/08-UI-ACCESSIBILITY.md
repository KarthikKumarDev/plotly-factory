# UI and accessibility

Rules for color consistency, font consistency, standard layouts, and accessibility. Follow these when building or changing dashboard UI so it stays consistent and usable. Chart theming: [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md). Layout components: [07-COMPONENTS.md](07-COMPONENTS.md).

---

## Guidelines for visually aesthetic dashboards

Apply these so every dashboard feels polished and on-brand.

| Guideline | Action |
|-----------|--------|
| **Single source of visual truth** | One theme (colors, fonts, spacing) across the app. Use the same Plotly template and color sequence everywhere. See §1 Color consistency, §2 Theme modes, §3 Font consistency, §4 Standard layouts. Do not use one-off colors or fonts unless documented. |
| **Clear visual hierarchy** | Consistent heading levels, chart titles, and axis labels. Use a small set of chart types and layouts from [07-COMPONENTS.md](07-COMPONENTS.md) so the dashboard feels coherent. See §3 Font consistency. |
| **Whitespace and alignment** | Use a grid (e.g. `dbc.Row` / `dbc.Col`) and consistent padding so components align and the layout breathes. Document grid and spacing in §4 or in [07-COMPONENTS.md](07-COMPONENTS.md). |
| **Charts that support the narrative** | Choose chart types that match the message (e.g. time series for trends, bar for comparisons). Keep axes and legends readable; avoid clutter. Follow [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md) for theming and performance. |
| **Responsive and proportional** | Design for different viewport sizes: use responsive components and relative sizing. Note breakpoints or layout rules in this doc or in [07-COMPONENTS.md](07-COMPONENTS.md) so future dashboards stay consistent. |

---

## Guidelines for higher user experience (UX)

These practices make dashboards easier and more pleasant to use.

| Guideline | Action |
|-----------|--------|
| **Loading and progress** | Use `dcc.Loading` around any component that depends on slow data or callbacks. Avoid blank areas with no feedback. See [05-DASH-GUIDE.md](05-DASH-GUIDE.md). |
| **Clear feedback** | After user actions (filters, clicks), show that something happened (e.g. updated chart, disabled button, or short message). Use `no_update` only when you intentionally leave an output unchanged. |
| **Obvious navigation and purpose** | Each page or section has a clear purpose; in multi-page apps, use obvious navigation (e.g. navbar, breadcrumbs). Document structure in [03-ARCHITECTURE.md](03-ARCHITECTURE.md) and [07-COMPONENTS.md](07-COMPONENTS.md). |
| **Accessibility** | Sufficient contrast, labels for controls, meaningful chart titles and axis labels, keyboard/focus. See §5–8 in this doc. Treat a11y as part of good UX. |
| **Error and empty states** | When data is missing or a callback fails, show a clear message instead of a broken or empty chart. Document how errors are surfaced in [05-DASH-GUIDE.md](05-DASH-GUIDE.md) or [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md). |
| **Performance** | Keep interactions responsive: use caching ([06-DATA-PATTERNS.md](06-DATA-PATTERNS.md)), appropriate chart types and downsampling ([04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md)), and avoid large payloads in the client. |

---

## 1. Color consistency

| Rule | Action |
|------|--------|
| **Single palette** | Define one palette per theme: primary, secondary, neutral, semantic (success, warning, error). Use the same hex everywhere (UI and charts). |
| **Where to set** | CSS variables or shared config (`theme/colors.py`, `assets/theme.css`). In Plotly: `fig.update_layout(colorway=[...])` from the same palette. |
| **Charts** | Same color sequence for all charts (e.g. `px.colors.qualitative.Set2` or your palette). See [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md). |
| **Do not** | Use one-off colors. Add new colors to the palette and document them. |

---

## 2. Dark and light theme modes

Support **light** and **dark** themes with separate palettes. One active theme at a time; apply to full app (layout + charts).

### Theme switch

| Rule | Action |
|------|--------|
| **Storage** | `dcc.Store(id="theme-mode", data="light")` or `"dark"`; or read `prefers-color-scheme`. |
| **Apply** | Set `data-theme="light"` or `data-theme="dark"` on root container; style via CSS `[data-theme="light"]` / `[data-theme="dark"]`. |
| **Control** | Toggle (switch or dropdown) updates Store and triggers callback or clientside refresh of layout and charts. |

### Light theme palette (exact values — rich royal pastels)

| Role | Use for | Value |
|------|--------|--------|
| **Background** | Page background | `#faf8ff` |
| **Surface** | Cards, panels, inputs | `#f0ebfa` |
| **Text primary** | Body text, headings | `#3d3551` |
| **Text secondary** | Captions, hints | `#7a6b8a` |
| **Primary** | Buttons, links, accents | `#7b68ee` |
| **Border** | Dividers, card borders | `#e0d8f0` |
| **Chart paper** | Plotly `paper_bgcolor` | `#faf8ff` |
| **Chart plot** | Plotly `plot_bgcolor` | `#f0ebfa` |

### Dark theme palette (exact values — rich royal pastels)

| Role | Use for | Value |
|------|--------|--------|
| **Background** | Page background | `#1a1625` |
| **Surface** | Cards, panels, inputs | `#252035` |
| **Text primary** | Body text, headings | `#e8e4f0` |
| **Text secondary** | Captions, hints | `#a89bb8` |
| **Primary** | Buttons, links, accents | `#a78bfa` |
| **Border** | Dividers, card borders | `#3d3551` |
| **Chart paper** | Plotly `paper_bgcolor` | `#1a1625` |
| **Chart plot** | Plotly `plot_bgcolor` | `#252035` |

### Rules for both themes

| Rule | Action |
|------|--------|
| **Contrast** | Meet WCAG AA in both themes. Check light and dark. |
| **Charts** | Pass active theme into figure builder; set `paper_bgcolor`, `plot_bgcolor`, `font.color`, `colorway`. Use `plotly_white` (light) or `plotly_dark` (dark), or set layout explicitly. |
| **Single source** | Define both palettes in one place (`theme/colors.py` or `assets/theme.css`). Do not hardcode theme colors in components. |

---

## 3. Font consistency

| Rule | Action |
|------|--------|
| **Font stack** | One family for the app. Default: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`. Set in root CSS or `assets/`. |
| **Size scale** | Use one scale. Default: page title `1.5rem`, section heading `1.25rem`, body `1rem`, caption `0.875rem`. Use same scale in HTML and in `fig.update_layout(font=...)`. |
| **Hierarchy** | Headings in order (h1 → h2 → h3). No skipped levels. One h1 per page. |
| **Do not** | Mix font families or ad-hoc sizes. |

---

## 4. Standard layouts

| Rule | Action |
|------|--------|
| **Grid** | `dbc.Container` + `dbc.Row` / `dbc.Col`. Same breakpoints and gutters on every page. |
| **Spacing** | One scale. Default: `4px`, `8px`, `16px`, `24px`, `32px` (or `0.25rem`–`2rem`). Same padding/margin for similar elements. |
| **Cards vs sections** | `dbc.Card` for distinct blocks (metrics, chart containers). Plain div + heading for simple groups. Same content type → same pattern. |
| **Alignment** | Align to grid; align labels and values across cards/tables. Document patterns in [07-COMPONENTS.md](07-COMPONENTS.md). |

---

## 5. Colors and contrast (accessibility)

| Rule | Action |
|------|--------|
| **WCAG AA** | Normal text: contrast ratio **≥ 4.5:1**. Large text (18px+ or 14px+ bold): **≥ 3:1**. Use a contrast checker on your palette. |
| **Charts** | Colorblind-friendly sequences; contrast between series and background. See [04-PLOTLY-GUIDE.md](04-PLOTLY-GUIDE.md). |

---

## 6. Labels and semantics

| Rule | Action |
|------|--------|
| **Form controls** | Every dropdown, slider, input has a visible label or `aria-label="Description"`. No unlabeled controls. |
| **Charts** | `fig.update_layout(title="...", xaxis_title="...", yaxis_title="...")` with meaningful text. |
| **Links/buttons** | Descriptive text (e.g. "View report"). Do not use "Click here". |

---

## 7. Keyboard and focus

| Rule | Action |
|------|--------|
| **Focus order** | Tab order: top to bottom, left to right. Focus must be visible (e.g. `outline: 2px solid; outline-offset: 2px` or `box-shadow` ring). |
| **Shortcuts** | If the app has shortcuts, document them (help section or this doc). |

---

## 8. Screen readers

| Rule | Action |
|------|--------|
| **Structure** | Semantic HTML; headings for sections. Use heading levels in order. |
| **Live regions** | For dynamic updates (e.g. "Data updated"), use `aria-live="polite"` on the container that changes. |
| **Dash components** | Add labels or workarounds for known dcc/dbc a11y gaps. |

---

## 9. Checklist

- [ ] Single palette per theme; no one-off colors
- [ ] Light and dark palettes in use; theme switch works; charts use active theme
- [ ] One font stack and size scale; heading hierarchy correct
- [ ] Grid and spacing scale consistent
- [ ] Contrast ≥ 4.5:1 (normal) / ≥ 3:1 (large)
- [ ] All interactive elements labeled
- [ ] Focus visible; tab order logical
- [ ] Chart titles and axes descriptive

---

Use one palette per theme, one font scale, one layout system. Document new colors or layout patterns in this doc or in 07-COMPONENTS.
