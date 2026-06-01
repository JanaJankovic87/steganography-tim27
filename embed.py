from stego_core import embed

if __name__ == "__main__":
    embed(
        input_image="input.jpg",
        message="Good grief!",
        output_image="stego.png"
    )