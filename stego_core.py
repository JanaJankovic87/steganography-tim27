from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
ORIGINAL_IMAGES_DIR = BASE_DIR / "original_images"
OUTPUT_IMAGES_DIR = BASE_DIR / "output_images"


def resolve_image_path(image_name):
    candidate = Path(image_name)
    if candidate.is_absolute():
        return candidate

    original_candidate = ORIGINAL_IMAGES_DIR / candidate
    if original_candidate.exists():
        return original_candidate

    output_candidate = OUTPUT_IMAGES_DIR / candidate
    if output_candidate.exists():
        return output_candidate

    root_candidate = BASE_DIR / candidate
    if root_candidate.exists():
        return root_candidate

    return original_candidate


def resolve_input_image(image_name):
    return resolve_image_path(image_name)


def resolve_output_image(image_name):
    candidate = Path(image_name)
    if candidate.is_absolute():
        candidate.parent.mkdir(parents=True, exist_ok=True)
        return candidate

    output_candidate = OUTPUT_IMAGES_DIR / candidate
    output_candidate.parent.mkdir(parents=True, exist_ok=True)
    return output_candidate


def embed(input_image, message, output_image):
    input_path = resolve_image_path(input_image)
    output_path = resolve_output_image(output_image)

    image = Image.open(input_path)
    pixels = list(image.getdata())

    message = message + "@@snoopy@@"

    bits = ""
    for character in message:
        bits += format(ord(character), '08b')

    total_bits = len(bits)
    max_bits = len(pixels) * 3

    if total_bits > max_bits:
        print(f"Error: message is too long!")
        print(f"Message requires {total_bits} bits")
        print(f"Image only has {max_bits} bits available")
        return

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]

        if bit_index < total_bits:
            r = (r & 0b11111110) | int(bits[bit_index])
            bit_index += 1
        if bit_index < total_bits:
            g = (g & 0b11111110) | int(bits[bit_index])
            bit_index += 1
        if bit_index < total_bits:
            b = (b & 0b11111110) | int(bits[bit_index])
            bit_index += 1

        new_pixels.append((r, g, b))

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_path)
    print(f"Message successfully embedded in: {output_path}")


def extract(stego_path):
    image = Image.open(resolve_image_path(stego_path))
    pixels = list(image.getdata())

    bits = []
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i+8]
        char = chr(int(''.join(map(str, byte)), 2))
        chars.append(char)

    full_text = ''.join(chars)

    terminator = "@@snoopy@@"
    idx = full_text.find(terminator)
    if idx != -1:
        return full_text[:idx]
    return full_text


def xor_encrypt(text, key):
    result = ""
    for i, char in enumerate(text):
        result += chr(ord(char) ^ ord(key[i % len(key)]))
    return result