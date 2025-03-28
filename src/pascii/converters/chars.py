from abc import ABC, abstractmethod
from statistics import median
from typing import Callable, Iterable

from PIL import Image

from pascii.consts import GSCALE


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
        threshold_function: Callable[[Iterable[int]], float] = median,
    ):
        self.reversed = reversed
        self.threshold_function = threshold_function

    def convert(self, img: Image.Image, size: tuple[int, int]) -> str:
        img = img.resize((size[0] * 2, size[1] * 4)).convert("L")

        width, height = img.size
        result_width, result_height = width // 2, height // 4
        pixels = list(img.getdata())

        threshold = self.threshold_function(pixels)

        pixels = [
            [(threshold >= pixel) == self.reversed for pixel in pixels[i : i + width]]
            for i in range(0, len(pixels), width)
        ]

        ascii_image = ""
        for i in range(0, result_height):
            row = ""
            for j in range(0, result_width):
                i2, j2 = i * 4, j * 2
                p = (
                    ((pixels[i2][j2] * 2**0) + (pixels[i2][j2 + 1] * 2**3))
                    + ((pixels[i2 + 1][j2] * 2**1) + (pixels[i2 + 1][j2 + 1] * 2**4))
                    + ((pixels[i2 + 2][j2] * 2**2) + (pixels[i2 + 2][j2 + 1] * 2**5))
                    + ((pixels[i2 + 3][j2] * 2**6) + (pixels[i2 + 3][j2 + 1] * 2**7))
                )
                row += chr(int("2800", 16) + int(p))
            ascii_image += row + "\n"

        # Shitty shit
        ascii_image += "0" * 1000000

        return ascii_image
