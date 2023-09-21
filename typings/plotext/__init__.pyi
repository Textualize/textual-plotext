"""Experimental type stub for Plotext.

To start with this simply contains what's needed to help fully type-check
the code of this library; but as time goes on this could turn into a set of
stubs for the whole of Plotext.
"""

from typing import Any, Union, Tuple

def sin(
    periods: int = 2,
    length: int = 200,
    amplitude: int = 1,
    phase: float = 0,
    decay: int = 0,
) -> list[float]: ...
def square(periods: int = 2, length: int = 200, amplitude: float = 1) -> list[int]: ...
def colorize(
    string: str,
    fullground: Union[str, int, Tuple[int, int, int], None] = None,
    style: str | None = None,
    background: Union[str, int, Tuple[int, int, int], None] = None,
    show: bool = False,
) -> str: ...
def uncolorize(string: str) -> str: ...
def transpose(data: list[list[Any]]) -> list[list[Any]]: ...

platform: str
