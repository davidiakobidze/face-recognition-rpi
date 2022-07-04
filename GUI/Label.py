import tkinter as tk


class Lab:
    def __init__(self,
                 gui,
                 x: int = 0,
                 y: int = 0,
                 image=None,
                 text: str = "",
                 font_size: int = 20
                 ):
        self.gui = gui
        self.root = gui.root
        self.x = x
        self.y = y
        self.font_size = font_size
        self.label = tk.Label(
            self.root,
            bg='white',
            text=text,
            image=image,
            font=("Arial", self.font_size)
        )

    def show(self, save=True):
        self.gui.pl(self.label, self.x, self.y, save)

    def configure(self, image=None, text=None):
        self.label.configure(image=image, text=text)

    def remove(self):
        self.label.place_forget()
