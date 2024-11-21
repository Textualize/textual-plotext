"""Provides a class that acts as a thin wrapper around Plottext.

Because (as of the time of writing) there doesn't seem to be a method of
getting a plotting object from Plottext, this class pulls a figure out from
inside Plotext and promotes it to the top level, so to speak, and then takes
care of adding in some of the utility methods that will bee needed.
"""

from __future__ import annotations

from typing import Any, Tuple, Union

from textual.theme import BUILTIN_THEMES
from typing_extensions import Literal, TypeAlias, get_args

from plotext._dict import (
    themes as _themes,
    type1_to_type2_codes,
)
from plotext._utility import get_color_code

from textual.color import Color as TextualColor

from . import plotext
from .plotext._figure import _figure_class as Figure

PlotextThemeName = Literal[
    # The standard Plotext themes.
    "clear",
    "dark",
    "default",
    "dreamland",
    "elegant",
    "girly",
    "grandpa",
    "matrix",
    "mature",
    "pro",
    "retro",
    "sahara",
    "salad",
    "scream",
    "serious",
    "windows",
    # Full colour versions of the Plotext themes.
    "textual-clear",
    "textual-dark",
    "textual-default",
    "textual-dreamland",
    "textual-elegant",
    "textual-girly",
    "textual-grandpa",
    "textual-matrix",
    "textual-mature",
    "textual-pro",
    "textual-retro",
    "textual-sahara",
    "textual-salad",
    "textual-scream",
    "textual-serious",
    "textual-windows",
]
"""Literal type that is the list of theme names defined in Plotext.

Note:
    This is a copy of the theme names and will need to be updated if Plotext
    ever adds more. The main reasons for taking this approach are:

    1. There is no public interface to access this information.
    2. Turning runtime information into type-checking data isn't simple.
"""

Color: TypeAlias = Union[str, int, Tuple[int, int, int]]
"""Type of a Plotext colour."""


class Plot(Figure):
    """A class that provides a Textual-friendly interface to Plotext.

    This class inherits from Plotext's `_figure_class` and then adds access
    to some global functions, making it appear like the top-level `plotext`
    module.

    The aim of the class is to make this:

    ```python
    import plotext as plt

    plt.title("Scatter Plot")
    plt.scatter(plt.sin())
    ```

    and this:

    ```python
    plt = Plot()
    plt.title("Scatter Plot")
    plt.scatter(plt.sin())
    ```

    functionally equivalent, but with the advantage that the latter has no
    global state and is free of external side-effects.
    """

    @staticmethod
    def sin(
        periods: int = 2,
        length: int = 200,
        amplitude: int = 1,
        phase: float = 0,
        decay: int = 0,
    ) -> list[float]:
        """A wrapper around `Plotext.sin`."""
        return plotext.sin(
            periods=periods,
            length=length,
            amplitude=amplitude,
            phase=phase,
            decay=decay,
        )

    @staticmethod
    def square(periods: int = 2, length: int = 200, amplitude: float = 1) -> list[int]:
        """A wrapper around `Plotext.square`."""
        return plotext.square(periods=periods, length=length, amplitude=amplitude)

    @staticmethod
    def colorize(
        string: str,
        fullground: Color | None = None,
        style: str | None = None,
        background: Color | None = None,
        show: bool = False,
    ) -> str:
        """A wrapper around `Plotet.colorize`."""
        return plotext.colorize(
            string,
            fullground=fullground,
            style=style,
            background=background,
            show=show,
        )

    @staticmethod
    def uncolorize(string: str) -> str:
        """A wrapper around `Plotext.uncolorize`."""
        return plotext.uncolorize(string)

    @staticmethod
    def transpose(data: list[list[Any]]) -> list[list[Any]]:
        """A wrapper around `Plotext.transpose`."""
        return plotext.transpose(data)

    platform = plotext.platform
    """The platform, as recognised by Plotext.

    One of either `unix` or `windows`.
    """

    def show(self) -> None:
        """Stub function. This should never be called within Textual."""

    def save_fig(
        self, path: str | None = None, append: bool = False, keep_colors: bool = False
    ) -> None:
        """Stub function. This should not be called within Textual."""
        # Actually... it might make sense to support this at some point and
        # might not be too tricky to handle. But for now this is about
        # allowing plotting within the application.
        del path, append, keep_colors


# Hoist the docstrings for the wrapper functions we've added above.
Plot.sin.__doc__ = plotext.sin.__doc__
Plot.square.__doc__ = plotext.square.__doc__
Plot.colorize.__doc__ = plotext.colorize.__doc__
Plot.uncolorize.__doc__ = plotext.uncolorize.__doc__
Plot.transpose.__doc__ = plotext.transpose.__doc__


def themes() -> tuple[str, ...]:
    """Get the list of available theme names.

    Returns:
        A tuple of the names of the themes defined in Plotext.
    """
    return get_args(PlotextThemeName)


##############################################################################
# Here we patch in some textual-friendly themes. A Plotext theme is of the
# style:
#
# [canvas_color, axes_color, ticks_color, ticks_style, color_sequence]
#
# where color_sequence is a sequence of colours that will be used as plots
# are added (that is, if you plot 3 types of data and don't specify colours,
# this sequence will be used).


def _rgbify(color: Color) -> tuple[int, int, int] | str:
    """Force any Plotext colour into an RGB value.

    Args:
        color: The colour to convert.

    Returns:
        An RGB tuple for the colour.
    """
    if isinstance(color, str):
        # For some reason Plotext uses yellow and gold but never defines
        # them.
        #
        # TODO: Figure out a good version of those colours.
        return (
            color
            if color == "default"
            else _rgbify(
                get_color_code(
                    {"yellow": "orange", "gold": "orange+"}.get(color, color)
                )
            )
        )
    if isinstance(color, int):
        # A single integer; convert that into an RGB.
        return type1_to_type2_codes[color]
    # Must be an RGB already.
    return color


def _rgbify_theme(
    canvas_color: Color,
    axes_color: Color,
    ticks_color: Color,
    ticks_style: str,
    data_colors: list[Color],
) -> tuple[Color, Color, Color, str, list[Color]]:
    """Turn the given theme into a fully-RGB theme.

    Args:
        canvas_color: The canvas color.
        axes_color: The axes color.
        ticks_color: The ticks color.
        ticks_style: The styling for the ticks.
        data_colors: The sequence of colors for the various plots.

    Returns:
        The theme, made RGB-friendly.
    """
    return (
        _rgbify(canvas_color),
        _rgbify(axes_color),
        _rgbify(ticks_color),
        ticks_style,
        [_rgbify(data_color) for data_color in data_colors],
    )


_sequence = [
    (0, 130, 200),
    (60, 180, 75),
    (230, 25, 75),
    (255, 225, 25),
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    (240, 50, 230),
    (180, 225, 40),
    (250, 190, 212),
    (0, 128, 128),
    (220, 190, 255),
    (170, 110, 40),
    (235, 230, 180),
    (128, 0, 0),
    (170, 255, 195),
    (128, 128, 0),
    (255, 215, 180),
    (0, 0, 245),
    (128, 128, 128),
]
"""A sequence of colours for multiple plots.

Designed to work with either light or dark mode.
"""

# Make full-colour versions of the Plotext themes. In almost every case
# we'll follow the data sequence colours laid down by Plotext; but in a
# couple of cases we'll use our own curated set.
_themes["textual-default"] = list(
    _rgbify_theme("default", "default", "default", "default", _sequence)
)
_themes["textual-clear"] = list(
    _rgbify_theme(
        "default",
        "default",
        "default",
        "default",
        ["default"],
    )
)
_themes["textual-dark"] = _rgbify_theme(*_themes["dark"])
_themes["textual-dreamland"] = _rgbify_theme(*_themes["dreamland"])
_themes["textual-elegant"] = _rgbify_theme(*_themes["elegant"])
_themes["textual-girly"] = _rgbify_theme(*_themes["girly"])
_themes["textual-grandpa"] = _rgbify_theme(*_themes["grandpa"])
_themes["textual-matrix"] = _rgbify_theme(*_themes["matrix"])
_themes["textual-mature"] = _rgbify_theme(*_themes["mature"])
_themes["textual-pro"] = _themes["textual-default"]
_themes["textual-retro"] = _rgbify_theme(*_themes["retro"])
_themes["textual-sahara"] = _rgbify_theme(*_themes["sahara"])
_themes["textual-salad"] = _rgbify_theme(*_themes["salad"])
_themes["textual-scream"] = _rgbify_theme(*_themes["scream"])
_themes["textual-serious"] = _rgbify_theme(*_themes["serious"])
_themes["textual-windows"] = _rgbify_theme(*_themes["windows"])
