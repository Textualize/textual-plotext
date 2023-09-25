"""A longer-form example of using textual-plotext."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import cycle
from json import loads
from typing import Any
from typing_extensions import Final
from urllib.request import Request, urlopen

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Header, Footer

from textual_plotext import PlotextPlot

TEXTUAL_ICBM: Final[tuple[float, float]] = (55.9533, -3.1883)
"""The ICBM address of the approximate location of Textualize HQ."""


class Weather(PlotextPlot):
    """A widget for plotting weather data."""

    marker: reactive[str] = reactive("sd")

    def __init__(
        self,
        title: str,
        *,
        name: str | None = None,
        id: str | None = None,
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
        self._unit = "?"
        self._data: list[float] = []
        self._time: list[str] = []

    def update(self, data: dict[str, Any], values: str) -> None:
        """Update the data for the weather plot.

        Args:
            data: The data from the weather API.
            values: The name of the values to plot.
        """
        self._data = data["hourly"][values]
        self._time = [moment.replace("T", " ") for moment in data["hourly"]["time"]]
        self._unit = data["hourly_units"][values]
        self.refresh()

    def plot(self) -> None:
        """Plot the data using Plotext."""
        self.plt.date_form("Y-m-d H:M")
        self.plt.title(self._title)
        self.plt.ylabel(self._unit)
        self.plt.xlabel("Time")
        self.plt.plot(self._time, self._data, marker=self.marker)


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
        self._markers = cycle(("dot", "hd", "fhd", "braille", "sd"))
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
        self.post_message(
            self.WeatherData(
                loads(
                    urlopen(
                        Request(
                            "https://archive-api.open-meteo.com/v1/archive?"
                            f"latitude={TEXTUAL_ICBM[0]}&longitude={TEXTUAL_ICBM[1]}"
                            f"&start_date={start_date.strftime('%Y-%m-%d')}"
                            f"&end_date={end_date.strftime('%Y-%m-%d')}"
                            "&hourly=temperature_2m,precipitation,surface_pressure,windspeed_10m"
                        )
                    )
                    .read()
                    .decode("utf-8")
                )
            )
        )

    @on(WeatherData)
    def populate_plots(self, event: WeatherData) -> None:
        """Populate the weather plots with data received from the API.

        Args:
            event: The weather data reception event.
        """
        self.query_one("#temperature", Weather).update(event.history, "temperature_2m")
        self.query_one("#windspeed", Weather).update(event.history, "windspeed_10m")
        self.query_one("#precipitation", Weather).update(event.history, "precipitation")
        self.query_one("#pressure", Weather).update(event.history, "surface_pressure")

    def action_marker(self) -> None:
        """Cycle to the next marker type."""
        marker = next(self._markers)
        for plot in self.query(Weather):
            plot.marker = marker


if __name__ == "__main__":
    TextualTowersWeatherApp().run()
