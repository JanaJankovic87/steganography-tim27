from stego_core import embed, extract

INPUT_IMAGE  = "snoopy1.jpg"
OUTPUT_IMAGE = "example1_stego.png"
MESSAGE      = "Tweet tweet!"

embed(INPUT_IMAGE, MESSAGE, OUTPUT_IMAGE)

extracted = extract(OUTPUT_IMAGE)
print(f"Original message: {MESSAGE}")
print(f"Extracted message: {extracted}")
