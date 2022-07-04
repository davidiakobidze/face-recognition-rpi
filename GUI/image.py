from PIL import Image, ImageTk


def get_image(image) -> ImageTk.PhotoImage:
    image = Image.open(image) if type(image) == str else image

    return ImageTk.PhotoImage(image)
