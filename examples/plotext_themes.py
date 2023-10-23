"""A small app to explore how the different Plotext themes look."""

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Select

from textual_plotext import PlotextPlot

from plotext._dict import themes


class ThemeSample(Vertical):
    """Widget for showing a theme sample."""

    DEFAULT_CSS = """
    ThemeSample {
        padding: 1 2;
    }

    Select * {
        border: none !important;
    }

    Select:focus {
        background: $primary;
    }
    """

    def compose(self) -> ComposeResult:
        yield PlotextPlot()
        yield Select[str](
            [(theme, theme) for theme in themes.keys()],
            value="default",
            allow_blank=False,
        )

    def on_mount(self) -> None:
        plot = self.query_one(PlotextPlot)
        plot.auto_theme = False
        plot.plt.title("This is the title")
        plot.plt.scatter(plot.plt.sin())

    @on(Select.Changed)
    def change_theme(self, event: Select.Changed) -> None:
        if isinstance(event.value, str):
            self.query_one(PlotextPlot).plt.theme(event.value)
            self.query_one(PlotextPlot).refresh()


class ThemeApp(App[None]):
    """A Textual application for exploring the different Plotext themes."""

    TITLE = "Plotext theme explorer"

    BINDINGS = [
        Binding("d", "toggle_dark", "Light/Dark"),
        Binding("q", "quit", "Quit"),
    ]

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        for _ in range(4):
            yield ThemeSample()
        yield Footer()


if __name__ == "__main__":
    ThemeApp().run()
