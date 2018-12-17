import matplotlib
matplotlib.use("TkAgg")
from tkinter import *
from tkinter import ttk

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

my_window = Tk.Tk()

"""
#Testing the window to see if all is well
class Red_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=250
        self["width"]=250
        self["bg"]="red"

red = Red_Frame(my_window)
red.pack()
"""

"""
#This is for normal figure construction and display in a canvas object, sans seaborn
from numpy import arange, sin, pi
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

a.plot(t, s)
canvas = FigureCanvasTkAgg(f, master=my_window)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
"""

"""
#This example works for sns plots that are actually plots, if it doesn't work try next example
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

iris = sns.load_dataset("iris")
graph = sns.swarmplot(x="species", y="petal_length", data=iris)
fig = graph.get_figure()

canvas = FigureCanvasTkAgg(fig, master=my_window)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
"""

"""
#This should work for any sns plots that don't count as plots and don't have the get_figure method, instead access the fig object directly
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

iris = sns.load_dataset("iris")
graph = sns.factorplot(data=iris)
fig = graph.fig

canvas = FigureCanvasTkAgg(fig, master=my_window)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

#this section will be a function that's called when listbox changes or control panel applies (maybe two seperate functions? One for listbox changes and the other for control panel changes?)
fig.clear()
graph = sns.swarmplot(x="species", y="petal_length", data=iris)
#^^^ or sns.whatever graph from listbox(whatever params from control panel)
fig = graph.get_figure()
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use("TkAgg")
import matplotlib.animation as animation

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

canvas = FigureCanvasTkAgg(f, my_window)
canvas.show()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, my_window)
toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

ani = animation.FuncAnimation(f, animate, interval=1000)

my_window.mainloop()