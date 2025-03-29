from abc import ABC, abstractmethod
from statistics import median
from typing import Callable, Iterable

from PIL import Image

from pascii.consts import GSCALE
from pascii.utils import braille_map


class CharConverterBase(ABC):
    @abstractmethod
    def convert(self, img: Image.Image, size: tuple[int, int]) -> str: ...


class SingleChar(CharConverterBase):
    char: str = ""

    def __init__(self, char: str = "@"):
        self.char = char

    def convert(self, img: Image.Image, size: tuple[int, int]) -> str:
        img = img.resize(size).convert("RGB")

        width, height = img.size

        return "\n".join([self.char * width] * height)


class Grayscale(CharConverterBase):
    reversed = False

    def __init__(self, reversed=False):
        self.reversed = reversed

    def convert(self, img: Image.Image, size: tuple[int, int]) -> str:
        img = img.resize(size).convert("L")

        width, _ = img.size
        pixels = list(img.getdata())

        denominator = 300 // len(GSCALE)

        if not self.reversed:
            ascii_image = [
                "".join(
                    GSCALE[-(pixel // denominator) - 1]
                    for pixel in pixels[i : i + width]
                )
                for i in range(0, len(pixels), width)
            ]
        else:
            ascii_image = [
                "".join(GSCALE[pixel // denominator] for pixel in pixels[i : i + width])
                for i in range(0, len(pixels), width)
            ]

        return "\n".join(ascii_image)


class Braille(CharConverterBase):
    def __init__(
        self,
        reversed: bool = False,
        threshold_function: Callable[[list[int]], float] = median,
    ):
        self.reversed = reversed
        self.threshold_function = threshold_function

    def convert(self, img: Image.Image, size: tuple[int, int]) -> str:
        result_width, result_height = size

        img = img.resize((result_width * 2, result_height * 4)).convert("L")
        width, height = img.size
        pixels = list(img.getdata())

        threshold = self.threshold_function(pixels)

        pixels = [
            [(threshold >= pixel) == self.reversed for pixel in pixels[i : i + width]]
            for i in range(0, len(pixels), width)
        ]

        ascii_image = ""
        for i in range(result_height):
            row = ""
            for j in range(result_width):
                p = sum(
                    pixels[y][x] * 2**a
                    for a, (x, y) in enumerate(braille_map(j * 2, i * 4))
                )
                row += chr(int("2800", 16) + int(p))
            ascii_image += row
            if i != result_height - 1:
                ascii_image += "\n"
        # Shitty shit

        return ascii_image
