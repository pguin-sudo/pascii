from pascii import AsciiArt, chars, colors

# ❥

img_paths = (
    # "tests/images/penis.png",
    # "tests/images/python.png",
    # "tests/images/serega.jpg",
    "tests/images/nastya.jpg",
    "tests/images/jaba.jpg",
)

char_converters = (
    chars.Grayscale(),
    chars.SingleChar("❥"),
    # chars.Grayscale(True),
    chars.Braille(),
    # chars.Braille(True),
)

color_converters = (
    colors.AvgColor(),
    colors.BrailleColor(),
)

for img_path in img_paths:
    for char_converter in char_converters:
        for color_converter in color_converters:
            test_art = AsciiArt.from_path(
                img_path, char_converter, color_converter
            ).resize(new_height=58)
            test_art.to_terminal()

            print("<" + 85 * "-" + ">")
