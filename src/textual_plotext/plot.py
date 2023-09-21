"""Provides a class that acts as a thin wrapper around Plottext.

Because (as of the time of writing) there doesn't seem to be a method of
getting a plotting object from Plottext, this class pulls a figure out from
inside Plotext and promotes it to the top level, so to speak, and then takes
care of adding in some of the utility methods that will bee needed.
"""

from __future__ import annotations
from typing import TypeAlias

from typing_extensions import Literal, get_args

import plotext
from plotext._figure import _figure_class as Figure

ThemeName = Literal[
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
]
"""Literal type that is the list of theme names defined in Plotext.

Note:
    This is a copy of the theme names and will need to be updated if Plotext
    ever adds more. The main reasons for taking this approach are:

    1. There is no public interface to access this information.
    2. Turning runtime information into type-checking data isn't simple.
"""

Color: TypeAlias = str | int | tuple[int, int, int]
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

    def show(self) -> None:
        """Stub function. This should never be called within Textual."""


# Hoist the docstrings for the wrapper functions we've added above.
Plot.sin.__doc__ = plotext.sin.__doc__
Plot.square.__doc__ = plotext.square.__doc__
Plot.colorize.__doc__ = plotext.colorize.__doc__


def themes() -> tuple[str, ...]:
    """Get the list of available theme names.

    Returns:
        A tuple of the names of the themes defined in Plotext.
    """
    return get_args(ThemeName)
