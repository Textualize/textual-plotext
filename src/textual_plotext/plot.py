"""Provides a class that acts as a thin wrapper around Plottext.

Because (as of the time of writing) there doesn't seem to be a method of
getting a plotting object from Plottext, this class provides a way of
building up the list of calls on Plotext so that we can act as if that is
provided.
"""

from __future__ import annotations

from typing import Any, Callable

import plotext

SAFE: set[str] = {"sin"}
"""The set of functions that are safe to call without holding back.

Some Plotext functions are simple helpers that return values that are needed
right away. If they are named within this set they'll be called as such.
"""


class PlotCall:
    def __init__(self, function: Callable[[Any], Any]) -> None:
        self._function = function
        self._args: tuple[Any, ...] = tuple()
        self._kwargs: dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        return None

    def execute(self) -> None:
        return self._function(*self._args, **self._kwargs)

    def __repr__(self) -> str:
        # TODO: Just for debugging now; tidy up so it looks correct.
        return (
            f"{self._function.__name__}("
            # TODO: Don't have the stray , between args and kwargs.
            f"{', '.join([repr(arg) for arg in self._args])}"
            f", {self._kwargs}"
            ")"
        )


class Plot:
    """A Plottext-wrapper class.

    This class is designed to wrap the Plotext module and, where possible,
    capture plotting functions for later playback.
    """

    def __init__(self) -> None:
        """Initialise the Plotext-wrapper class."""
        self._calls: list[PlotCall] = []

    def __getattr__(self, attr: str):
        if attr in SAFE:
            return getattr(plotext, attr)
        try:
            self._calls.append(PlotCall(getattr(plotext, attr)))
        except AttributeError:
            raise NameError from None
        return self._calls[-1]

    def clear_figure(self) -> None:
        """Clear the plot."""
        self._calls = []

    def _run(self) -> None:
        """Run the plot.

        Calling this method has the side-effect of clearing the current
        figure and playing back all of the calls made on the instance of
        this class.
        """
        plotext.clear_figure()
        for step in self._calls:
            step.execute()

    def show(self) -> None:
        """Runs the plot commands and calls the Plotext `show` method."""
        self._run()
        plotext.show()

    def build(self) -> str:
        """Runs the plot commands and calls the Plotext `build` method."""
        self._run()
        return plotext.build()
