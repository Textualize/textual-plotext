"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

from __future__ import annotations

import random
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Label, Rule, TabbedContent, TabPane

from textual_plotext import PlotextPlot


class ExamplesPane(VerticalScroll):
    """Base class for a pane of examples."""

    DEFAULT_CSS = """
    ExamplesPane Label {
        margin: 2;
        width: 1fr;
        text-align: center;
    }
    """

    def examples(self, source: str, examples: list[PlotextPlot]) -> ComposeResult:
        yield Label(
            f"Examples taken from https://github.com/piccolomo/plotext/blob/master/readme/{source}.md"
        )
        for example in examples:
            yield example
            yield Rule()


class BasicPlots(ExamplesPane):
    """Examples from the basic section of the Plotext documentation."""

    class ScatterPlot(PlotextPlot):
        def plot(self) -> None:
            """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#scatter-plot"""
            y = self.plt.sin()
            self.plt.scatter(y)
            self.plt.title("Scatter Plot")

    class LinePlot(PlotextPlot):
        def plot(self) -> None:
            """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#line-plot"""
            y = self.plt.sin()
            self.plt.plot(y)
            self.plt.title("Line Plot")

    class LogPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#log-plot"""

        def plot(self) -> None:
            l = 10**4
            y = self.plt.sin(periods=2, length=l)
            self.plt.plot(y)
            self.plt.xscale("log")  # for logarithmic x scale
            self.plt.yscale("linear")  # for linear y scale
            self.plt.grid(0, 1)  # to add vertical grid lines
            self.plt.title("Logarithmic Plot")
            self.plt.xlabel("logarithmic scale")
            self.plt.ylabel("linear scale")

    class StemPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#stem-plot"""

        def plot(self) -> None:
            y = self.plt.sin()
            self.plt.plot(y, fillx=True)
            self.plt.title("Stem Plot")

    class MultipleDataSets(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-data-sets"""

        def plot(self) -> None:
            y1 = self.plt.sin()
            y2 = self.plt.sin(phase=-1)
            self.plt.plot(y1, label="plot")
            self.plt.scatter(y2, label="scatter")
            self.plt.title("Multiple Data Set")

    class MultipleAxesPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/basic.md#multiple-axes-plot"""

        def plot(self) -> None:
            y1 = self.plt.sin()
            y2 = self.plt.sin(2, phase=-1)
            self.plt.plot(y1, xside="lower", yside="left", label="lower left")
            self.plt.plot(y2, xside="upper", yside="right", label="upper right")
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

        def plot(self) -> None:
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            percentages = [14, 36, 11, 8, 7, 4]
            self.plt.bar(pizzas, percentages)
            self.plt.title("Most Favored Pizzas in the World")

    class HorizontalBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#horizontal-bar-plot"""

        def plot(self) -> None:
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            percentages = [14, 36, 11, 8, 7, 4]
            self.plt.bar(
                pizzas, percentages, orientation="horizontal", width=3 / 5
            )  # or in short orientation = 'h'
            self.plt.title("Most Favoured Pizzas in the World")

    class MultipleBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#multiple-bar-plot"""

        def plot(self) -> None:
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            male_percentages = [14, 36, 11, 8, 7, 4]
            female_percentages = [12, 20, 35, 15, 2, 1]
            self.plt.multiple_bar(
                pizzas, [male_percentages, female_percentages]
            )  # , labels = ["men", "women"])
            self.plt.title("Most Favored Pizzas in the World by Gender")

    class StackedBarPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#stacked-bar-plot"""

        def plot(self) -> None:
            pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
            male_percentages = [14, 36, 11, 8, 7, 4]
            female_percentages = [12, 20, 35, 15, 2, 1]
            self.plt.stacked_bar(
                pizzas, [male_percentages, female_percentages]
            )  # , labels = ["men", "women"])
            self.plt.title("Most Favored Pizzas in the World by Gender")

    # def box_plot(self, plt: Plot) -> None:
    #     """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#box-plot"""
    #     labels = ["apple", "orange", "pear", "banana"]
    #     datas = [
    #         [1,2,3,5,10,8],
    #         [4,9,6,12,20,13],
    #         [1,2,3,4,5,6],
    #         [3,9,12,16,9,8,3,7,2]
    #     ]

    #     plt.box(labels, datas, width=0.3)
    #     plt.title("The weight of the fruit")

    class HistogramPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#histogram-plot"""

        def plot(self) -> None:
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
                # self.boxplot(),
                self.HistogramPlot(),
            ],
        )


class SpecialPlots(ExamplesPane):
    """Examples from the special plots section of the Plotext documentation."""

    class ErrorPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#error-plot"""

        def plot(self) -> None:
            l = 20
            n = 1
            ye = [random.random() * n for _ in range(l)]
            xe = [random.random() * n for _ in range(l)]
            y = self.plt.sin(length=l)
            self.plt.error(y, xerr=xe, yerr=ye)
            self.plt.title("Error Plot")

    class EventPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#event-plot"""

        def plot(self) -> None:
            self.plt.date_form("H:M")  # also just "H" looks ok
            times = [
                datetime(
                    2022,
                    3,
                    27,
                    random.randint(0, 23),
                    random.randint(0, 59),
                    random.randint(0, 59),
                )
                for _ in range(100)
            ]  # A random list of times during the day
            times = self.plt.datetimes_to_string(times)
            self.plt.event_plot(times)

    class StreamingDataPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#streaming-data"""

        def on_mount(self) -> None:
            self.frame = 0
            self.auto_refresh = 0.25

        def plot(self) -> None:
            self.plt.title("Streaming Data")
            self.plt.scatter(
                self.plt.sin(periods=2, length=1_000, phase=(2 * self.frame) / 50)
            )
            self.frame += 1

    class MatrixPlot(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#matrix-plot"""

        def plot(self) -> None:
            cols, rows = 200, 45
            p = 1
            matrix = [
                [(abs(r - rows / 2) + abs(c - cols / 2)) ** p for c in range(cols)]
                for r in range(rows)
            ]
            self.plt.matrix_plot(matrix)
            self.plt.plotsize(cols, rows)
            self.plt.title("Matrix Plot")

    class ConfusionMatrix(PlotextPlot):
        """https://github.com/piccolomo/plotext/blob/master/readme/special.md#confusion-matrix"""

        def plot(self) -> None:
            l = 300
            actual = [random.randrange(0, 4) for _ in range(l)]
            predicted = [random.randrange(0, 4) for _ in range(l)]
            labels = ["Autumn", "Spring", "Summer", "Winter"]
            self.plt.cmatrix(actual, predicted, labels)

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        return self.examples(
            "special",
            [
                self.ErrorPlot(),
                self.EventPlot(),
                self.StreamingDataPlot(),
                self.MatrixPlot(),
                self.ConfusionMatrix(),
            ],
        )


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
                yield BasicPlots()
            with TabPane("Bar Plots"):
                yield BarPlots()
            with TabPane("Special Plots"):
                yield SpecialPlots()


if __name__ == "__main__":
    DemoApp().run()
