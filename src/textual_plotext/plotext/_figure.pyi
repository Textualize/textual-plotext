"""Type hints for the methods of the Plotext _figure_class class.

NOTE: Some of the work in here is guesswork. There are no type hints inside
Plotext's code (hence this stub file), and it's not always clear from the
Plotext code what the type of any given parameter on any given method is.

Corrections are most welcome!

ALSO NOTE: For the moment this is simply for support while developing
textual-plotext; but this could turn into something that provides more
general support for the type-hinting of Plotext.
"""

from __future__ import annotations

from typing import Any, Sequence, Tuple, Union
from typing_extensions import Literal, TypeAlias

from datetime import datetime

Alignment: TypeAlias = Literal["left", "center", "right", "top", "bottom", "dynamic"]
Color: TypeAlias = Union[str, int, Tuple[int, int, int]]
Orientation: TypeAlias = Literal["horizontal", "vertical"]

class _figure_class:
    ############################################################################
    # External Set Functions
    def title(self, title: str | None = None) -> None: ...
    def xlabel(self, label: str | None = None, xside: str | None = None) -> None: ...
    def ylabel(self, label: str | None = None, xside: str | None = None) -> None: ...
    def xlim(
        self,
        left: float | None = None,
        right: float | None = None,
        xside: float | None = None,
    ) -> None: ...
    def ylim(
        self,
        lower: float | None = None,
        upper: float | None = None,
        yside: float | None = None,
    ) -> None: ...
    def xscale(self, scale: str | None = None, xside: str | None = None) -> None: ...
    def yscale(self, scale: str | None = None, yside: str | None = None) -> None: ...
    def xticks(
        self,
        ticks: list[float] | None = None,
        labels: list[str] | None = None,
        xside: float | None = None,
    ) -> None: ...
    def yticks(
        self,
        ticks: list[float] | None = None,
        labels: list[str] | None = None,
        yside: float | None = None,
    ) -> None: ...
    def xfrequency(
        self, frequency: float | None = None, xside: float | None = None
    ) -> None: ...
    def yfrequency(
        self, frequency: float | None = None, yside: float | None = None
    ) -> None: ...
    def xreverse(
        self, reverse: bool | None = None, xside: float | None = None
    ) -> None: ...
    def yreverse(
        self, reverse: bool | None = None, yside: float | None = None
    ) -> None: ...
    def xaxes(
        self, lower: bool | int | None = None, upper: bool | int | None = None
    ) -> None: ...
    def yaxes(
        self, left: bool | int | None = None, right: bool | int | None = None
    ) -> None: ...
    def frame(self, frame: bool | int | None = None) -> None: ...
    def grid(
        self, horizontal: bool | int | None = None, vertical: bool | int | None = None
    ) -> None: ...
    def canvas_color(self, color: Color | None = None) -> None: ...
    def axes_color(self, color: Color | None = None) -> None: ...
    def ticks_color(self, color: Color | None = None) -> None: ...
    def ticks_style(self, style: Color | None = None) -> None: ...
    def theme(self, theme: str | None = None) -> None: ...

    # Clear Functions
    def clear_figure(self) -> None: ...
    def clf(self) -> None: ...
    def clear_data(self) -> None: ...
    def cld(self) -> None: ...
    def clear_color(self) -> None: ...
    def clc(self) -> None: ...
    def clear_terminal(self, lines: int | None = None) -> None: ...
    def clr(self, lines: int | None = None) -> None: ...

    ############################################################################
    # Plot Functions
    def scatter(
        self,
        *args: Sequence[Any],
        marker: str | None = None,
        color: Color | None = None,
        style: str | None = None,
        fillx: float | bool | str | None = None,
        filly: float | bool | str | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def plot(
        self,
        *args: Sequence[Any],
        marker: str | None = None,
        color: Color | None = None,
        style: str | None = None,
        fillx: float | bool | str | None = None,
        filly: float | bool | str | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def bar(
        self,
        *args: Sequence[Any],
        xside=None,
        yside=None,
        marker: str | None = None,
        color: Color | None = None,
        fill: bool | None = None,
        width: float | None = None,
        orientation: Orientation | None = None,
        label=None,
        minimum: float | None = None,
        reset_ticks: bool | None = None,
    ) -> None: ...
    def multiple_bar(
        self,
        *args: Sequence[Any],
        xside=None,
        yside=None,
        marker: str | None = None,
        color: Color | None = None,
        fill: bool | None = None,
        width: float | None = None,
        orientation: Orientation | None = None,
        label: str | None = None,
        minimum: float | None = None,
        reset_ticks: bool | None = None,
    ) -> None: ...
    def stacked_bar(
        self,
        *args: Sequence[Any],
        xside=None,
        yside=None,
        marker: str | None = None,
        color: Color | None = None,
        fill: bool | None = None,
        width: float | None = None,
        orientation: Orientation | None = None,
        label: str | None = None,
        minimum: float | None = None,
        reset_ticks: bool | None = None,
    ) -> None: ...
    def hist(
        self,
        data: Sequence[Any],
        bins: int | None = None,
        marker: str | None = None,
        color: Color | None = None,
        fill: bool | None = None,
        norm=None,
        width: float | None = None,
        orientation: Orientation | None = None,
        minimum: float | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def candlestick(
        self,
        dates,
        data,
        colors=None,
        orientation: Orientation | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...

    ############################################################################
    # Plotting Tools
    def error(
        self,
        *args: Sequence[Any],
        xerr: Sequence[float] | None = None,
        yerr: Sequence[float] | None = None,
        color: Color | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def event_plot(
        self,
        data: Sequence[str],
        marker: str | None = None,
        color: Color | None = None,
        orientation: Orientation | None = None,
        side: str | None = None,
    ) -> None: ...
    def eventplot(
        self,
        data: Sequence[str],
        marker: str | None = None,
        color: Color | None = None,
        orientation: Orientation | None = None,
        side: str | None = None,
    ) -> None: ...
    def vertical_line(
        self, coordinate: float, color: Color | None = None, xside: str | None = None
    ) -> None: ...
    def vline(
        self, coordinate: float, color: Color | None = None, xside: str | None = None
    ) -> None: ...
    def horizontal_line(
        self, coordinate: float, color: Color | None = None, yside: str | None = None
    ) -> None: ...
    def hline(
        self, coordinate: float, color: Color | None = None, yside: str | None = None
    ) -> None: ...
    def text(
        self,
        text: str,
        x: float | None = None,
        y: float | None = None,
        color: Color | None = None,
        background: Color | None = None,
        style: str | None = None,
        orientation: Orientation | None = None,
        alignment: Alignment | None = None,
        xside: str | None = None,
        yside: str | None = None,
    ) -> None: ...
    def rectangle(
        self,
        x: float | None = None,
        y: float | None = None,
        marker: str | None = None,
        color: Color | None = None,
        lines: bool | None = None,
        fill: bool | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def polygon(
        self,
        x: float | None = None,
        y: float | None = None,
        radius: float | None = None,
        sides: int | None = None,
        marker: str | None = None,
        color: Color | None = None,
        lines: bool | None = None,
        fill: bool | None = None,
        xside: str | None = None,
        yside: str | None = None,
        label: str | None = None,
    ) -> None: ...
    def confusion_matrix(  # TODO
        self,
        actual,
        predicted,
        color: Color | None = None,
        style: str | None = None,
        labels=None,
    ) -> None: ...
    def cmatrix(  # TODO
        self,
        actual,
        predicted,
        color: Color | None = None,
        style: str | None = None,
        labels=None,
    ) -> None: ...
    def indicator(  # TODO
        self,
        value,
        label: str | None = None,
        color: Color | None = None,
        style: str | None = None,
    ) -> None: ...

    ############################################################################
    # 2D Plots
    def matrix_plot(  # TODO
        self, matrix, marker: str | None = None, style: str | None = None, fast=False
    ) -> None: ...
    def image_plot(  # TODO
        self,
        path,
        marker: str | None = None,
        style: str | None = None,
        fast=False,
        grayscale=False,
    ) -> None: ...

    ############################################################################
    # Date Functions
    def date_form(  # TODO
        self, input_form: str | None = None, output_form: str | None = None
    ) -> None: ...
    def set_time0(self, string: str, input_form: str | None = None) -> None: ...  # TODO
    def today_datetime(self) -> datetime: ...  # TODO
    def today_string(self, output_form: str | None = None) -> str: ...  # TODO
    def datetime_to_string(  # TODO
        self, datetime: datetime, output_form: str | None = None
    ) -> str: ...
    def datetimes_to_string(  # TODO
        self, datetimes: Sequence[datetime], output_form: str | None = None
    ) -> list[str]: ...
    def string_to_datetime(  # TODO
        self, string: str, input_form: str | None = None
    ) -> datetime: ...
    def string_to_time(  # TODO
        self, string: str, input_form: str | None = None
    ) -> datetime: ...
    def strings_to_time(  # TODO
        self, string: Sequence[str], input_form: str | None = None
    ) -> datetime: ...

    ############################################################################
    # Build Functions
    def build(self) -> str: ...

    ############################################################################
    # Externally Called Utility
    def plot_size(  # TODO
        self, width: int | None = None, height: int | None = None
    ) -> None: ...
    def plotsize(
        self, width: int | None = None, height: int | None = None
    ) -> None: ...  # TODO
