"""Provides a class that acts as a thin wrapper around Plottext.

Because (as of the time of writing) there doesn't seem to be a method of
getting a plotting object from Plottext, this class provides a way of
building up the list of calls on Plotext so that we can act as if that is
provided.
"""

from __future__ import annotations

from typing import Any, Callable

from typing_extensions import Final, Self

import plotext

SAFE: Final[set[str]] = {"sin"}
"""The set of functions that are safe to call without holding back.

Some Plotext functions are simple helpers that return values that are needed
right away. If they are named within this set they'll be called as such.
"""


class PlotCall:
    """Class that holds the details of a single call to Plotext."""

    def __init__(self, function: Callable[[Any], Any]) -> None:
        """Initialise the all to Plotext.

        Args:
            function: The function that will be called.
        """
        self._function = function
        self._args: tuple[Any, ...] = tuple()
        self._kwargs: dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        """Capture the arguments for the call.

        Args:
            args: The positional arguments for the call.
            kwargs: The keyword arguments for the call.

        Returns:
            Self.
        """
        self._args = args
        self._kwargs = kwargs
        return self

    def execute(self) -> None:
        """Execute the call to Plotext."""
        self._function(*self._args, **self._kwargs)

    def __repr__(self) -> str:
        args = [repr(argument) for argument in self._args]
        kwargs = [f"{keyword}={repr(value)}" for keyword, value in self._kwargs.items()]
        return f"{self._function.__name__}({', '.join([*args, *kwargs])})"


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
            raise NameError(f"Plotext.{attr} does not exist") from None
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
