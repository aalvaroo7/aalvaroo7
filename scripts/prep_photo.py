from PIL import Image, ImageOps, ImageEnhance
from rembg import remove
import io
import os

INPUT_IMAGE = "foto.png"
OUTPUT_IMAGE = "foto-preparada.png"

def remove_background(img: Image.Image) -> Image.Image:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    result = remove(buf.getvalue())
    out = Image.open(io.BytesIO(result)).convert("RGBA")
    return out

def crop_to_subject(img: Image.Image, padding=40) -> Image.Image:
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return img
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img.width, right + padding)
    bottom = min(img.height, bottom + padding)
    return img.crop((left, top, right, bottom))

def composite_on_white(img: Image.Image) -> Image.Image:
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    merged = Image.alpha_composite(bg, img)
    return merged.convert("RGB")

def main():
    if not os.path.exists(INPUT_IMAGE):
        raise FileNotFoundError(f"No se encuentra {INPUT_IMAGE}")

    img = Image.open(INPUT_IMAGE).convert("RGBA")

    # Quitar fondo
    img = remove_background(img)

    # Recortar al sujeto
    img = crop_to_subject(img, padding=30)

    # Poner fondo blanco para que el ASCII quede limpio
    img = composite_on_white(img)

    # Escala de grises
    img = ImageOps.grayscale(img)

    # Mejorar contraste
    img = ImageOps.autocontrast(img, cutoff=1)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.35)

    # Suavizar un poco brillo para que la cara se marque mejor
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(1.12)

    # Guardar
    img.save(OUTPUT_IMAGE)
    print(f"Imagen preparada guardada como: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()