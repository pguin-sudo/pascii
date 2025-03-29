from typing import Type, TypeVar

from PIL import Image

from pascii.converters import chars, colors

T = TypeVar("T", bound="AsciiArt")


class AsciiArt:
    img: Image.Image
    size: tuple[int, int]
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
        self.width, self.height = img.size

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

    def resize(
        self, new_width: int = 0, new_height: int = 0, ratio_multiplier: float = 0.55
    ):
        width, height = self.img.size
        aspect_ratio = height / width
        if not new_height and not new_width:
            return self
        elif new_height and not new_width:
            new_width = int(new_height / aspect_ratio / ratio_multiplier)
        elif new_width and not new_height:
            new_height = int(new_width * aspect_ratio * ratio_multiplier)

        self.size = (new_width, new_height)
        return self

    def to_terminal(self):
        text = self.char_converter.convert(self.img, self.size)
        if (len(text.split("\n")[0]), len(text.split("\n"))) != self.size:
            print(
                self.char_converter,
                (len(text.split("\n")[0]), len(text.split("\n"))),
                self.size,
            )
            return
        text = self.color_converter.convert(self.img, text, self.size)
        print(text)
