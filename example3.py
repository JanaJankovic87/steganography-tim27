from stego_core import embed, extract, xor_encrypt

INPUT_IMAGE  = "snoopy3.jpg"
OUTPUT_IMAGE = "example3_stego.png"
MESSAGE      = "Happiness is a warm puppy."
KEY          = "key"

encrypted = xor_encrypt(MESSAGE, KEY)
print(f"Original message:   {MESSAGE}")
print(f"XOR encrypted:      {repr(encrypted)}")

embed(INPUT_IMAGE, encrypted, OUTPUT_IMAGE)

extracted_encrypted = extract(OUTPUT_IMAGE)
decrypted = xor_encrypt(extracted_encrypted, KEY)

print(f"Extracted (encrypted): {repr(extracted_encrypted)}")
print(f"Decrypted message:     {decrypted}")
