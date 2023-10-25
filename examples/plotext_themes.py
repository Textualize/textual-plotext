"""A small app to explore how the different Plotext themes look."""

from __future__ import annotations

from itertools import cycle

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Mount
from textual.reactive import var
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option, Separator

from textual_plotext import PlotextPlot, themes


class ThemeSample(PlotextPlot):
    """A plot for showing off a theme."""

    DEFAULT_CSS = """
    ThemeSample {
        border-top: panel $accent;
        border-bottom: blank $accent;
        margin: 2 4;
    }
    """

    theme: var[str] = var("clear")
    """The theme to show."""

    marker: var[str] = var("fhd")
    """The type of marker to use for the sample."""

    swatch_mode: var[bool] = var(False)
    """Should we be in color swatch mode?"""

    def __init__(
        self, title: str, id: str, classes: str | None = None
    ) -> None:  # pylint:disable=redefined-builtin
        """Initialise the theme sample.

        Args:
            title: The title for the widget.
            id: The ID for the widget.
        """
        super().__init__(id=id, classes=classes)
        self.auto_theme = False
        self.border_title = title
        self._data = [self.plt.sin(phase=n / 4) for n in range(19)]

    @on(Mount)
    def replot(self) -> None:
        """Replot the sample."""
        self.plt.clear_figure()
        self.plt.theme(self.theme)
        self.plt.title("This is the title")
        if self.swatch_mode:
            self.plt.multiple_bar(["Swatch sample"], [[1]] * 20)
        else:
            for data in self._data:
                self.plt.plot(data, marker=self.marker)
        self.refresh()

    def _watch_theme(self) -> None:
        """React to a change of theme."""
        self.border_subtitle = f"{self.theme} ({self.marker})"
        self.replot()

    def _watch_marker(self) -> None:
        """React to a change of marker."""
        self._watch_theme()

    def _watch_swatch_mode(self) -> None:
        """React to the swatch mode being changed."""
        self._watch_theme()


class ThemeApp(App[None]):
    """A Textual application for exploring the different Plotext themes."""

    CSS = """
    #themes {
        height: 1fr;
        border: none;
    }

    #samples {
        width: 5fr;
    }

    .invisible {
        display: none;
    }
    """

    TITLE = "Plotext theme explorer"

    BINDINGS = [
        Binding("d", "toggle_dark", "Light/Dark"),
        Binding("m", "marker", "Change markers"),
        Binding("s", "toggle_swatch", "Plot/Swatch"),
        Binding("q", "quit", "Quit"),
    ]

    marker: var[str] = var("fhd")
    """The marker used for each of the plots."""

    def __init__(self) -> None:
        """Initialise the application."""
        super().__init__()
        self._markers = cycle(("braille", "sd", "dot", "hd", "fhd"))

    def compose(self) -> ComposeResult:
        """Compose the main screen."""
        yield Header()
        with Horizontal():
            yield OptionList(
                *[
                    Option(theme.capitalize(), id=theme.lower())
                    for theme in themes()
                    if not theme.startswith("textual-")
                ],
                Separator(),
                Option("Textual Design Dark-Friendly", id="textual-design-dark"),
                Option("Textual Design Light-Friendly", id="textual-design-light"),
                id="themes",
            )
            with Vertical(id="samples"):
                yield ThemeSample("Plotext Theme", id="plotext", classes="shared")
                yield ThemeSample(
                    "Textual Equivalent Theme", id="textual", classes="shared"
                )
                yield ThemeSample(
                    "Textual Theme", id="exclusive", classes="exclusive invisible"
                )

        yield Footer()

    @on(OptionList.OptionHighlighted)
    def update_samples(self, event: OptionList.OptionHighlighted) -> None:
        """Update each of the samples when the selected theme changes.

        Args:
            event: The selection highlight event.
        """
        if event.option_id is not None:
            if event.option_id.startswith("textual-design"):
                self.query_one("#exclusive", ThemeSample).theme = event.option_id
                self.query(".shared").add_class("invisible")
                self.query(".exclusive").remove_class("invisible")
            else:
                self.query_one("#plotext", ThemeSample).theme = event.option_id
                self.query_one(
                    "#textual", ThemeSample
                ).theme = f"textual-{event.option_id}"
                self.query(".shared").remove_class("invisible")
                self.query(".exclusive").add_class("invisible")

    def _watch_marker(self) -> None:
        """React to a change of marker."""
        for sample in self.query(ThemeSample).results():
            sample.marker = self.marker

    def action_marker(self) -> None:
        """Change the marker used for the plots."""
        self.marker = next(self._markers)

    def action_toggle_swatch(self) -> None:
        """Toggle the samples between plotting and swatch mode."""
        for sample in self.query(ThemeSample).results():
            sample.swatch_mode = not sample.swatch_mode


if __name__ == "__main__":
    ThemeApp().run()
