from pascii import AsciiArt, chars, colors

# ❥

test_art = AsciiArt.from_path(
    "tests/images/jaba.jpg", chars.Grayscale(True), colors.AvgColor()
).resize(new_height=64)
test_art.to_terminal()
