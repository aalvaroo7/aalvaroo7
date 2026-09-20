from PIL import Image
import os
import html

INPUT_IMAGE = "foto-preparada.png"
OUTPUT_SVG = "ascii.svg"

ASCII_CHARS = " .`:-=+*cs#%@"

# Ajusta el ancho del retrato ASCII
ASCII_WIDTH = 62

# Ajuste vertical porque los caracteres son más altos que anchos
HEIGHT_CORRECTION = 0.55

FONT_SIZE = 10
LINE_HEIGHT = 12
PADDING = 20

def pixel_to_char(pixel):
    index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def image_to_ascii_lines(image_path):
    img = Image.open(image_path).convert("L")

    width, height = img.size
    aspect_ratio = height / width
    new_height = int(ASCII_WIDTH * aspect_ratio * HEIGHT_CORRECTION)

    img = img.resize((ASCII_WIDTH, new_height))

    pixels = img.load()
    lines = []

    for y in range(new_height):
        line = ""
        for x in range(ASCII_WIDTH):
            pixel = pixels[x, y]
            line += pixel_to_char(pixel)
        lines.append(line)

    return lines

def make_svg(lines, output_path):
    svg_width = ASCII_WIDTH * 7 + PADDING * 2
    svg_height = len(lines) * LINE_HEIGHT + PADDING * 2

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">''')
    svg_parts.append(f'''<rect width="100%" height="100%" fill="#0d1117"/>''')

    # Marco estilo terminal
    svg_parts.append(f'''<rect x="5" y="5" width="{svg_width-10}" height="{svg_height-10}" rx="8" ry="8" fill="none" stroke="#30363d" stroke-width="1"/>''')

    for i, line in enumerate(lines):
        y = PADDING + (i + 1) * LINE_HEIGHT
        safe_line = html.escape(line)

        delay = round(i * 0.06, 2)
        svg_parts.append(f'''
        <g opacity="0">
            <text x="{PADDING}" y="{y}" font-family="Consolas, 'Courier New', monospace"
                  font-size="{FONT_SIZE}" fill="#c9d1d9" xml:space="preserve">{safe_line}</text>
            <animate attributeName="opacity"
                     values="0;0;1;1"
                     keyTimes="0;0.15;0.16;1"
                     dur="8s"
                     begin="{delay}s"
                     repeatCount="indefinite"/>
        </g>
        ''')

    svg_parts.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

def main():
    if not os.path.exists(INPUT_IMAGE):
        raise FileNotFoundError(f"No se encuentra {INPUT_IMAGE}")

    lines = image_to_ascii_lines(INPUT_IMAGE)
    make_svg(lines, OUTPUT_SVG)
    print(f"SVG ASCII generado: {OUTPUT_SVG}")

if __name__ == "__main__":
    main()