"""A small self-contained example of a Plotext plot in a Textual app."""

from textual import on
from textual.app import App, ComposeResult
from textual.events import Mount

from textual_plotext import PlotextPlot


class ScatterApp(App[None]):
    """Example Textual application showing a Plotext plot."""

    BINDINGS = [
        ("[", "previous_theme", "Previous theme"),
        ("]", "next_theme", "Next theme"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.theme_names = [
            theme for theme in self.available_themes if theme != "textual-ansi"
        ]
        self.watch(self.app, "theme", lambda: self.call_after_refresh(self.replot))

    def compose(self) -> ComposeResult:
        """Compose the plotting widget."""
        yield PlotextPlot()

    @on(Mount)
    def replot(self) -> None:
        """Set up the plot."""
        plt = self.query_one(PlotextPlot).plt
        plt.clear_figure()
        plt.clear_data()
        plt.title("Scatter Plot")
        plt.scatter(plt.sin())
        self.refresh()

    def action_next_theme(self) -> None:
        themes = self.theme_names
        index = themes.index(self.current_theme.name)
        self.theme = themes[(index + 1) % len(themes)]
        self.notify_new_theme(self.current_theme.name)

    def action_previous_theme(self) -> None:
        themes = self.theme_names
        index = themes.index(self.current_theme.name)
        self.theme = themes[(index - 1) % len(themes)]
        self.notify_new_theme(self.current_theme.name)

    def notify_new_theme(self, theme_name: str) -> None:
        self.clear_notifications()
        self.notify(
            title="Theme updated",
            message=f"Theme is {theme_name}.",
        )


if __name__ == "__main__":
    ScatterApp().run()
