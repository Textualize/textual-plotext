"""A small self-contained example of a Plotext plot in a Textual app."""

from textual.app import App, ComposeResult

from textual_plotext import PlotextPlot


class ScatterApp(App[None]):
    """Example Textual application showing a Plotext plot."""

    def compose(self) -> ComposeResult:
        """Compose the plotting widget."""
        yield PlotextPlot()

    def on_mount(self) -> None:
        """Set up the plot."""
        plt = self.query_one(PlotextPlot).plt
        plt.title("Scatter Plot")
        plt.scatter(plt.sin())


if __name__ == "__main__":
    ScatterApp().run()
