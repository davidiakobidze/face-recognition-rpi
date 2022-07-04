from GUI.Label import Lab


class GUI:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none", bg="white")

        self.place_labels_list = list()

    def create_text(self, text: str, x: int, y: int, size: int):
        label = Lab(self, x, y, None, text, size)
        label.show()

    def pl(self, label, x: int, y: int, save: bool = True) -> None:
        label.place(x=x, y=y)
        if save:
            self.place_labels_list.append(label)

    def remove_all(self):
        for i in self.place_labels_list:
            i.place_forget()
        self.place_labels_list = list()
