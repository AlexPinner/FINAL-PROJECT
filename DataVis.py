from tkinter import *
from tkinter import ttk

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

#Create main window
root = Tk.Tk()

#Create notebook (thing that controls the tabs)
note = ttk.Notebook(root)

#Create the EDA listbox
EDA_list = ["Pairplot","Correlation Matrix","Bar Chart","Scatter Plot","PCA"]

#Create the data cleaning listbox
Cleaning_list = ["Find and Replace","Scaling","Factorize","Feature Selection", "Outliers"]

def Len_Max(list_item):
    "Returns the length of the longest list item"
    len_max = 0
    for m in list_item:
        if len(m) > len_max:
            len_max = len(m)
    return len_max

def Create_Listbox(window, list_items):
    "Returns a listbox created in window and populated with list_items"

    listbox = Listbox(window, width=Len_Max(list_items))

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=1) #always pack scrollbar before listbox

    for m in list_items:
        listbox.insert(END, str(m))
    
    return listbox

def EDA_onSelect(evt):
    w = evt.widget
    #print(w.curselection())
    if(w.curselection()):
        index = int(w.curselection()[0])
        value = w.get(index)
        #switch case instead of this print
        print('You selected item %d: "%s"' % (index, value))

def Cleaning_onSelect(evt):
    w = evt.widget
    #print(w.curselection())
    if(w.curselection()):
        index = int(w.curselection()[0])
        value = w.get(index)
        #switch case instead of this print
        print('You selected item %d: "%s"' % (index, value))

#PLACEHOLDER FRAME, DELETE LATER
class Red_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="red"

###############################
##Create tab for data cleaning
#############################
Data_Cleaning_Pane = PanedWindow(orient=HORIZONTAL)
Data_Cleaning_Pane.pack(fill=BOTH, expand=1)
#Leftmost item, listbox
left = Frame(Data_Cleaning_Pane)
Data_Cleaning_Listbox = Create_Listbox(left, Cleaning_list)
Data_Cleaning_Listbox.bind('<<ListboxSelect>>', Cleaning_onSelect)
Data_Cleaning_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
Data_Cleaning_Pane.add(right)
#Top right item, canvas
Data_Cleaning_Table = Red_Frame(Data_Cleaning_Pane)
right.add(Data_Cleaning_Table)
#Bottom right item, controls
Data_Cleaning_Controls = Red_Frame(Data_Cleaning_Pane)
right.add(Data_Cleaning_Controls)


#################################################
##Create tab for exploratory data analysis (EDA)
###############################################
EDA_Pane = PanedWindow(orient=HORIZONTAL)
EDA_Pane.pack(fill=BOTH, expand=1)
#Leftmost item, listbox
left = Frame(EDA_Pane)
EDA_Listbox = Create_Listbox(left, EDA_list)
EDA_Listbox.bind('<<ListboxSelect>>', EDA_onSelect)
EDA_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
EDA_Pane.add(right)
#Top right item, canvas
EDA_Canvas = Red_Frame(EDA_Pane)
"""
try:
    fig = graph.get_figure()
except:
    fig = graph.fig
EDA_Canvas = FigureCanvasTkAgg(fig, master=EDA_Pane)
EDA_Canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
"""
right.add(EDA_Canvas)
#Bottom right item, controls
EDA_Controls = Red_Frame(EDA_Pane)
right.add(EDA_Controls)

###############################
##Add the tabs to the notebook
#############################
note.add(Data_Cleaning_Pane, text="Data Cleaning")
note.add(EDA_Pane, text="EDA")

note.pack()

root.mainloop()