from textual.app import App, ComposeResult

from textual_plotext import PlotextPlot


class ScatterApp(App[None]):
    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        plt.title("Scatter Plot")
        plt.scatter(plt.sin())


if __name__ == "__main__":
    ScatterApp().run()
