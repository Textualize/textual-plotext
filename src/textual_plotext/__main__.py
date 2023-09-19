"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

from typing import Callable

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Label, Rule, TabbedContent, TabPane

from textual_plotext import Plot, PlotextPlot


class ExamplesPane(VerticalScroll):
    """Base class for a pane of examples."""

    DEFAULT_CSS = """
    ExamplesPane Label {
        margin: 2;
        width: 1fr;
        text-align: center;
    }
    """

    def make_a(self, example: Callable[[Plot], None]) -> PlotextPlot:
        plot = PlotextPlot()
        example(plot.plot)
        return plot


class BasicPane(ExamplesPane):
    """Examples from the basic section of the Plotext documentation."""

    def scatter_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#scatter-plot"""
        y = plt.sin()
        plt.scatter(y)
        plt.title("Scatter Plot")

    def line_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#line-plot"""
        y = plt.sin()
        plt.plot(y)
        plt.title("Line Plot")

    def log_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#log-plot"""
        l = 10**4
        y = plt.sin(periods=2, length=l)
        plt.plot(y)
        plt.xscale("log")  # for logarithmic x scale
        plt.yscale("linear")  # for linear y scale
        plt.grid(0, 1)  # to add vertical grid lines
        plt.title("Logarithmic Plot")
        plt.xlabel("logarithmic scale")
        plt.ylabel("linear scale")

    def stem_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#stem-plot"""
        y = plt.sin()
        plt.plot(y, fillx=True)
        plt.title("Stem Plot")

    def multiple_data_sets(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-data-sets"""
        y1 = plt.sin()
        y2 = plt.sin(phase=-1)
        plt.plot(y1, label="plot")
        plt.scatter(y2, label="scatter")
        plt.title("Multiple Data Set")

    def multiple_axes_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-axes-plot"""
        y1 = plt.sin()
        y2 = plt.sin(2, phase=-1)
        plt.plot(y1, xside="lower", yside="left", label="lower left")
        plt.plot(y2, xside="upper", yside="right", label="upper right")
        plt.title("Multiple Axes Plot")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Label(
            "Examples from https://github.com/piccolomo/plotext/blob/master/readme/basic.md"
        )
        yield self.make_a(self.scatter_plot)
        yield Rule()
        yield self.make_a(self.line_plot)
        yield Rule()
        yield self.make_a(self.log_plot)
        yield Rule()
        yield self.make_a(self.stem_plot)
        yield Rule()
        yield self.make_a(self.multiple_data_sets)
        yield Rule()
        yield self.make_a(self.multiple_axes_plot)
        yield Rule()


class DemoApp(App[None]):
    """Demonstration application for the library."""

    CSS = """
    PlotextPlot {
        height: 40%
    }
    """

    TITLE = "textual-plotext Demonstration"

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        with TabbedContent():
            with TabPane("Basic Plots"):
                yield BasicPane()


if __name__ == "__main__":
    DemoApp().run()
