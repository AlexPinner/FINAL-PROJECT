from tkinter import *

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title('Pane Testing')
root.geometry('{}x{}'.format(800, 600))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

pane_one = PanedWindow(root, orient=VERTICAL, bd=0, bg='yellow', sashwidth=4)
pane_one.grid(sticky='nsew')

pane_two = PanedWindow(pane_one, orient=HORIZONTAL, bd=0, bg='black', sashwidth=4)
pane_two.grid(sticky='new')
pane_one.add(pane_two, stretch='always')

pane_one_red = Frame(pane_one)
pane_one_red.config(bg='red', width=200, height=100)
pane_one_red.grid(sticky='nsew')

test_frame_one = Frame(pane_one_red)
test_frame_two = Frame(pane_one_red)
test_frame_one.config(bg='pink', height=150)
test_frame_two.config(bg='purple', height=150)
test_button_one = Button(test_frame_one)
test_button_two = Button(test_frame_two)
test_button_one.config(text='Raise Two', command=lambda: raise_frame(test_frame_two))
test_button_two.config(text='Raise One', command=lambda: raise_frame(test_frame_one))
test_frame_one.grid(row=0, column=1, sticky='nsew')
test_frame_two.grid(row=0, column=1, sticky='nsew')
test_button_one.grid(row=0, column=0, sticky='nsew')
test_button_two.grid(row=0, column=0, sticky='nsew')
raise_frame(test_frame_one)
red_height = Frame(pane_one_red)
red_height.config(bg='green', width=10, height=150)
pane_one_red.grid_columnconfigure(0, weight=1)
pane_one_red.grid_columnconfigure(3, weight=1)
red_height.grid(row=0, column=2, sticky='nsew')
pane_one.add(pane_one_red, stretch='never')
"""
pane_one_pink = Frame(pane_one)
pane_one_pink.config(bg='pink', width=200, height=200)
pane_one_pink.grid(sticky='nsew')
pane_one.add(pane_one_pink, stretch='always')
"""

pane_two_blue = Frame(pane_two)
pane_two_blue.config(bg='blue', width=100, height=200)
pane_two_blue.grid(sticky='nsew')
blue_width = Frame(pane_two_blue)
blue_width.config(bg='cyan', width=150, height=10)
pane_two_blue.grid_rowconfigure(0, weight=1)
pane_two_blue.grid_rowconfigure(2, weight=1)
blue_width.grid(row=1, column=0, sticky='nsew')
pane_two.add(pane_two_blue, stretch='never')

pane_two_orange = Frame(pane_two)
pane_two_orange.config(bg='orange', width=200, height=200)
pane_two_orange.grid(sticky='nsew')
pane_two.add(pane_two_orange, stretch='always')

root.mainloop()