import matplotlib
matplotlib.use("TkAgg")
from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class Red_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="red"

class Blue_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="blue"

class Green_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="green"

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

class Purple_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="purple"

class Cyan_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="cyan"

class Black_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="black"

class Brown_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="brown"

class White_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="white"

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

my_window = Tk.Tk()

note = ttk.Notebook(my_window)

big_pane1 = PanedWindow(orient=HORIZONTAL)
big_pane1.pack(fill=BOTH, expand=1)
left = Red_Frame(big_pane1)
big_pane1.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
big_pane1.add(right)
top = Orange_Frame(big_pane1)
right.add(top)
bottom = Yellow_Frame(big_pane1)
right.add(bottom)

big_pane2 = PanedWindow(orient=HORIZONTAL)
big_pane2.pack(fill=BOTH, expand=1)
left = Purple_Frame(big_pane2)
big_pane2.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
big_pane2.add(right)
top = Blue_Frame(big_pane2)
right.add(top)
bottom = Green_Frame(big_pane2)
right.add(bottom)

big_pane3 = PanedWindow(orient=HORIZONTAL)
big_pane3.pack(fill=BOTH, expand=1)
left = Cyan_Frame(big_pane3)
big_pane3.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
big_pane3.add(right)
top = Brown_Frame(big_pane3)
right.add(top)

iris = sns.load_dataset("iris")
graph = sns.swarmplot(x="species", y="petal_length", data=iris)
fig = graph.get_figure()

canvas = FigureCanvasTkAgg(fig, master=right)
bottom = canvas.get_tk_widget()

right.add(bottom)

tab1=big_pane1
tab2=big_pane2
tab3=big_pane3

note.add(tab1, text = "Tab One (EDA)")
note.add(tab2, text = "Tab Two (Visualizations)")
note.add(tab3, text = "Tab Three (Test)")

note.pack()

my_window.mainloop()