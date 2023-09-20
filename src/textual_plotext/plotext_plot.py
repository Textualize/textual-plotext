"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations

from textual.app import RenderResult
from textual.reactive import var
from textual.widget import Widget

from rich.text import Text

from .plot import Plot, ThemeName


class PlotextPlot(Widget):
    """A Plotext plot display widget."""

    DEFAULT_CSS = """
    PlotextPlot {
        width: 1fr;
        height: 1fr;
    }
    """

    auto_theme: var[bool] = var(True)
    """Should the plot automatically adjust the theme depending on light and dark mode?

    If set to `True` the theme of the plot will be adjusted to either
    [`light_mode_theme`][PlotextPlot.light_mode_theme] or
    [`dark_mode_theme`][PlotextPlot.dark_mode_theme] when
    [`App.dark`](https://textual.textualize.io/api/app/#textual.app.App.dark)
    is changed.
    """

    light_mode_theme: var[ThemeName] = var("default")
    """The Plotext theme to use for light mode.

    Note:
        This theme is only used when [`auto_theme`][PlotextPlot.auto_theme] is `True`.
    """

    dark_mode_theme: var[ThemeName] = var("dark")
    """The Plotext theme to use for dark mode.

    Note:
        This theme is only used when [`auto_theme`][PlotextPlot.auto_theme] is `True`.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the Plotext plot widget.

        Args:
            name: The name of the Plotext plot widget.
            id: The ID of the Plotext plot widget in the DOM.
            classes: The CSS classes of the Plotext plot widget.
            disabled: Whether the Plotext plot widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._plot = Plot()
        self.watch(self.app, "dark", self._dark_mode, init=False)

    @property
    def plt(self) -> Plot:
        """The Plotext plotting object.

        Whereas normally Plotext-using could would so something like this:

        ```python
        import plotext as plt

        ...

        plt.some_call()
        plt.some_other_call()
        ```

        use this `plt` property instead of importing `plotext`.
        """
        return self._plot

    def plot(self) -> None:
        """The code for creating the plot.

        Subclass `PlotextPlot` and implement this method, placing all the
        code needed to produce the plot within.

        Note:
            Do **NOT** use the Plotext `show` method in here, this widget
            takes care of the work of showing the plot.

        Example:
            ```python
            class ExamplePlot(PlotextPlot):

                def plot(self) -> None:
                    self.plt.scatter(self.plt.sin())
                    plt.title("Scatter Plot")
            ```
        """

    def render(self) -> RenderResult:
        """Render the plot."""
        self.plt.clear_figure()
        self.plot()
        self.plt.plotsize(self.size.width, self.size.height)
        if self.auto_theme:
            self.plt.theme(
                self.dark_mode_theme if self.app.dark else self.light_mode_theme
            )
        return Text.from_ansi(self._plot.build())

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
