from PIL import Image

def text_to_bits(text):
    bits = ""
    for character in text:
        bits += format(ord(character), '08b')
    return bits

def embed(input_image, message, output_image):
    image = Image.open(input_image)
    pixels = list(image.getdata())
    
    message = message + "@@snoopy@@"  # jedinstveni kod za prepoznavanje kraja poruke
    
    message_bits = text_to_bits(message)
    total_bits = len(message_bits)
    
    max_bits = len(pixels) * 3
    if total_bits > max_bits:
        print(f"Error: Message is too long!")
        print(f"Message requires {total_bits} bits")
        print(f"Image only has {max_bits} bits")
        return
    
    new_pixels = []
    bit_index = 0
    
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        if bit_index < total_bits:
            r = (r & 0b11111110) | int(message_bits[bit_index])
            bit_index += 1
        
        if bit_index < total_bits:
            g = (g & 0b11111110) | int(message_bits[bit_index])
            bit_index += 1
        
        if bit_index < total_bits:
            b = (b & 0b11111110) | int(message_bits[bit_index])
            bit_index += 1
        
        new_pixels.append((r, g, b))
    
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_image)
    
    print(f"Message successfully hidden in the image.")
    print(f"Output image is: {output_image}")



if __name__ == "__main__":
    embed(
        input_image="input.jpg",
        message="Good grief!",
        output_image="stego.png"
    )