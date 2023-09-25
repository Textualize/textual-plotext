"""Experimental type stub for Plotext.

To start with this simply contains what's needed to help fully type-check
the code of this library; but as time goes on this could turn into a set of
stubs for the whole of Plotext.
"""

from __future__ import annotations

from typing import Any

def sin(
    periods: int,
    length: int,
    amplitude: int,
    phase: float,
    decay: int,
) -> list[float]: ...
def square(periods: int, length: int, amplitude: float) -> list[int]: ...
def colorize(
    string: str,
    fullground: str | int | tuple[int, int, int] | None,
    style: str | None,
    background: str | int | tuple[int, int, int] | None,
    show: bool,
) -> str: ...
def uncolorize(string: str) -> str: ...
def transpose(data: list[list[Any]]) -> list[list[Any]]: ...

platform: str = ...
