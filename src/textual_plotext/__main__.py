"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Header, Footer

from textual_plotext import PlotextPlot


class RefreshingPlot(PlotextPlot):
    def update(self) -> None:
        plt = self.plot
        plt.clf()
        l, frames = 1000, 30
        x = range(1, l + 1)
        y = plt.sin(periods=2, length=l, phase=2 * self.phase / frames)
        plt.scatter(x, y, marker="braille")
        plt.title("Updating plot!")
        plt.theme("dark")
        plt.ylim(-1, 1)
        self.phase += 1
        self.refresh()

    def on_mount(self) -> None:
        self.phase = 0
        self.update()
        self.set_interval(0.1, self.update)


class DemoApp(App[None]):
    """Demonstration application for the library."""

    CSS = """
    Grid {
        grid-size: 2;
    }

    PlotextPlot {
        border: solid cornflowerblue;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        with Grid():
            yield PlotextPlot(id="line")
            yield RefreshingPlot()
            yield PlotextPlot(id="logarithmic")
            yield PlotextPlot(id="multiple")
        yield Footer()

    def on_mount(self) -> None:
        plt = self.query_one("#line", PlotextPlot).plot
        y = plt.sin()
        plt.plot(y)
        plt.title("Line Plot")

        plt = self.query_one("#logarithmic", PlotextPlot).plot
        l = 10**4
        y = plt.sin(periods=2, length=l)
        plt.plot(y)
        plt.xscale("log")
        plt.yscale("linear")
        plt.grid(0, 1)
        plt.title("Logarithmic Plot")
        plt.xlabel("logarithmic scale")
        plt.ylabel("linear scale")

        plt = self.query_one("#multiple", PlotextPlot).plot
        y1 = plt.sin()
        y2 = plt.sin(2, phase=-1)
        plt.plot(y1, xside="lower", yside="left", label="lower left")
        plt.plot(y2, xside="upper", yside="right", label="upper right")
        plt.title("Multiple Axes Plot")


if __name__ == "__main__":
    DemoApp().run()
