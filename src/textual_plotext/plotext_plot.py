"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations

from textual.app import RenderResult
from textual.widget import Widget

from rich.text import Text

from .plot import Plot


class PlotextPlot(Widget):
    """A Plotext plot display widget."""

    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        # TODO: Usual widget stuff here.
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._plot = Plot()

    @property
    def plot(self) -> Plot:
        return self._plot

    def render(self) -> RenderResult:
        self._plot.plotsize(self.size.width, self.size.height)
        return Text.from_ansi(self._plot.build())
