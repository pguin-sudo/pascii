from PIL import Image

from typing import Type, TypeVar

from pascii.converters import colors, chars

T = TypeVar("T", bound="AsciiArt")


class AsciiArt:
    img: Image.Image
    char_converter: chars.CharConverterBase
    color_converter: colors.ColorConverterBase

    def __init__(
        self,
        img: Image.Image,
        char_converter: chars.CharConverterBase,
        color_converter: colors.ColorConverterBase,
    ):
        self.img = img
        self.char_converter = char_converter
        self.color_converter = color_converter

    @classmethod
    def from_path(
        cls: Type[T],
        path: str = "image.jpg",
        char_converter: chars.CharConverterBase = chars.SingleChar(),
        color_converter: colors.ColorConverterBase = colors.AvgColor(),
    ) -> T:
        try:
            img = Image.open(path)
        except:
            print(path, "Unable to find image ")
            raise

        return cls(img, char_converter, color_converter)

    def resize(self, new_width: int | None = None, new_height: int | None = None):
        width, height = self.img.size
        aspect_ratio = height / width
        if new_height is None and new_width is None:
            return self
        elif new_height is not None and new_width is None:
            new_width = int(new_height / aspect_ratio / 0.55)
        elif new_width is not None and new_height is None:
            new_height = int(new_width * aspect_ratio * 0.55)

        self.img = self.img.resize((new_width, new_height))
        return self

    def to_terminal(self):
        text = self.char_converter.convert(self.img)
        text = self.color_converter.convert(self.img, text)
        print(text)
