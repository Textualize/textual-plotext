"""A small app to explore how the different Plotext themes look."""

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Mount
from textual.reactive import var
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option

from textual_plotext import PlotextPlot, themes


class ThemeSample(PlotextPlot):
    """A plot for showing off a theme."""

    DEFAULT_CSS = """
    ThemeSample {
        border-top: panel $accent;
        border-bottom: blank $accent;
        padding: 2 4;
    }
    """

    theme: var[str] = var("clear")

    def __init__(self, title: str, id: str) -> None:
        super().__init__(id=id)
        self.border_title = title
        self._data = [self.plt.sin(phase=n / 4) for n in range(16)]

    @on(Mount)
    def replot(self) -> None:
        self.plt.clear_figure()
        self.plt.theme(self.theme)
        self.plt.title("This is the title")
        for data in self._data:
            self.plt.scatter(data)
        self.refresh()

    def _watch_theme(self) -> None:
        self.border_subtitle = self.theme
        self.replot()


class ThemeApp(App[None]):
    """A Textual application for exploring the different Plotext themes."""

    CSS = """
    #themes {
        height: 1fr;
        border: none;
    }

    #samples {
        width: 4fr;
    }
    """

    TITLE = "Plotext theme explorer"

    BINDINGS = [
        Binding("d", "toggle_dark", "Light/Dark"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield OptionList(
                *[
                    Option(theme.capitalize(), id=theme.lower())
                    for theme in themes()
                    if not theme.startswith("textual-")
                ],
                id="themes",
            )
            with Vertical(id="samples"):
                yield ThemeSample("Plotext Theme", id="plotext")
                yield ThemeSample("Textual Equivalent Theme", id="textual")
        yield Footer()

    @on(OptionList.OptionHighlighted)
    def update_samples(self, event: OptionList.OptionHighlighted) -> None:
        if event.option_id is not None:
            self.query_one("#plotext", ThemeSample).theme = event.option_id
            self.query_one("#textual", ThemeSample).theme = f"textual-{event.option_id}"


if __name__ == "__main__":
    ThemeApp().run()
