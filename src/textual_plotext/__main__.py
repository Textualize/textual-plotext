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
            for n in range(4):
                yield PlotextPlot(id=f"plot-{n}")
        yield Footer()

    def on_mount(self) -> None:
        plt = self.query_one("#plot-0", PlotextPlot).plot
        y = plt.sin()
        plt.plot(y)
        plt.title("Line Plot")

        plt = self.query_one("#plot-1", PlotextPlot).plot
        y = plt.sin()
        plt.scatter(y)
        plt.title("Scatter Plot")  # to apply a title

        plt = self.query_one("#plot-2", PlotextPlot).plot
        l = 10**4
        y = plt.sin(periods=2, length=l)
        plt.plot(y)
        plt.xscale("log")
        plt.yscale("linear")
        plt.grid(0, 1)
        plt.title("Logarithmic Plot")
        plt.xlabel("logarithmic scale")
        plt.ylabel("linear scale")

        plt = self.query_one("#plot-3", PlotextPlot).plot
        y1 = plt.sin()
        y2 = plt.sin(2, phase=-1)
        plt.plot(y1, xside="lower", yside="left", label="lower left")
        plt.plot(y2, xside="upper", yside="right", label="upper right")
        plt.title("Multiple Axes Plot")


if __name__ == "__main__":
    DemoApp().run()
