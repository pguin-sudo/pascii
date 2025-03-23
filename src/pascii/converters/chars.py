from PIL import Image

from abc import ABC, abstractmethod

from pascii.consts import GSCALE


class CharConverterBase(ABC):
    @abstractmethod
    def convert(self, img: Image.Image) -> str: ...


class SingleChar(CharConverterBase):
    char: str = ""

    def __init__(self, char: str = "@"):
        self.char = char

    def convert(self, img: Image.Image) -> str:
        img = img.convert("RGB")

        width, height = img.size

        return "\n".join([self.char * width] * height)


class Grayscale(CharConverterBase):
    def convert(self, img: Image.Image) -> str:
        img = img.convert("L")

        width, _ = img.size
        pixels = list(img.getdata())

        denominator = 300 // len(GSCALE)

        ascii_image = [
            "".join(GSCALE[pixel // denominator] for pixel in pixels[i : i + width])
            for i in range(0, len(pixels), width)
        ]

        return "\n".join(ascii_image)
