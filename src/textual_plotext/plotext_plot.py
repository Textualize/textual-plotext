"""Provides a widget for creating and displaying a Plotext plot."""

from __future__ import annotations
from typing import Literal

from rich.text import Text
from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.color import Color
from .plot import Plot, PlotextThemeName, _rgbify_theme, _sequence

from plotext._dict import themes as _themes


class PlotextPlot(Widget):
    """A Plotext plot display widget."""

    DEFAULT_CSS = """
    PlotextPlot {
        width: 1fr;
        height: 1fr;
    }
    """

    theme: reactive[Literal["auto"] | PlotextThemeName] = reactive("auto")
    """The theme to use for the plot.

    If set to `"auto"` the theme will be dynamically generated based on the
    current theme of the Textual app.

    Note that this will just alter the background and foreground colors of the
    plot to match the current Textual theme, not the colors of the plotted graph.

    If set to a specific Plotext theme name, that theme will be used.
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
        self.app.theme_changed_signal.subscribe(
            self, lambda theme: self._register_theme(theme.name)
        )
        self._register_theme(self.app.theme)

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
        # If the theme is set to "auto" ensure the theme is registered with Plotext.
        plotext_theme_name = self._get_plotext_theme_name(self.app.theme)
        self._plot.theme(plotext_theme_name)
        return Text.from_ansi(self._plot.build())

    def _register_theme(self, app_theme_name: str) -> None:
        """Register the theme with Plotext if necessary.

        Args:
            app_theme_name: The name of the theme from the Textual app.
              This will only be used if the `theme` reactive of this plot
              is set to `"auto"`.
        """
        # If we're not using auto theme, we don't need to register
        # the Textual app theme with Plotext.
        if self.theme != "auto":
            return

        plotext_theme_name = self._get_plotext_theme_name(app_theme_name)
        app_theme_variables = self.app.theme_variables
        if plotext_theme_name not in _themes:
            _themes[plotext_theme_name] = _rgbify_theme(
                Color.parse(app_theme_variables.get("surface")).rgb,
                Color.parse(app_theme_variables.get("surface")).rgb,
                Color.parse(app_theme_variables.get("foreground")).rgb,
                "default",
                _sequence,
            )
        self.refresh()

    def _get_plotext_theme_name(self, app_theme_name: str) -> str:
        """Get the name of the Plotext theme to use.

        If the theme is set to `"auto"` the theme name will be of the form
        `textual-auto-<app_theme_name>`. Otherwise the theme name will be the
        Plotext theme name, which will be directly set on the plot..

        Args:
            app_theme_name: The name of the theme from the Textual app.
        """
        if self.theme == "auto":
            return f"textual-auto-{app_theme_name}"
        else:
            return self.theme
