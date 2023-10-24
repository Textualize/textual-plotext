"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations

from rich.text import Text
from textual.app import RenderResult
from textual.reactive import var
from textual.widget import Widget

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

    By default this is set to `False` and `light_mode_theme` and
    `dark_mode_theme` are both set to the same theme, designed to take on
    colours appropriate to the current mode.
    """

    light_mode_theme: var[ThemeName] = var("textual-design-light")
    """The Plotext theme to use for light mode.

    Note:
        This theme is only used when [`auto_theme`][PlotextPlot.auto_theme] is `True`.
    """

    dark_mode_theme: var[ThemeName] = var("textual-design-dark")
    """The Plotext theme to use for dark mode.

    Note:
        This theme is only used when [`auto_theme`][PlotextPlot.auto_theme] is `True`.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,  # pylint:disable=redefined-builtin
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
        # We use textual-default as the default theme, as that's going to
        # work well no matter if we're in light or dark mode.
        self._plot.theme("textual-default")
        # Watch the application's dark mode switch so that we can react to
        # any request to auto-change between light and dark themes.
        self.watch(self.app, "dark", self._dark_mode, init=False)

    @property
    def plt(self) -> Plot:
        """The Plotext plotting object.

        Whereas normally Plotext-using code would so something like this:

        ```python
        import plotext as plt

        ...

        plt.some_call()
        plt.some_other_call()
        ```

        use this `plt` property instead of importing `plotext`.
        """
        return self._plot

    def render(self) -> RenderResult:
        """Render the plot.

        Returns:
            The renderable for displaying the plot.
        """
        self._plot.plotsize(self.size.width, self.size.height)
        if self.auto_theme:
            self._plot.theme(
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
