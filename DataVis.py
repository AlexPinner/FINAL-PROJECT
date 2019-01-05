from tkinter import *
from tkinter import ttk
from tkinter import font

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
import matplotlib.image as mpimg

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

#Create main window
root = Tk.Tk()

print(font.names())
myfont = font.nametofont('TkDefaultFont')
myfont.configure(size=24)
data = sns.load_dataset('Iris')
sns.pairplot(data=data)

#Create notebook (thing that controls the tabs)
note = ttk.Notebook(root)

#Create config parser for ini files
config = ConfigParser()

#Forward declare figure object for use in canvas
#data = sns.load_dataset("iris")
#data = data.dropna()
#graph = sns.pairplot(data=data, kind="reg")
#fig = graph.fig

fig = Figure()
#a = fig.add_subplot(111)

#Create the EDA listbox list
EDA_list = ["Pairplot","Correlation Matrix","Bar Chart","Scatter Plot","PCA"]

#Create the data cleaning listbox list
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
    #font=('Fixed', 14) #stick this in Listbox() after width=...
    listbox = Listbox(window, width=Len_Max(list_items))

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y) #always pack scrollbar before listbox
    
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=1) #always pack scrollbar before listbox

    for m in list_items:
        listbox.insert(END, str(m))
    
    return listbox

def EDA_onSelect(evt):
    w = evt.widget
    #print(w.curselection())
    if(w.curselection()):
        #print(w.curselection())
        #clear_fig()
        #Get data about current selection
        index = int(w.curselection()[0])
        value = w.get(index)
        #Read ini file to check for presets
        config.read('test.ini')
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('PSB.png')
        a.imshow(img_arr)
        a.axis('off')
        EDA_Canvas.draw()
        #Pairplot
        if(index==0):
            if(config.has_section('Pairplot')):
                #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else:
                #go with default fig creation
                print('You selected item %d: "%s"' % (index, value))
                data = sns.load_dataset('Iris')
                data = data.dropna()
                pp = sns.pairplot(data=data, kind='reg')
                pp.savefig('pp.png')
                #xList=[1,2,3,4]
                #yList=[2,4,8,16]
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('pp.png')
                a.imshow(img_arr)
                a.axis('off')
                #a.plot(xList, yList)
                EDA_Canvas.draw()
        #Correlation matrix
        elif(index==1):
            if(config.has_section('Correlation')):
                #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else:
                #go with default fig creation
                data = sns.load_dataset("titanic")
                data = data.dropna()
                data = data.corr()
                fig.clear()
                a = fig.add_subplot(111)
                sns.heatmap(data=data, ax=a)
                EDA_Canvas.draw()
        #Bar chart
        elif (index==2):
            if(config.has_section('Bar Chart')):
                #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else:
                #go with default fig creation
                data = sns.load_dataset("flights")
                data = data.dropna()
                fig.clear()
                a = fig.add_subplot(111)
                sns.barplot(data=data, x='month', y='passengers', ci=None, ax=a)
                EDA_Canvas.draw()
        #Scatter plot
        elif (index==3):
            if(config.has_section('Scatter Plot')):
                #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else:
                #go with default fig creation
                print('You selected item %d: "%s"' % (index, value))
                data = sns.load_dataset("tips")
                data = data.dropna()
                sp = sns.lmplot(data=data, x="total_bill", y="tip")
                sp.savefig('sp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('sp.png')
                a.imshow(img_arr)
                a.axis('off')
                ##plot = sns.lmplot(data=data, x="total_bill", y="tip")
                #sns.regplot(data=data, x='total_bill', y='tip', ax=a)
                #sns.residplot(x=data['total_bill'], y=data['tip'], ax=a)
                ##plot.savefig('plot.png')
                ##img = Image.open('plot.png')
                #filename = ImageTk.PhotoImage(img)
                ##a.imshow(img)
                EDA_Canvas.draw()
        #PCA
        elif (index==4):
            if(config.has_section('PCA')):
                #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else:
                #go with default fig creation
                print('You selected item %d: "%s"' % (index, value))
                fig.clear()
                #EDA_Listbox.configure(font=('Fixed', 14))
                EDA_Canvas.draw()
        #print('Tabs are: ', note.children.keys())
        #print('Active tab: ', note.select())
        #tabfont = font.Font(font=note.children[EDA]['font'])
        #print(tabfont.actual())


def Cleaning_onSelect(evt):
    w = evt.widget
    #print(w.curselection())
    if(w.curselection()):
        index = int(w.curselection()[0])
        value = w.get(index)
        #switch case instead of this print
        #print('You selected item %d: "%s"' % (index, value))
        if(index==0):
            print('You selected item %d: "%s"' % (index, value))
            #Find and replace
        elif(index==1):
            print('You selected item %d: "%s"' % (index, value))
            #Scaling
        elif (index==2):
            print('You selected item %d: "%s"' % (index, value))
            #Factorize
        elif (index==3):
            print('You selected item %d: "%s"' % (index, value))
            #Feature Selection
        elif (index==4):
            print('You selected item %d: "%s"' % (index, value))
            #Outliers

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
#EDA_Canvas = Red_Frame(EDA_Pane)
EDA_Canvas = FigureCanvasTkAgg(fig, master=right)
top = EDA_Canvas.get_tk_widget()
right.add(top, stretch='first')
#Bottom right item, controls
EDA_Controls = Red_Frame(EDA_Pane)
right.add(EDA_Controls)


###############################
##Add the tabs to the notebook
#############################
note.add(Data_Cleaning_Pane, text="Data Cleaning")
note.add(EDA_Pane, text="EDA")

note.pack(fill=BOTH, expand=1)

root.mainloop()