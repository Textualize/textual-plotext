"""A small app to explore how the different Plotext themes look."""

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Select

from textual_plotext import PlotextPlot, themes


class ThemeSample(Vertical):
    """Widget for showing a theme sample."""

    DEFAULT_CSS = """
    ThemeSample {
        padding: 1 2;
    }

    Select SelectCurrent, Select:focus SelectCurrent {
        border: none !important;
    }

    Select:focus {
        background: $primary;
    }
    """

    def compose(self) -> ComposeResult:
        yield PlotextPlot()
        yield Select[str](
            [(theme, theme) for theme in themes()],
            value="default",
            allow_blank=False,
        )

    def on_mount(self) -> None:
        self.replot()

    @on(Select.Changed)
    def replot(self) -> None:
        plot = self.query_one(PlotextPlot)
        plot.auto_theme = False
        plot.plt.clear_figure()
        plot.plt.theme(self.query_one(Select).value)
        plot.plt.title("This is the title")
        plot.plt.scatter(plot.plt.sin())
        plot.refresh()


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
