import threading
import tkinter as tk

from GUI.GUI import GUI


def run():
    pass


if __name__ == '__main__':
    # Start GUI
    gui_object = None
    root = tk.Tk()
    gui_object = GUI(root)
    threading.Thread(target=run).start()

    root.mainloop()
