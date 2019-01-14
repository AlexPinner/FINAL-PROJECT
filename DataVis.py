from tkinter import filedialog
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import font

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# create main window
root = Tk.Tk()
root.geometry('2400x1200')

# print(font.names()) #all available fonts
myfont = font.nametofont('TkDefaultFont')
myfont.configure(size=24)
data = sns.load_dataset('Iris')
# Pre-brake fonts and window size so it doesn't happen later
sns.pairplot(data=data)

# create notebook (thing that controls the tabs)
note = ttk.Notebook(root)

# create config parser for ini files
config = ConfigParser()

# instantiate figure object for use in canvas
fig = Figure()

# create the EDA listbox list
EDA_list = ["Pairplot", "Correlation Matrix",
            "Bar Chart", "Scatter Plot", "PCA"]

# create the data cleaning listbox list
Cleaning_list = ["Find and Replace", "Scaling",
                 "Factorize", "Feature Selection", "Outliers"]


def Len_Max(list_item):
    "Returns the length of the longest list item"
    len_max = 0
    for m in list_item:
        if len(m) > len_max:
            len_max = len(m)
    return len_max


def Create_Listbox(window, list_items):
    "Returns a listbox created in window and populated with list_items"
    # font=('Fixed', 14) #stick this in Listbox() after width=...
    listbox = Listbox(window, width=Len_Max(list_items))

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)  # always pack scrollbar before listbox

    listbox.config(yscrollcommand=scrollbar.set)
    # always pack scrollbar before listbox
    listbox.pack(side=LEFT, fill=BOTH, expand=1)

    for m in list_items:
        listbox.insert(END, str(m))

    return listbox


def Settings_Reset_Warning():
    "Creates modal dialog to ensure user wants to change dataset even if it resets ini settings"
    dlg = Toplevel(master=root)
    dlg.transient(root)
    dlg.grab_set()
    ask = BooleanVar()
    cont = BooleanVar()

    def Yes():
        cont.set(True)
        dlg.destroy()

    def No():
        cont.set(False)
        dlg.destroy()

    Label(dlg, text="Switching datasets will reset any graph settings\n that are sensitive to data changes. Continue?").grid(
        row=0, columnspan=2)
    Button(dlg, text="Continue", command=Yes).grid(
        row=1, column=0, sticky='ne')
    Button(dlg, text="Cancel", command=No).grid(row=1, column=1, sticky='nw')
    Checkbutton(dlg, variable=ask, text="Don't ask again", padx=2,
                pady=2).grid(row=2, columnspan=2, sticky='s')
    dlg.wait_window(dlg)
    if(ask.get()):
        config.read('datavis.ini')
        config.set('general', 'settings_reset_warning', 'False')
        with open('datavis.ini', 'w') as configfile:
            config.write(configfile)
    print(cont.get())
    return cont.get()


def Select_Dataset():
    "Prompt user to select a dataset file"
    filename = filedialog.askopenfilename(initialdir="/", title="Select Dataset", filetypes=(
        ("csv files", "*.csv"), ("xls files", "*.xls"), ("all files", "*.*")))
    config.read('datavis.ini')
    curr = config.get('general', 'dataset_location')
    if filename and (curr != filename):  # new dataset?
        if config.getboolean('general', 'settings_reset_warning'):  # ask again?
            if Settings_Reset_Warning():  # continue?
                Update_Data_Loc(filename)  # change dataset


def Update_Data_Loc(string):
    "Saves updated data location to ini"
    config = ConfigParser()
    config.read('datavis.ini')
    config.set('general', 'dataset_location', string)
    with open('datavis.ini', 'w') as configfile:
        config.write(configfile)


def Reset_ini(degree):  # FINISH ME
    "Reset ini to various degrees. 0 is all settings. 1 is only settings affected by dataset changes."
    if degree == 0:  # full reset
        pass
    else:  # partial reset
        pass


def EDA_onSelect(evt):
    w = evt.widget
    if(w.curselection()):
        # get data about current selection
        index = int(w.curselection()[0])
        value = w.get(index)
        # Check ini for graph settings
        config.read('datavis.ini')
        # display 'please stand by' image
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('PSB.png')
        a.imshow(img_arr)
        a.axis('off')
        EDA_Canvas.draw()

        if(index == 0):  # pairplot
            # use custom vals for fig creation
            if(config.has_section('pairplot') and config.has_section('general')):
                # import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                # import user graph settings
                # which column determines color of points
                pp_hue = config.get('pairplot', 'hue')
                # which columns to use in plot
                pp_vars = config.get('pairplot', 'vars')
                # fit regression line?
                pp_kind = config.get('pairplot', 'kind')
                # which graphs to use along diagonal
                pp_diag_kind = config.get('pairplot', 'diag_kind')
                # create and display custom graph
                pp = sns.pairplot(data=data, hue=pp_hue, vars=pp_vars,
                                  kind=pp_kind, diag_kind=pp_diag_kind)
                pp.savefig('pp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('pp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
            else:  # go with default fig creation
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
        elif(index == 1):  # correlation matrix
            # use custom vals for fig creation
            if(config.has_section('correlation') and config.has_section('general')):
                # import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                data = data.corr()
                # import user graph settings
                cm_annot = config.getboolean(
                    'correlation', 'annot')  # print numbers in cells?
                cm_cbar = config.getboolean(
                    'correlation', 'cbar')  # show colobar?
                cm_square = config.getboolean(
                    'correlation', 'square')  # make cells square?
                fig.clear()
                a = fig.add_subplot(111)
                # create and display custom graph
                sns.heatmap(data=data, annot=cm_annot,
                            cbar=cm_cbar, square=cm_square, ax=a)
                EDA_Canvas.draw()
            else:  # go with default fig creation
                data = sns.load_dataset('titanic')
                data = data.dropna()
                data = data.corr()
                fig.clear()
                a = fig.add_subplot(111)
                sns.heatmap(data=data, ax=a)
                EDA_Canvas.draw()
        elif (index == 2):  # bar chart
            # use custom vals for fig creation
            if(config.has_section('bar') and config.has_section('general')):
                # import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                # import user graph settings
                bp_x = config.get('bar', 'x')  # x var
                bp_y = config.get('bar', 'y')  # y var
                bp_hue = config.get('bar', 'hue')  # hue column
                bp_ci = config.get('bar', 'ci')  # confidence intervals
                # vertical or horizontal
                bp_orient = config.get('bar', 'orient')
                fig.clear()
                a = fig.add_subplot(111)
                # create and display custom graph
                sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue,
                            ci=bp_ci, orient=bp_orient, ax=a)
                EDA_Canvas.draw()
            else:  # go with default fig creation
                data = sns.load_dataset("flights")
                data = data.dropna()
                fig.clear()
                a = fig.add_subplot(111)
                sns.barplot(data=data, x='month',
                            y='passengers', ci=None, ax=a)
                EDA_Canvas.draw()
        elif (index == 3):  # scatter plot
            # use custom vals for fig creation
            if(config.has_section('scatter') and config.has_section('general')):
                # import user data set
                data = config.get('general', 'dataset_location')
                data = data.dropna()
                # import user graph settings
                sp_x = config.get('scatter', 'x')  # x var
                sp_y = config.get('scatter', 'y')  # y var
                sp_hue = config.get('scatter', 'hue')  # hue column
                sp_legend = config.getboolean(
                    'scatter', 'legend')  # display legend?
                sp_scatter = config.getboolean(
                    'scatter', 'scatter')  # draw scatter?
                # fit linear regression line?
                sp_fit_reg = config.get('scatter', 'fit_reg')
                # create and display custom graph
                sp = sns.lmplot(data=data, x=sp_x, y=sp_y, hue=sp_hue,
                                legend=sp_legend, scatter=sp_scatter, fit_reg=sp_fit_reg)
                sp.savefig('sp.png')
                fig.clear()
                a = fig.add_subplot(111)
                img_arr = mpimg.imread('sp.png')
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
            else:  # go with default fig creation
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
        elif (index == 4):  # pca
            # use custom vals for fig creation
            if(config.has_section('PCA') and config.has_section('general')):
                print('You selected item %d: "%s"' % (index, value))
            else:  # go with default fig creation
                print('You selected item %d: "%s"' % (index, value))
                fig.clear()
                EDA_Canvas.draw()


def Cleaning_onSelect(evt):
    w = evt.widget
    # print(w.curselection())
    if(w.curselection()):
        index = int(w.curselection()[0])
        value = w.get(index)
        if(index == 0):  # find and replace
            print('You selected item %d: "%s"' % (index, value))
        elif(index == 1):  # scaling
            print('You selected item %d: "%s"' % (index, value))
        elif (index == 2):  # factorize
            print('You selected item %d: "%s"' % (index, value))
        elif (index == 3):  # feature selection
            print('You selected item %d: "%s"' % (index, value))
        elif (index == 4):  # outliers
            print('You selected item %d: "%s"' % (index, value))


class Red_Frame(Frame):  # PLACEHOLDER FRAME, DELETE LATER
    def __init__(self, the_window):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "red"


class PP_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
    config.read('datavis.ini')
    data_loc = config.get('general', 'dataset_location')
    data = pd.read_csv(data_loc, encoding='latin-1')
    # which column determines color of points
    pp_hue = config.get('pairplot', 'hue')
    # which columns to use in plot
    pp_vars = config.get('pairplot', 'vars')
    # fit regression line?
    pp_kind = config.get('pairplot', 'kind')
    # which graphs to use along diagonal
    pp_diag_kind = config.get('pairplot', 'diag_kind')


#################
# Create toolbar
###############
toolbar = Frame(master=root, bd=1, relief='raised')
toolbar.pack(side=TOP, fill=X)
photo = PhotoImage(file="open_file.png")
import_btn = Button(toolbar, image=photo, command=lambda: Select_Dataset())
import_btn.pack(side='left')


###############################
# Create tab for data cleaning
#############################
Data_Cleaning_Pane = PanedWindow(orient=HORIZONTAL)
Data_Cleaning_Pane.pack(fill=BOTH, expand=1)
# Leftmost item, listbox
left = Frame(Data_Cleaning_Pane)
Data_Cleaning_Listbox = Create_Listbox(left, Cleaning_list)
Data_Cleaning_Listbox.bind('<<ListboxSelect>>', Cleaning_onSelect)
Data_Cleaning_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
Data_Cleaning_Pane.add(right)
# Top right item, canvas
Data_Cleaning_Table = Red_Frame(Data_Cleaning_Pane)
right.add(Data_Cleaning_Table)
# Bottom right item, controls
Data_Cleaning_Controls = Red_Frame(Data_Cleaning_Pane)
right.add(Data_Cleaning_Controls)


#################################################
# Create tab for exploratory data analysis (EDA)
###############################################
EDA_Pane = PanedWindow(orient=HORIZONTAL)
EDA_Pane.pack(fill=BOTH, expand=1)
# Leftmost item, listbox
left = Frame(EDA_Pane)
EDA_Listbox = Create_Listbox(left, EDA_list)
EDA_Listbox.bind('<<ListboxSelect>>', EDA_onSelect)
EDA_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
EDA_Pane.add(right)
# Top right item, canvas
# EDA_Canvas = Red_Frame(EDA_Pane)
EDA_Canvas = FigureCanvasTkAgg(fig, master=right)
top = EDA_Canvas.get_tk_widget()
right.add(top, stretch='first')
# Bottom right item, controls
EDA_Controls = Red_Frame(EDA_Pane)
right.add(EDA_Controls)


###############################
# Add the tabs to the notebook
#############################
note.add(Data_Cleaning_Pane, text="Data Cleaning")
note.add(EDA_Pane, text="EDA")

note.pack(fill=BOTH, expand=1)

root.mainloop()
