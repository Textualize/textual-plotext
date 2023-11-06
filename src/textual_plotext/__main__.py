"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

# The following code borrows heavily from the Plotext readme files, and as
# such has some variables names and the like that would generally annoy
# pylint; so here we ask pylint to ease up for this particular file.
#
# Also, because it's common with Textual to introduce a property in
# `on_mount`, we ask pylint to ease up on that too.
#
# pylint:disable=invalid-name, attribute-defined-outside-init

from __future__ import annotations

import os
import random
from datetime import datetime
from itertools import chain, cycle

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Label, Rule, TabbedContent, TabPane

from textual_plotext import PlotextPlot


class ExamplesPane(VerticalScroll):
    """Base class for a pane of examples."""

    DEFAULT_CSS = """
    ExamplesPane {
        scrollbar-gutter: stable;
    }

    ExamplesPane Label {
        margin: 2;
        width: 1fr;
        text-align: center;
    }
    """

    def examples(self, source: str, examples: list[PlotextPlot]) -> ComposeResult:
        """Provide the composed examples.

        Args:
            source: The source for the examples within the Plotext readme files.
            examples: A list of the example widgets.
        """
        yield Label(
            "Examples taken from https://github.com/piccolomo/"
            f"plotext/blob/master/readme/{source}.md"
        )
        for example in examples:
            yield example
            yield Rule()


class BasicPlots(ExamplesPane):
    """Examples from the basic section of the Plotext documentation."""

    class ScatterPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#scatter-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.scatter(self.plt.sin())
            self.plt.title("Scatter Plot")

    class LinePlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#line-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.plot(self.plt.sin())
            self.plt.title("Line Plot")

    class LogPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#log-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.plot(self.plt.sin(periods=2, length=10**4))
            self.plt.xscale("log")
            self.plt.yscale("linear")
            self.plt.grid(0, 1)
            self.plt.title("Logarithmic Plot")
            self.plt.xlabel("logarithmic scale")
            self.plt.ylabel("linear scale")
            # A slightly hacky workaround for what seems to be a bug in
            # Plotext itself when it comes to log scales. We force a build
            # of the data...
            _ = self.plt.build()
            # ...then put the scale back to linear so it doesn't try and
            # apply log again and again on each render.
            self.plt.xscale("linear")

    class StemPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#stem-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.plot(self.plt.sin(), fillx=True)
            self.plt.title("Stem Plot")

    class MultipleDataSets(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-data-sets"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.plot(self.plt.sin(), label="plot")
            self.plt.scatter(self.plt.sin(phase=-1), label="scatter")
            self.plt.title("Multiple Data Set")

    class MultipleAxesPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-axes-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.plot(
                self.plt.sin(), xside="lower", yside="left", label="lower left"
            )
            self.plt.plot(
                self.plt.sin(2, phase=-1),
                xside="upper",
                yside="right",
                label="upper right",
            )
            self.plt.title("Multiple Axes Plot")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        return self.examples(
            "basic",
            [
                self.ScatterPlot(),
                self.LinePlot(),
                self.LogPlot(),
                self.StemPlot(),
                self.MultipleDataSets(),
                self.MultipleAxesPlot(),
            ],
        )


class BarPlots(ExamplesPane):
    """Examples from the bar plots section of the Plotext documentation."""

    class VerticalBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#vertical-bar-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            percentages = [14, 36, 11, 8, 7, 4]
            self.plt.bar(pizzas, percentages)
            self.plt.title("Most Favored Pizzas in the World")

    class HorizontalBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#horizontal-bar-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            percentages = [14, 36, 11, 8, 7, 4]
            self.plt.bar(
                pizzas, percentages, orientation="horizontal", width=3 / 5
            )  # or in short orientation = 'h'
            self.plt.title("Most Favoured Pizzas in the World")

    class MultipleBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#multiple-bar-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            male_percentages = [14, 36, 11, 8, 7, 4]
            female_percentages = [12, 20, 35, 15, 2, 1]
            self.plt.multiple_bar(
                pizzas, [male_percentages, female_percentages]
            )  # , labels = ["men", "women"])
            self.plt.title("Most Favored Pizzas in the World by Gender")

    class StackedBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#stacked-bar-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            male_percentages = [14, 36, 11, 8, 7, 4]
            female_percentages = [12, 20, 35, 15, 2, 1]
            self.plt.stacked_bar(
                pizzas, [male_percentages, female_percentages]
            )  # , labels = ["men", "women"])
            self.plt.title("Most Favored Pizzas in the World by Gender")

    class HistogramPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#histogram-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            l = 7 * 10**4
            data1 = [random.gauss(0, 1) for _ in range(10 * l)]
            data2 = [random.gauss(3, 1) for _ in range(6 * l)]
            data3 = [random.gauss(6, 1) for _ in range(4 * l)]
            bins = 60
            self.plt.hist(data1, bins, label="mean 0")
            self.plt.hist(data2, bins, label="mean 3")
            self.plt.hist(data3, bins, label="mean 6")
            self.plt.title("Histogram Plot")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        return self.examples(
            "bar",
            [
                self.VerticalBarPlot(),
                self.HorizontalBarPlot(),
                self.MultipleBarPlot(),
                self.StackedBarPlot(),
                self.HistogramPlot(),
            ],
        )


class SpecialPlots(ExamplesPane):
    """Examples from the special plots section of the Plotext documentation."""

    class ErrorPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#error-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            l = 20
            ye = [random.random() for _ in range(l)]
            xe = [random.random() for _ in range(l)]
            data = self.plt.sin(length=l)
            self.plt.error(data, xerr=xe, yerr=ye)
            self.plt.title("Error Plot")

    class EventPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#event-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.date_form("H:M")
            times = self.plt.datetimes_to_string(
                [
                    datetime(
                        2022,
                        3,
                        27,
                        random.randint(0, 23),
                        random.randint(0, 59),
                        random.randint(0, 59),
                    )
                    for _ in range(100)
                ]
            )
            self.plt.event_plot(times)

    class StreamingDataPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#streaming-data"""

        def on_mount(self) -> None:
            """Set up the initial conditions for the 'streaming' data."""
            self.frame = 0
            self.plt.title("Streaming Data")
            self.set_interval(0.25, self.plot)

        def plot(self) -> None:
            """Plot the current frame of the stream."""
            self.plt.clear_data()
            self.plt.scatter(
                self.plt.sin(periods=2, length=1_000, phase=(2 * self.frame) / 50)
            )
            self.refresh()
            self.frame += 1

    class MatrixPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#matrix-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.title("Matrix Plot")

        def on_resize(self) -> None:
            """Remake the data when the size changes."""
            p = 1
            matrix = [
                [
                    (abs(r - self.size.height / 2) + abs(c - self.size.width / 2)) ** p
                    for c in range(self.size.width)
                ]
                for r in range(self.size.height)
            ]
            self.plt.clear_data()
            self.plt.matrix_plot(matrix)

    class ConfusionMatrix(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#confusion-matrix"""

        def on_mount(self) -> None:
            """Set up the plot."""
            l = 300
            actual = [random.randrange(0, 4) for _ in range(l)]
            predicted = [random.randrange(0, 4) for _ in range(l)]
            labels = ["Autumn", "Spring", "Summer", "Winter"]
            self.plt.cmatrix(actual, predicted, labels=labels)

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        return self.examples(
            "special",
            [
                self.ErrorPlot(),
                *([] if os.name == "nt" else [self.EventPlot()]),
                self.StreamingDataPlot(),
                self.MatrixPlot(),
                self.ConfusionMatrix(),
            ],
        )


class DecoratorPlots(ExamplesPane):
    """Examples from the decorator plots section of the Plotext documentation."""

    class LinePlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/decorator.md#line-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.scatter(self.plt.sin())
            self.plt.title("Extra Lines")
            self.plt.vline(100, "magenta")
            self.plt.hline(0.5, "blue+")
            self.plt.plotsize(100, 30)

    class TextPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/decorator.md#text-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            percentages = [14, 36, 11, 8, 7, 4]
            self.plt.bar(pizzas, percentages)
            self.plt.title("Labelled Bar Plot using Text()")
            for i, pizza in enumerate(pizzas):
                self.plt.text(
                    pizza,
                    x=i + 1,
                    y=percentages[i] + 1.5,
                    alignment="center",
                    color="red",
                )
            self.plt.ylim(0, 38)

    class ShapePlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/decorator.md#shape-plot"""

        def on_mount(self) -> None:
            """Set up the plot."""
            self.plt.title("Shapes")
            self.plt.polygon()
            self.plt.rectangle()
            self.plt.polygon(sides=100)  # to simulate a circle
            self.plt.show()

    class PulsePlot(PlotextPlot):
        """I made this one up myself."""

        def on_mount(self) -> None:
            """Set up the pulsing polygon example."""
            self.plt.title("Pulse")
            self.steps = cycle(chain(range(3, 21), range(20, 2, -1)))
            self.set_interval(0.5, self.plot)

        def plot(self) -> None:
            """Plot a polygon with a changing number of sides."""
            self.plt.clear_data()
            self.plt.polygon(sides=next(self.steps))
            self.refresh()

    def compose(self) -> ComposeResult:
        return self.examples(
            "decorator",
            [self.LinePlot(), self.TextPlot(), self.ShapePlot(), self.PulsePlot()],
        )


class DemoApp(App[None]):
    """Demonstration application for the library."""

    CSS = """
    PlotextPlot {
        height: 40%
    }

    ShapePlot, PulsePlot {
        height: 100%;
    }
    """

    TITLE = "textual-plotext Demonstration"

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        with TabbedContent():
            with TabPane("Basic Plots"):
                yield BasicPlots()
            with TabPane("Bar Plots"):
                yield BarPlots()
            with TabPane("Special Plots"):
                yield SpecialPlots()
            with TabPane("Decorator Plots"):
                yield DecoratorPlots()


if __name__ == "__main__":
    DemoApp().run()
