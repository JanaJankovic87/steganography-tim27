from PIL import Image

from stego_core import resolve_input_image, resolve_output_image

ORIGINAL_IMAGE = "snoopy3.jpg"
STEGO_IMAGE = "example2_stego.png"
OUTPUT_ORIGINAL = "lsb_original.png"
OUTPUT_STEGO    = "lsb_stego.png"


def show_lsb_layer(image_path, output_path):
    img = Image.open(resolve_input_image(image_path)).convert('RGB')
    pixels = list(img.getdata())

    lsb_pixels = []
    for pixel in pixels:
        r, g, b = pixel
        lsb_pixels.append(((r & 1) * 255, (g & 1) * 255, (b & 1) * 255))

    lsb_img = Image.new('RGB', img.size)
    lsb_img.putdata(lsb_pixels)
    resolved_output_path = resolve_output_image(output_path)
    lsb_img.save(resolved_output_path)
    print(f"LSB layer saved: {resolved_output_path}")


show_lsb_layer(ORIGINAL_IMAGE, OUTPUT_ORIGINAL)
show_lsb_layer(STEGO_IMAGE, OUTPUT_STEGO)

print()
print("Compare lsb_original.png and lsb_stego.png.")
print("On the stego image you will see structure at the beginning")
print("where the message bits were written into the pixels.")