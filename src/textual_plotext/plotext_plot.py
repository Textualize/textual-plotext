"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations

from rich.text import Text
from textual.app import RenderResult
from textual.reactive import var
from textual.widget import Widget
from textual.color import Color
from textual.theme import Theme
from .plot import Plot, _rgbify_theme, _sequence

from plotext._dict import themes as _themes


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

    def on_mount(self) -> None:
        """Set up the plot."""
        # Watch the application's theme switch so that we can react to
        # any request to auto-change between light and dark themes.
        self.app.theme_changed_signal.subscribe(self, self._theme_changed)

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
        # This is a belt-and-braces setting of the size of the plot.
        # Internally plotsize calls _set_plot, and as best as I can figure
        # out, what I'm doing here *should* be a no-op (or rather a repeat
        # of what I've just done). And yet... the resizing of plots just
        # doesn't work right without this. This *might* be some
        # as-yet-undiscovered side-effect of dumpster-diving for the figure
        # class.
        #
        # https://github.com/Textualize/textual-plotext/issues/5
        self._plot._set_size(self.size.width, self.size.height)
        plotext_theme_name = f"textual-{self.app.theme}"
        self._plot.theme(plotext_theme_name)
        return Text.from_ansi(self._plot.build())

    def _theme_changed(self, theme: Theme) -> None:
        """React to the theme being changed."""
        app_theme = self.app.theme_variables
        plotext_theme = _rgbify_theme(
            Color.parse(app_theme.get("surface")).rgb,
            Color.parse(app_theme.get("surface")).rgb,
            Color.parse(app_theme.get("foreground")).rgb,
            "default",
            [
                Color.parse(app_theme.get("text-accent")).rgb,
                Color.parse(app_theme.get("text-primary")).rgb,
                Color.parse(app_theme.get("text-secondary")).rgb,
                Color.parse(app_theme.get("text-success")).rgb,
                Color.parse(app_theme.get("text-warning")).rgb,
                Color.parse(app_theme.get("text-error")).rgb,
            ],
        )
        plotext_theme_name = f"textual-{self.app.theme}"
        _themes[plotext_theme_name] = plotext_theme
        self._plot.theme(plotext_theme_name)
        self.refresh()
