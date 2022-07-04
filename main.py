import threading
import tkinter as tk
import time

from GUI.GUI import GUI


def run():
    print("run")
    gui_object.start()
    while 1:
        time.sleep(1)


if __name__ == '__main__':
    # Start GUI
    gui_object = None
    root = tk.Tk()
    gui_object = GUI(root)
    threading.Thread(target=run).start()

    root.mainloop()
