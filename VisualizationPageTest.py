from tkinter import *
from tkinter import ttk

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()

def Create_EDA_Notebook(window):
    "Creates notebook geared towards EDA"

    note = ttk.Notebook(window)
    Create_Listbox
    Create_Notebook_Tab(note, "Data Cleaning", listbox)
    Create_Notebook_Tab(note, "EDA", )


def Create_Notebook_Tab(notebook, tab_name, left_item, right_top_item, right_bottom_item):
    "Create a notebook page and place each item in the corresponding paned window location."

    tab = PanedWindow(orient=HORIZONTAL)
    tab.pack(fill=BOTH, expand=1)
    tab.add(left_item)
    right = PanedWindow(orient=VERTICAL)
    right.pack(fill=BOTH, expand=1)
    tab.add(right)
    right.add(right_top_item)
    right.add(right_bottom_item)

    notebook.add(tab, text=tab_name)

def Create_Listbox(window, list_items):
    "Create a listbox in window and populate it with list_items"

    len_max = 0
    for m in list_items:
        if len(m) > len_max:
            len_max = len(m)
    
    listbox = Listbox(window, width=len_max)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    listbox.config(yscrollcommand=scrollbar.set)

    for m in list_items:
        listbox.insert(END, str(m))
