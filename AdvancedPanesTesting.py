import tkinter as tk
from tkinter import Frame, Label, Button, PanedWindow, Listbox, Toplevel, Scrollbar
from tkinter import HORIZONTAL, VERTICAL, LEFT, RIGHT, TOP, BOTTOM, Y, X, BOTH, END

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


def raise_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title('Advanced Pane Testing')
root.geometry('{}x{}'.format(800, 600))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

"""
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
test_button_one.grid(row=0, column=0, sticky='nsew')
test_button_two.grid(row=0, column=0, sticky='nsew')
test_frame_one.grid(row=0, column=1, sticky='nsew')
test_frame_two.grid(row=0, column=1, sticky='nsew')
raise_frame(test_frame_one)
red_height = Frame(pane_one_red)
red_height.config(bg='green', width=10, height=150)
pane_one_red.grid_columnconfigure(0, weight=1)
pane_one_red.grid_columnconfigure(3, weight=1)
red_height.grid(row=0, column=2, sticky='nsew')
pane_one.add(pane_one_red, stretch='never')

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
"""

class PP_Frame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent, **options)

        self.config(bg='green')
        pp_label = Label(self)
        pp_label.config(text='Pairplot Controls')
        pp_label.grid(row=0, column=0, sticky='ew')
        window_prop = Frame(self)
        window_prop.config(width=10, height=150, bg='lavender')
        window_prop.grid(row=0, column=1, sticky='nsew')

class CM_Frame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent, **options)

        self.config(bg='purple')
        cm_label = Label(self)
        cm_label.config(text='Correlation Matrix Controls')
        cm_label.grid(row=0, column=0, sticky='ew')
        window_prop = Frame(self)
        window_prop.config(width=10, height=150, bg='pink')
        window_prop.grid(row=0, column=1, sticky='nsew')


class BP_Frame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent, **options)

        self.config(bg='blue')
        bp_label = Label(self)
        bp_label.config(text='Barplot Controls')
        bp_label.grid(row=0, column=0, sticky='ew')
        window_prop = Frame(self)
        window_prop.config(width=10, height=150, bg='cyan')
        window_prop.grid(row=0, column=1, sticky='nsew')


EDA_Bottom_Pane = PanedWindow(root, orient=VERTICAL, bd=0, bg='yellow', sashwidth=4)
EDA_Bottom_Pane.grid(sticky='nsew')

EDA_Top_Pane = PanedWindow(EDA_Bottom_Pane, orient=HORIZONTAL, bd=0, bg='black', sashwidth=4)
EDA_Top_Pane.grid(sticky='nsew')
EDA_Bottom_Pane.add(EDA_Top_Pane, stretch='always')

EDA_Controls_Frame = Frame(EDA_Bottom_Pane)
EDA_Controls_Frame.config(bg='red', width=200, height=100)
EDA_Controls_Frame.grid(sticky='nsew')
EDA_Controls_Frame.grid_columnconfigure(0, weight=1)
EDA_Controls_Frame.grid_columnconfigure(2, weight=1)
EDA_Bottom_Pane.add(EDA_Controls_Frame, stretch='never')

pp_frame = PP_Frame(EDA_Controls_Frame)
cm_frame = CM_Frame(EDA_Controls_Frame)
bp_frame = BP_Frame(EDA_Controls_Frame)

for frame in (pp_frame, cm_frame, bp_frame):
    frame.grid(row=0, column=1, sticky='nsew')
raise_frame(pp_frame)

EDA_Listbox_Frame = Frame(EDA_Top_Pane)
EDA_Listbox_Frame.config(bg='blue', width=100, height=200)
EDA_Listbox_Frame.grid(sticky='nsew')
EDA_Top_Pane.add(EDA_Listbox_Frame, stretch='never')

pp_listbox = Frame(EDA_Listbox_Frame)
cm_listbox = Frame(EDA_Listbox_Frame)
bp_listbox = Frame(EDA_Listbox_Frame)

for frame in (pp_listbox, cm_listbox, bp_listbox):
    frame.grid()

Button(pp_listbox, text='Pairplot', command=lambda: raise_frame(pp_frame)).grid()
Button(cm_listbox, text='Correlation Matrix', command=lambda: raise_frame(cm_frame)).grid()
Button(bp_listbox, text='Bar Plot', command=lambda: raise_frame(bp_frame)).grid()

EDA_Canvas_Frame = Frame(EDA_Top_Pane)
EDA_Canvas_Frame.config(bg='orange')
EDA_Canvas_Frame.grid(sticky='nsew')
EDA_Top_Pane.add(EDA_Canvas_Frame, stretch='always')

root.mainloop()
