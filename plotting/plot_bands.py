
# Plot fan charts with `plot_bands`
#
# `plot_bands` renders multi-variant Series as fan charts: bands of shaded
# regions around a central midline, useful for visualising uncertainty or
# distributional forecasts.
#
# Data layout (columns of the multi-variant Series):
#   num_variants = 2k + 1  →  k bands + 1 midline
#   num_variants = 2k      →  k bands, no midline
#
# For a 5-variant Series [v0, v1, v2, v3, v4]:
#   v0, v4  →  outer band edges
#   v1, v3  →  inner band edges
#   v2      →  midline


# -----------------------------------------------------------------------
# Import packages
# -----------------------------------------------------------------------

import numpy as np
import irispie as ir

ir.min_version_required("0.7.0")


# -----------------------------------------------------------------------
# Create sample fan-chart data
# -----------------------------------------------------------------------
#
# Simulate a random-walk central path with linearly widening uncertainty.

_SPAN = ir.qq(2020, 1) >> ir.qq(2024, 4)
_NUM_PERIODS = len(tuple(_SPAN))

np.random.seed(0)

_midline = ir.Series(
    periods=_SPAN,
    values=np.cumsum(np.random.normal(0, 0.3, _NUM_PERIODS)),
)

_inner = ir.Series(
    periods=_SPAN,
    values=np.linspace(0.1, 1.0, _NUM_PERIODS),
)

_outer = ir.Series(
    periods=_SPAN,
    values=np.linspace(0.2, 2.5, _NUM_PERIODS),
)

# 5-variant Series: 2 symmetric bands + midline
bands5 = _midline-_outer | _midline-_inner | _midline | _midline+_inner | _midline+_outer

# 3-variant Series: 1 band + midline
bands3 = _midline-_inner | _midline | _midline+_inner


# -----------------------------------------------------------------------
# Basic fan chart (2 bands + midline)
# -----------------------------------------------------------------------

bands5.plot_bands(
    legend=["Outer band", "Inner band", "Central path"],
    show_legend=True,
)


# -----------------------------------------------------------------------
# Single band + midline
# -----------------------------------------------------------------------

bands3.plot_bands(
    legend=["Band", "Central path"],
    show_legend=True,
    figure_title="Single band",
)


# -----------------------------------------------------------------------
# Custom shading weights
#
# shading_weights controls the intensity (opacity) of each band shade.
# Each weight is a blend factor in [0, 1] between the background color
# and the base color: 0 → background, 1 → full base color.
# The number of weights must equal the number of bands (num_variants // 2).
# -----------------------------------------------------------------------

bands5.plot_bands(
    shading_weights=[0.15, 0.40],   # outer band lighter, inner band darker
    figure_title="Custom shading weights",
)


# -----------------------------------------------------------------------
# Custom background color
#
# base_color sets the base color of all the band shades and the midline.
# shading_background sets the color that each band shade blends into.
# Accepts hex strings, rgb(...) strings, or RGBA float tuples.
# Defaults to white (1, 1, 1, 1).
# -----------------------------------------------------------------------

bands5.plot_bands(
    base_color="#000",
    shading_background="#e8f0fe",   # light blue background
    figure_title="Custom shading background",
)


# -----------------------------------------------------------------------
# Fine-grained trace updates
#
# update_band_traces   — applied (cyclically) to each band trace
# update_midline_trace — applied to the midline trace only
# -----------------------------------------------------------------------

bands5.plot_bands(
    update_band_traces={"line_width": 0},
    update_midline_trace={"line_color": "black", "line_width": 2},
    figure_title="Custom trace updates",
)


# -----------------------------------------------------------------------
# Fan chart in a subplot grid
# -----------------------------------------------------------------------

fig = ir.make_subplots(
    (1, 2),
    subplot_titles=["Two bands", "One band"],
)

bands5.plot_bands(
    figure=fig,
    subplot=0,
    subplot_title="Two bands",
    show_figure=False,
)

bands3.plot_bands(
    figure=fig,
    subplot=1,
    subplot_title="One band",
    show_figure=False,
)

fig.show()
