"""Provides a class that acts as a thin wrapper around Plottext.

Because (as of the time of writing) there doesn't seem to be a method of
getting a plotting object from Plottext, this class provides a way of
building up the list of calls on Plotext so that we can act as if that is
provided.
"""

from __future__ import annotations

from typing import Any, Callable
from typing_extensions import Self

import plotext

SAFE: set[str] = {"sin"}


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
    """A Plottext-wrapper class."""

    def __init__(self) -> None:
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
        self._calls = []

    def _run(self) -> None:
        plotext.clear_figure()
        for step in self._calls:
            step.execute()

    def show(self) -> None:
        self._run()
        return plotext.show()

    def build(self) -> str:
        self._run()
        return plotext.build()
