from PIL import Image

from abc import ABC, abstractmethod


class ColorConverterBase(ABC):
    @staticmethod
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    @abstractmethod
    def convert(self, img: Image.Image, text: str) -> str: ...


class Monotone(ColorConverterBase):
    color: tuple[int, int, int]

    def __init__(self, color: tuple[int, int, int] = (255, 255, 255)):
        self.color = color

    def convert(self, img: Image.Image, text: str) -> str:
        return ColorConverterBase.rgb_to_ansi(*self.color) + text + "\033[0m"


class AvgColor(ColorConverterBase):
    def convert(self, img: Image.Image, text: str) -> str:
        width, height = img.size

        text = text.replace("\n", "")

        ascii_image = []
        for y in range(height):
            line = "".join(
                (
                    ColorConverterBase.rgb_to_ansi(*img.getpixel((x, y)))
                    + text[y * width + x]
                )
                for x in range(width)
            )
            ascii_image.append(line)

        return "\n".join(ascii_image) + "\033[0m"
