"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

from __future__ import annotations

import random
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

    def examples(
        self, source: str, examples: list[Callable[[Plot], None]]
    ) -> ComposeResult:
        yield Label(
            f"Examples taken from https://github.com/piccolomo/plotext/blob/master/readme/{source}.md"
        )
        for example in examples:
            yield self.make_a(example)
            yield Rule()


class BasicPlots(ExamplesPane):
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
        return self.examples(
            "basic",
            [
                self.scatter_plot,
                self.line_plot,
                self.log_plot,
                self.stem_plot,
                self.multiple_data_sets,
                self.multiple_axes_plot,
            ],
        )


class BarPlots(ExamplesPane):
    """Examples from the bar plots section of the Plotext documentation."""

    def vertical_bar_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#vertical-bar-plot"""
        pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
        percentages = [14, 36, 11, 8, 7, 4]
        plt.bar(pizzas, percentages)
        plt.title("Most Favored Pizzas in the World")

    def horizontal_bar_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#horizontal-bar-plot"""
        pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
        percentages = [14, 36, 11, 8, 7, 4]
        plt.bar(
            pizzas, percentages, orientation="horizontal", width=3 / 5
        )  # or in short orientation = 'h'
        plt.title("Most Favoured Pizzas in the World")

    def multiple_bar_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#multiple-bar-plot"""
        pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
        male_percentages = [14, 36, 11, 8, 7, 4]
        female_percentages = [12, 20, 35, 15, 2, 1]
        plt.multiple_bar(
            pizzas, [male_percentages, female_percentages]
        )  # , labels = ["men", "women"])
        plt.title("Most Favored Pizzas in the World by Gender")

    def stacked_bar_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#stacked-bar-plot"""
        pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
        male_percentages = [14, 36, 11, 8, 7, 4]
        female_percentages = [12, 20, 35, 15, 2, 1]
        plt.stacked_bar(
            pizzas, [male_percentages, female_percentages]
        )  # , labels = ["men", "women"])
        plt.title("Most Favored Pizzas in the World by Gender")

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

    def histogram_plot(self, plt: Plot) -> None:
        """https://github.com/piccolomo/plotext/blob/master/readme/bar.md#histogram-plot"""
        l = 7 * 10**4
        data1 = [random.gauss(0, 1) for _ in range(10 * l)]
        data2 = [random.gauss(3, 1) for _ in range(6 * l)]
        data3 = [random.gauss(6, 1) for _ in range(4 * l)]
        bins = 60
        plt.hist(data1, bins, label="mean 0")
        plt.hist(data2, bins, label="mean 3")
        plt.hist(data3, bins, label="mean 6")
        plt.title("Histogram Plot")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        return self.examples(
            "bar",
            [
                self.vertical_bar_plot,
                self.horizontal_bar_plot,
                self.multiple_bar_plot,
                self.stacked_bar_plot,
                # self.box_plot,
                self.histogram_plot,
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


if __name__ == "__main__":
    DemoApp().run()
