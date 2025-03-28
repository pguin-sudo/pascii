from abc import ABC, abstractmethod

from PIL import Image


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
        width, height = img.size

        text = text.replace("\n", "")

        ascii_image = ""
        for y in range(height):
            line = ""
            for x in range(width):
                color = img.getpixel((x, y))
                if type(color) is tuple:
                    line += ColorConverterBase.rgb_to_ansi(*color) + text[y * width + x]
                else:
                    line += (
                        ColorConverterBase.rgb_to_ansi(color, color, color)
                        + text[y * width + x]
                    )

            ascii_image += line + "\n"

        return ascii_image + "\033[0m"
