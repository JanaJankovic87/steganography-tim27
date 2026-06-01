from stego_core import embed, extract

INPUT_IMAGE  = "snoopy2.jpg"
OUTPUT_IMAGE = "example2_stego.png"
MESSAGE      = (
    "Woodstock may be small, but he is the best friend a beagle could ever have. He cannot fly in a straight line, he cannot understand most things, but he always shows up when it matters most."
)

embed(INPUT_IMAGE, MESSAGE, OUTPUT_IMAGE)

extracted = extract(OUTPUT_IMAGE)
print(f"Original message ({len(MESSAGE)} chars):")
print(MESSAGE)
print()
print(f"Extracted message ({len(extracted)} chars):")
print(extracted)
