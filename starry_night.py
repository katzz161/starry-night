
import os
import sys
import time
import shutil
import math
from PIL import Image

# ==========================================
#          STARRY NIGHT ASCII ART
# ==========================================

IMAGE_FILE = "starry_night.jpg"

# Characters used to recreate the painting
ASCII_CHARS = " .'`^,:;Il!i><~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

RESET = "\033[0m"
CLEAR = "\033[2J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def get_terminal_size():
    size = shutil.get_terminal_size((100, 40))
    return size.columns, size.lines - 2


def pixel_to_ascii(pixel):
    r, g, b = pixel

    # Calculate brightness
    brightness = 0.299*r + 0.587*g + 0.114*b

    index = int(brightness / 255 * (len(ASCII_CHARS)-1))
    char = ASCII_CHARS[index]

    return char, r, g, b


def create_ascii(image, width, height, frame):
    image = image.resize((width, height))

    pixels = image.load()
    result = []

    for y in range(height):
        line = ""

        for x in range(width):
            char, r, g, b = pixel_to_ascii(pixels[x, y])

            # Gentle moving colour shimmer
            shimmer = math.sin(frame * 0.035 + x * 0.025 + y * 0.02)

            r = max(0, min(255, int(r + shimmer * 5)))
            g = max(0, min(255, int(g + shimmer * 7)))
            b = max(0, min(255, int(b + shimmer * 9)))

            line += (
                f"\033[38;2;{r};{g};{b}m{char}"
            )

        line += RESET
        result.append(line)

    return "\n".join(result)


def main():
    if not os.path.exists(IMAGE_FILE):
        print("Could not find starry_night.jpg!")
        print("Place the image in the same folder as this script.")
        return

    image = Image.open(IMAGE_FILE).convert("RGB")

    print(HIDE_CURSOR + CLEAR)

    frame = 0

    try:
        while True:
            width, height = get_terminal_size()

            # Keep the image proportions
            height = max(10, height)
            width = max(20, width)

            resized_height = int(height * 0.5)

            artwork = create_ascii(
                image,
                width,
                resized_height,
                frame
            )

            print("\033[H", end="")
            print(artwork, flush=True)

            frame += 1
            time.sleep(0.08)

    except KeyboardInterrupt:
        pass

    finally:
        print(RESET + SHOW_CURSOR)


if __name__ == "__main__":
    main()
