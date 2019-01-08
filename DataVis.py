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

#print(font.names()) #all available fonts
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
    if(w.curselection()):
        #Get data about current selection
        index = int(w.curselection()[0])
        value = w.get(index)
        #Check ini for graph settings
        config.read('datavis.ini')
        #Display 'please stand by' image
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('PSB.png')
        a.imshow(img_arr)
        a.axis('off')
        EDA_Canvas.draw()

        if(index==0): #pairplot
            if(config.has_section('pairplot') and config.has_section('general')): #use custom vals for fig creation
                #import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                #import user graph settings
                pp_hue = config.get('pairplot', 'hue') #which column determines color of points
                pp_vars = config.get('pairplot', 'vars') #which columns to use in plot
                pp_kind = config.get('pairplot', 'kind') #fit regression line?
                pp_diag_kind = config.get('pairplot', 'diag_kind') #which graphs to use along diagonal
                #create and display custom graph
                pp = sns.pairplot(data=data, hue=pp_hue, vars=pp_vars, kind=pp_kind, diag_kind=pp_diag_kind)
                pp.savefig('pp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('pp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
            else: #go with default fig creation
                data = sns.load_dataset('Iris')
                data = data.dropna()
                pp = sns.pairplot(data=data, kind='reg', hue='species')
                pp.savefig('pp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('pp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
        elif(index==1): #correlation matrix
            if(config.has_section('correlation') and config.has_section('general')): #use custom vals for fig creation
                #import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                data = data.corr()
                #import user graph settings
                cm_annot = config.getboolean('correlation', 'annot') #print numbers in cells?
                cm_cbar = config.getboolean('correlation', 'cbar') #show colobar?
                cm_square = config.getboolean('correlation', 'square') #make cells square?
                fig.clear()
                a = fig.add_subplot(111)
                #create and display custom graph
                sns.heatmap(data=data, annot=cm_annot, cbar=cm_cbar, square=cm_square, ax=a)
                EDA_Canvas.draw()
            else: #go with default fig creation
                data = sns.load_dataset('titanic')
                data = data.dropna()
                data = data.corr()
                fig.clear()
                a = fig.add_subplot(111)
                sns.heatmap(data=data, ax=a)
                EDA_Canvas.draw()
        elif (index==2): #bar chart
            if(config.has_section('bar') and config.has_section('general')): #use custom vals for fig creation
                #import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                #import user graph settings
                bp_x = config.get('bar', 'x') #x var
                bp_y = config.get('bar', 'y') #y var
                bp_hue = config.get('bar', 'hue') #hue column
                bp_ci = config.get('bar', 'ci') #confidence intervals
                bp_orient = config.get('bar', 'orient') #vertical or horizontal
                fig.clear()
                a = fig.add_subplot(111)
                #create and display custom graph
                sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue, ci=bp_ci, orient=bp_orient, ax=a)
                EDA_Canvas.draw()
            else: #go with default fig creation
                data = sns.load_dataset("flights")
                data = data.dropna()
                fig.clear()
                a = fig.add_subplot(111)
                sns.barplot(data=data, x='month', y='passengers', ci=None, ax=a)
                EDA_Canvas.draw()
        elif (index==3): #scatter plot
            if(config.has_section('scatter') and config.has_section('general')): #use custom vals for fig creation
                #import user data set
                data = config.get('general', 'dataset_location')
                data = data.dropna()
                #import user graph settings
                sp_x = config.get('scatter', 'x') #x var
                sp_y = config.get('scatter', 'y') #y var
                sp_hue = config.get('scatter', 'hue') #hue column
                sp_legend = config.getboolean('scatter', 'legend') #display legend?
                sp_scatter = config.getboolean('scatter', 'scatter') #draw scatter?
                sp_fit_reg = config.get('scatter', 'fit_reg') #fit linear regression line?
                #create and display custom graph
                sp = sns.lmplot(data=data, x=sp_x, y=sp_y, hue=sp_hue, legend=sp_legend, scatter=sp_scatter, fit_reg=sp_fit_reg)
                sp.savefig('sp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('sp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
            else: #go with default fig creation
                data = sns.load_dataset("tips")
                data = data.dropna()
                sp = sns.lmplot(data=data, x="total_bill", y="tip")
                sp.savefig('sp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('sp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
        elif (index==4): #pca
            if(config.has_section('PCA') and config.has_section('general')): #use custom vals for fig creation
                print('You selected item %d: "%s"' % (index, value))
            else: #go with default fig creation
                print('You selected item %d: "%s"' % (index, value))
                fig.clear()
                EDA_Canvas.draw()


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