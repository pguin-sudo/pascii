from typing import Any


def braille_map(
    x: int, y: int
) -> tuple[
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
]:
    return (
        (x, y),
        (x, y + 1),
        (x, y + 2),
        (x + 1, y),
        (x + 1, y + 1),
        (x + 1, y + 2),
        (x, y + 3),
        (x + 1, y + 3),
    )


def flatten_color(color: float | tuple[int, ...]) -> float: ...
