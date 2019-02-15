import tkinter as tk
import random

root = tk.Tk()


class Red_Frame(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "red"


class Blue_Frame(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "blue"


class Yellow_Frame(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "yellow"


def testFunc(frames):
    for fr in frames:
        fr.grid(row=0, column=0)
    frames[red].tkraise()


frames_list = {}

red = Red_Frame(root)
blue = Blue_Frame(root)
yellow = Yellow_Frame(root)

for f in (red, blue, yellow):
    frames_list[f] = f

testFunc(frames_list)

root.mainloop()
