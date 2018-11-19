from tkinter import *
from tkinter import ttk

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()

class Yellow_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="yellow"

class Orange_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="orange"

big_pane = PanedWindow(orient=HORIZONTAL)
big_pane.pack(fill=BOTH, expand=1)

"""
#This section works for listboxes in paned windows
listbox = Listbox(big_pane)
listbox.pack()

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

big_pane.add(listbox)
"""

#this section is like the previous one but with a scrollbar
left = Frame(big_pane)
left.pack()

listbox = Listbox(left)
listbox.pack(side=LEFT, fill=BOTH)

scrollbar = Scrollbar(left, orient=VERTICAL)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)

listbox.config(yscrollcommand=scrollbar.set)

listbox.insert(END, "Testing to see if expand")

for i in range(1000):
    listbox.insert(END, str(i))

big_pane.add(left)


right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
big_pane.add(right)
top = Orange_Frame(big_pane)
right.add(top)
bottom = Yellow_Frame(big_pane)
right.add(bottom)

mainloop()