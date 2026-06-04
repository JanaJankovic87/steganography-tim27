import random
import string
import sys

sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw

from stego_core import resolve_input_image, resolve_output_image

IMAGES = ["snoopy1.jpg", "snoopy2.jpg", "snoopy3.jpg"]
DEMO_IMAGE = "snoopy1.jpg"
TERMINATOR = "@@snoopy@@"
TERMINATOR_BITS = len(TERMINATOR) * 8


def max_chars(image_path, bits_per_channel=1):
    img = Image.open(resolve_input_image(image_path)).convert('RGB')
    w, h = img.size
    total_bits = w * h * 3 * bits_per_channel
    usable_bits = total_bits - TERMINATOR_BITS
    return max(0, usable_bits // 8)


def embed_nbits(image_path, message, bits_per_channel, output_filename):
    img = Image.open(resolve_input_image(image_path)).convert('RGB')
    pixels = list(img.getdata())

    full = message + TERMINATOR
    bits = "".join(format(ord(c), '08b') for c in full)
    total_bits = len(bits)
    max_available = len(pixels) * 3 * bits_per_channel

    if total_bits > max_available:
        raise ValueError(
            f"Poruka zahteva {total_bits} bita; "
            f"slika ima {max_available} bita za {bits_per_channel} bit/kanal."
        )

    mask = 0xFF ^ ((1 << bits_per_channel) - 1)
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        new_ch = []
        for ch in pixel[:3]:
            if bit_index < total_bits:
                end = min(bit_index + bits_per_channel, total_bits)
                chunk = bits[bit_index:end].ljust(bits_per_channel, '0')
                ch = (ch & mask) | int(chunk, 2)
                bit_index += bits_per_channel
            new_ch.append(ch)
        new_pixels.append(tuple(new_ch))

    out = Image.new('RGB', img.size)
    out.putdata(new_pixels)
    out.save(resolve_output_image(output_filename))


def make_comparison_strip(items, output_filename):
    LABEL_H = 28
    imgs = [Image.open(resolve_input_image(fn)).convert('RGB') for fn, _ in items]

    target_h = imgs[0].height
    target_w = imgs[0].width
    resized = [im.resize((target_w, target_h), Image.LANCZOS) for im in imgs]

    total_w = target_w * len(resized)
    strip = Image.new('RGB', (total_w, target_h + LABEL_H), (20, 20, 20))
    draw = ImageDraw.Draw(strip)

    for i, (im, (_, label)) in enumerate(zip(resized, items)):
        strip.paste(im, (i * target_w, 0))
        draw.text((i * target_w + 6, target_h + 6), label, fill=(255, 255, 255))

    strip.save(resolve_output_image(output_filename))
    print(f"Poređenje sačuvano: output_images/{output_filename}")


def random_text(n):
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=n))


print("=" * 70)
print("KAPACITET SLIKA  —  maksimalan broj karaktera")
print("=" * 70)
print(f"{'Slika':<22} {'Rezolucija':>12}   {'1-bit':>8} {'2-bit':>8} {'3-bit':>8} {'4-bit':>8}")
print("-" * 70)

for name in IMAGES:
    img = Image.open(resolve_input_image(name)).convert('RGB')
    w, h = img.size
    caps = [max_chars(name, b) for b in (1, 2, 3, 4)]
    res = f"{w}×{h}"
    row = f"{name:<22} {res:>12}   "
    row += "   ".join(f"{c:>8,}" for c in caps)
    print(row)

print()
print("Formula:  max_znakova = (W * H * 3_kanala * N_bita_po_kanalu) / 8  -  terminator")
print()

print("=" * 70)
print("VIZUELNA DEGRADACIJA  —  svaki nivo popunjen do maksimalnog kapaciteta")
print("=" * 70)

items = []
for bits in (1, 2, 3, 4):
    cap = max_chars(DEMO_IMAGE, bits)
    msg = random_text(cap)
    fname = f"capacity_{bits}bit.png"
    embed_nbits(DEMO_IMAGE, msg, bits, fname)
    max_change = (1 << bits) - 1
    label = f"{bits}-bit  (max +-{max_change})"
    items.append((fname, label))
    print(f"  {bits} bit/kanal  ->  kapacitet {cap:>7,} znakova  |  max promena +-{max_change}")

print()
make_comparison_strip(items, "capacity_comparison.png")
print()

print("=" * 70)
print("PRAG VIDLJIVOSTI")
print("=" * 70)
thresholds = [
    ("1 bit/kanal", "max +-1",  "NEVIDLJIVO"),
    ("2 bit/kanal", "max +-3",  "NEVIDLJIVO"),
    ("3 bit/kanal", "max +-7",  "GRANICNO"),
    ("4 bit/kanal", "max +-15", "VIDLJIVO"),
]
for bits_label, change, visibility in thresholds:
    print(f"  {bits_label:<14}  promena {change:<10}  ->  {visibility}")

print()
print("Siguran maksimum = 1 LSB po kanalu.")
print("Svaki dodatni bit DUPLIRA kapacitet, ali povećava rizik od detekcije.")
print()

print("=" * 70)
print("KONKRETAN PRIMER  —  snoopy1.jpg")
print("=" * 70)
img = Image.open(resolve_input_image(DEMO_IMAGE)).convert('RGB')
w, h = img.size
safe_cap = max_chars(DEMO_IMAGE, 1)
print(f"  Dimenzije:         {w} x {h} = {w*h:,} piksela")
print(f"  Kanali po pikselu: 3  (R, G, B)")
print(f"  Ukupno bita (1-bit LSB): {w*h*3:,}")
print(f"  Maksimalno znakova (1-bit): {safe_cap:,}")