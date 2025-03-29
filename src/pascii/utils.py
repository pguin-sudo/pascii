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


def flatten_color(color: float | tuple[int, ...] | None) -> tuple[int, int, int]:
    # print(color)
    if type(color) is tuple:
        return (color[0], color[1], color[2])
    if type(color) is float or type(color) is int:
        return (int(color), int(color), int(color))
    return (255, 255, 255)
