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
    Create_Notebook_Tab(note, "Data Cleaning", )
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