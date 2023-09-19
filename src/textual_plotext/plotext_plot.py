"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations

from textual.app import RenderResult
from textual.reactive import var
from textual.widget import Widget

from rich.text import Text

from .plot import Plot


class PlotextPlot(Widget):
    """A Plotext plot display widget."""

    DEFAULT_CSS = """
    PlotextPlot {
        width: 1fr;
        height: 1fr;
    }
    """

    auto_theme: var[bool] = var(True)
    """Should the plot automatically adjust the theme depending on light and dark mode?"""

    light_mode_theme: var[str] = var("default")
    """The Plotext theme to use for light mode."""

    dark_mode_theme: var[str] = var("dark")
    """The Plotext theme to use for dark mode."""

    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._plot = Plot()
        self.watch(self.app, "dark", self._dark_mode, init=False)

    @property
    def plot(self) -> Plot:
        """The plotting object.

        Use this property as you'd normally use the `plotext` module.
        """
        return self._plot

    def render(self) -> RenderResult:
        self.plot.plotsize(self.size.width, self.size.height)
        if self.auto_theme:
            self.plot.theme(
                self.dark_mode_theme if self.app.dark else self.light_mode_theme
            )
        return Text.from_ansi(self.plot.build())

    def _watch_light_mode_theme(self) -> None:
        """React to changes to the light mode theme."""
        if self.auto_theme and not self.app.dark:
            self.refresh()

    def _watch_dark_mode_theme(self) -> None:
        """React to changes to the dark mode theme."""
        if self.auto_theme and self.app.dark:
            self.refresh()

    def _dark_mode(self) -> None:
        """React to dark mode being toggled."""
        if self.auto_theme:
            self.refresh()
