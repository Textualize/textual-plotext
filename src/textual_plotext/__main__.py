"""Main entry point for the library.

When run as:

```sh
$ python -m textual_plotext
```

it will show a demonstration of the library in action.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from textual_plotext import PlotextPlot


class DemoApp(App[None]):
    """Demonstration application for the library."""

    CSS = """
    PlotextPlot {
        border: solid cornflowerblue;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        yield PlotextPlot()
        yield Footer()


if __name__ == "__main__":
    DemoApp().run()
