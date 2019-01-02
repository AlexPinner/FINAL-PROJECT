"""
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from io import StringIO
import pandas as pd
import matplotlib
import numpy as np
from tkinter import *
#from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg

root=Tk()

fig = Figure()
df = sns.load_dataset("iris")

sns_plot = sns.pairplot(df)
#png_output = StringIO()
sns_plot.savefig('plot.jpg')

img = mpimg.imread('plot.jpg')
#canvas = Canvas()
#canvas.print_png(png_output)
#print(png_output.getvalue())

#imgPath = r"plot.png"
#photo = PhotoImage(file = imgPath)
#label = Label(image = photo)
#label.image = photo # keep a reference!
#label.pack()
#canvas.create_image('plot.png')

#img = Image.open("plot.png")
#filename = ImageTk.PhotoImage(img)

a = fig.add_subplot(111)
a.imshow(img)
#canvas = Canvas(root,height=img.size[0],width=img.size[1])
#canvas.image = filename  # <--- keep reference of your image
#canvas.create_image(0,0,anchor='nw',image=filename)
#canvas.pack()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
canvas.draw()

root.mainloop()
"""

from tkinter import *
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import array, arange, sin, pi

root = Tk()
root_panel = Frame(root)
root_panel.pack(side="bottom", fill="both", expand="yes")

btn_panel = Frame(root_panel, height=35)
btn_panel.pack(side='top', fill="both", expand="yes")

#imgplot = plt.imshow(img_arr)

f = Figure()
a = f.add_subplot(111)

data = sns.load_dataset('Iris')
data = data.dropna()
pp = sns.pairplot(data=data, kind='reg')
pp.savefig('pp.png')

img_arr = mpimg.imread('pp.png')
a.imshow(img_arr)
#a.set_xticks([])
#a.set_yticks([])
#a.axis('off')

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
canvas._tkcanvas.pack(side="top", fill="both", expand=1)

root.mainloop()