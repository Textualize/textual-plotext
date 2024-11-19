"""A longer-form example of using textual-plotext."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import cycle
from json import loads
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.message import Message
from textual.reactive import var
from textual.widgets import Footer, Header
from typing_extensions import Final

from textual_plotext import PlotextPlot

TEXTUAL_ICBM: Final[tuple[float, float]] = (55.9533, -3.1883)
"""The ICBM address of the approximate location of Textualize HQ."""


class Weather(PlotextPlot):
    """A widget for plotting weather data."""

    marker: var[str] = var("sd")
    """The type of marker to use for the plot."""

    def __init__(
        self,
        title: str,
        *,
        name: str | None = None,
        id: str | None = None,  # pylint:disable=redefined-builtin
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the weather widget.

        Args:
            name: The name of the weather widget.
            id: The ID of the weather widget in the DOM.
            classes: The CSS classes of the weather widget.
            disabled: Whether the weather widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._title = title
        self._unit = "Loading..."
        self._data: list[float] = []
        self._time: list[str] = []
        self.watch(self.app, "theme", lambda: self.call_after_refresh(self.replot))

    def on_mount(self) -> None:
        """Plot the data using Plotext."""
        self.plt.date_form("Y-m-d H:M")
        self.plt.title(self._title)
        self.plt.xlabel("Time")

    def replot(self) -> None:
        """Redraw the plot."""
        self.plt.clear_data()
        self.plt.ylabel(self._unit)
        self.plt.plot(self._time, self._data, marker=self.marker)

        self.refresh()

    def update(self, data: dict[str, Any], values: str) -> None:
        """Update the data for the weather plot.

        Args:
            data: The data from the weather API.
            values: The name of the values to plot.
        """
        self._data = data["hourly"][values]
        self._time = [moment.replace("T", " ") for moment in data["hourly"]["time"]]
        self._unit = data["hourly_units"][values]
        self.replot()

    def _watch_marker(self) -> None:
        """React to the marker being changed."""
        self.replot()


class TextualTowersWeatherApp(App[None]):
    """An application for showing recent Textualize weather."""

    CSS = """
    Grid {
        grid-size: 2;
    }

    Weather {
        padding: 1 2;
    }
    """

    TITLE = "Weather at Textual Towers Around a Year Ago"

    BINDINGS = [
        ("d", "app.toggle_dark", "Toggle light/dark mode"),
        ("m", "marker", "Cycle example markers"),
        ("q", "app.quit", "Quit the example"),
        ("[", "previous_theme", "Previous theme"),
        ("]", "next_theme", "Next theme"),
    ]

    MARKERS = {
        "dot": "Dot",
        "hd": "High Definition",
        "fhd": "Higher Definition",
        "braille": "Braille",
        "sd": "Standard Definition",
    }

    marker: var[str] = var("sd")
    """The marker used for each of the plots."""

    def __init__(self) -> None:
        """Initialise the application."""
        super().__init__()
        self._markers = cycle(self.MARKERS.keys())
        self.theme_names = [
            theme for theme in self.available_themes if theme != "textual-ansi"
        ]

    def compose(self) -> ComposeResult:
        """Compose the display of the example app."""
        yield Header()
        with Grid():
            yield Weather("Temperature", id="temperature")
            yield Weather("Wind Speed (10m)", id="windspeed")
            yield Weather("Precipitation", id="precipitation")
            yield Weather("Surface Pressure", id="pressure")
        yield Footer()

    def on_mount(self) -> None:
        """Start the process of gathering the weather data."""
        self.gather_weather()

    @dataclass
    class WeatherData(Message):
        """Message posted once the weather data has been gathered."""

        history: dict[str, Any]
        """The history data gathered from the weather API."""

    @work(thread=True, exclusive=True)
    def gather_weather(self) -> None:
        """Worker thread that gathers historical weather data."""
        end_date = (
            datetime.now() - timedelta(days=365) + timedelta(weeks=1)
        )  # Yes, yes, I know. It's just an example.
        start_date = end_date - timedelta(weeks=2)  # Two! Weeks!
        try:
            with urlopen(
                Request(
                    "https://archive-api.open-meteo.com/v1/archive?"
                    f"latitude={TEXTUAL_ICBM[0]}&longitude={TEXTUAL_ICBM[1]}"
                    f"&start_date={start_date.strftime('%Y-%m-%d')}"
                    f"&end_date={end_date.strftime('%Y-%m-%d')}"
                    "&hourly=temperature_2m,precipitation,surface_pressure,windspeed_10m"
                )
            ) as result:
                self.post_message(
                    self.WeatherData(loads(result.read().decode("utf-8")))
                )
        except URLError as error:
            self.notify(
                str(error),
                title="Error loading weather data",
                severity="error",
                timeout=6,
            )

    @on(WeatherData)
    def populate_plots(self, event: WeatherData) -> None:
        """Populate the weather plots with data received from the API.

        Args:
            event: The weather data reception event.
        """
        with self.batch_update():
            self.query_one("#temperature", Weather).update(
                event.history, "temperature_2m"
            )
            self.query_one("#windspeed", Weather).update(event.history, "windspeed_10m")
            self.query_one("#precipitation", Weather).update(
                event.history, "precipitation"
            )
            self.query_one("#pressure", Weather).update(
                event.history, "surface_pressure"
            )

    def watch_marker(self) -> None:
        """React to the marker type being changed."""
        self.sub_title = self.MARKERS[self.marker]
        for plot in self.query(Weather).results(Weather):
            plot.marker = self.marker

    def action_marker(self) -> None:
        """Cycle to the next marker type."""
        self.marker = next(self._markers)

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
    TextualTowersWeatherApp().run()
