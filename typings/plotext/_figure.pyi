"""Type hints for the methods of the Plotext _figure_class class.

NOTE: Some of the work in here is guesswork. There are no type hints inside
Plotext's code (hence this stub file), and it's not always clear from the
Plotext code what the type of any given parameter on any given method is.

Corrections are most welcome!
"""

from __future__ import annotations

from typing import Tuple, Union
from typing_extensions import TypeAlias

from datetime import datetime

Color: TypeAlias = Union[str, int, Tuple[int, int, int]]

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
        *args,
        marker=None,
        color=None,
        style=None,
        fillx=None,
        filly=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def plot(
        self,
        *args,
        marker=None,
        color=None,
        style=None,
        fillx=None,
        filly=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def bar(
        self,
        *args,
        marker=None,
        color=None,
        fill=None,
        width=None,
        orientation=None,
        minimum=None,
        reset_ticks=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def multiple_bar(
        self,
        *args,
        marker=None,
        color=None,
        fill=None,
        width=None,
        orientation=None,
        minimum=None,
        reset_ticks=None,
        xside=None,
        yside=None,
        labels=None,
    ) -> None: ...
    def stacked_bar(
        self,
        *args,
        marker=None,
        color=None,
        fill=None,
        width=None,
        orientation=None,
        minimum=None,
        reset_ticks=None,
        xside=None,
        yside=None,
        labels=None,
    ) -> None: ...
    def hist(
        self,
        data,
        bins=None,
        marker=None,
        color=None,
        fill=None,
        norm=None,
        width=None,
        orientation=None,
        minimum=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def candlestick(
        self,
        dates,
        data,
        colors=None,
        orientation=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def box(
        self,
        *args,
        quintuples=None,
        colors=None,
        fill=None,
        width=None,
        orientation=None,
        minimum=None,
        reset_ticks=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...

    ############################################################################
    # Plotting Tools
    def error(
        self,
        *args,
        xerr=None,
        yerr=None,
        color=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def event_plot(
        self, data, marker=None, color=None, orientation=None, side=None
    ) -> None: ...
    def eventplot(
        self, data, marker=None, color=None, orientation=None, side=None
    ) -> None: ...
    def vertical_line(self, coordinate, color=None, xside=None) -> None: ...
    def vline(self, coordinate, color=None, xside=None) -> None: ...
    def horizontal_line(self, coordinate, color=None, yside=None) -> None: ...
    def hline(self, coordinate, color=None, yside=None) -> None: ...
    def text(
        self,
        label,
        x,
        y,
        color=None,
        background=None,
        style=None,
        orientation=None,
        alignment=None,
        xside=None,
        yside=None,
    ) -> None: ...
    def rectangle(
        self,
        x=None,
        y=None,
        marker=None,
        color=None,
        lines=None,
        fill=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def polygon(
        self,
        x=None,
        y=None,
        radius=None,
        sides=None,
        marker=None,
        color=None,
        lines=None,
        fill=None,
        xside=None,
        yside=None,
        label=None,
    ) -> None: ...
    def confusion_matrix(
        self, actual, predicted, color=None, style=None, labels=None
    ) -> None: ...
    def cmatrix(
        self, actual, predicted, color=None, style=None, labels=None
    ) -> None: ...
    def indicator(self, value, label=None, color=None, style=None) -> None: ...

    ############################################################################
    # 2D Plots
    def matrix_plot(self, matrix, marker=None, style=None, fast=False) -> None: ...
    def image_plot(
        self, path, marker=None, style=None, fast=False, grayscale=False
    ) -> None: ...

    ############################################################################
    # Date Functions
    def date_form(self, input_form=None, output_form=None) -> None: ...
    def set_time0(self, string, input_form=None) -> None: ...
    def today_datetime(self) -> datetime: ...
    def today_string(self, output_form=None) -> str: ...
    def datetime_to_string(self, datetime, output_form=None) -> str: ...
    def datetimes_to_string(self, datetimes, output_form=None) -> list[str]: ...
    def string_to_datetime(self, string, input_form=None) -> datetime: ...
    def string_to_time(self, string, input_form=None) -> datetime: ...  # TODO
    def strings_to_time(self, string, input_form=None) -> datetime: ...  # TODO

    ############################################################################
    # Build Functions
    def build(self) -> str: ...

    ############################################################################
    # Externally Called Utility
    def plot_size(
        self, width: int | None = None, height: int | None = None
    ) -> None: ...
    def plotsize(self, width: int | None = None, height: int | None = None) -> None: ...
