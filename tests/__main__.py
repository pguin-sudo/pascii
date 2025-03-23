from pascii import AsciiArt, chars, colors

# ❥

test_art = AsciiArt.from_path(
    "tests/images/penis.png", chars.Grayscale(), colors.AvgColor()
).resize(new_height=64)
test_art.to_terminal()
