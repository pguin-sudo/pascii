from abc import ABC, abstractmethod
from statistics import median
from typing import Callable, Iterable

from PIL import Image

from pascii.utils import braille_map, flatten_color


class ColorConverterBase(ABC):
    @abstractmethod
    def convert(self, img: Image.Image, text: str, size: tuple[int, int]) -> str: ...

    @staticmethod
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"


class Monotone(ColorConverterBase):
    color: tuple[int, int, int]

    def __init__(self, color: tuple[int, int, int] = (255, 255, 255)):
        self.color = color

    def convert(self, img: Image.Image, text: str, size: tuple[int, int]) -> str:
        return ColorConverterBase.rgb_to_ansi(*self.color) + text + "\033[0m"


class AvgColor(ColorConverterBase):
    def convert(self, img: Image.Image, text: str, size: tuple[int, int]) -> str:
        img = img.resize(size)
        width, height = size

        text = text.replace("\n", "")

        ascii_image = ""
        for y in range(height):
            row = ""
            for x in range(width):
                color = flatten_color(img.getpixel((x, y)))
                row += ColorConverterBase.rgb_to_ansi(*color) + text[y * width + x]

            ascii_image += row + "\n"

        return ascii_image + "\033[0m"


class BrailleColor(ColorConverterBase):
    def __init__(
        self,
        reversed: bool = False,
        threshold_function: Callable[[Iterable[int]], float] = median,
    ):
        self.reversed = reversed
        self.threshold_function = threshold_function

    def convert(self, img: Image.Image, text: str, size: tuple[int, int]) -> str:
        result_width, result_height = size

        img = img.resize((result_width * 2, result_height * 4))
        img_luma = img.convert("L")
        pixels = list(img_luma.getdata())

        text = text.replace("\n", "")

        threshold = self.threshold_function(pixels)

        ascii_image = ""
        for i in range(result_height):
            row = ""
            for j in range(result_width):
                colors = []
                for x, y in braille_map(j * 2, i * 4):
                    luma_color = img_luma.getpixel((x, y))
                    if type(luma_color) is not float and type(luma_color) is not int:
                        continue
                    color = flatten_color(img.getpixel((x, y)))
                    if (threshold >= luma_color) == self.reversed:
                        colors.append(color)
                avg_color = (
                    tuple(sum(c[d] for c in colors) // len(colors) for d in range(3))
                    if len(colors)
                    else (0, 0, 0)
                )
                row += (
                    ColorConverterBase.rgb_to_ansi(*avg_color)
                    + text[i * result_width + j]
                )
            ascii_image += row + "" + "\n"

        return ascii_image + "\033[0m"
