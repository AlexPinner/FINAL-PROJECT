import tkinter as tk
from tkinter import Frame, Label, Button, PanedWindow, Listbox, Toplevel, Scrollbar
from tkinter import HORIZONTAL, VERTICAL, LEFT, RIGHT, TOP, BOTTOM, Y, X, BOTH, END
from tkinter import filedialog, ttk, font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# create main window
root = tk.Tk()
root.title('DataVis')
root.geometry('{}x{}'.format(2400, 1200))

# print(font.names()) #all available fonts
myfont = font.nametofont('TkDefaultFont')
myfont.configure(size=24)
# Pre-brake fonts and window size so it doesn't happen later
data = sns.load_dataset('Iris')
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
        configfile.close()
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
    configfile.close()


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

        if (index == 0):  # pairplot
            # use custom vals for fig creation
            if(config.has_section('pairplot') and config.has_section('general')):
                # import user data set
                data_loc = config.get('general', 'dataset_location')
                data = pd.read_csv(data_loc, encoding='latin-1')
                data = data.dropna()
                # import user graph settings
                # which column determines color of points
                pp_hue = config.get('pairplot', 'hue')
                if pp_hue == 'None':
                    pp_hue = None
                print('Hue: ', pp_hue)
                # which columns to use in plot
                pp_vars = config.get('pairplot', 'vars').split(',')
                if pp_vars == ['None'] or pp_vars == ['']:
                    pp_vars = None
                print('Vars: ', pp_vars)
                # fit regression line?
                pp_kind = config.get('pairplot', 'kind')
                print('Kind: ', pp_kind)
                # which graphs to use along diagonal
                pp_diag_kind = config.get('pairplot', 'diag_kind')
                print('Diag_Kind: ', pp_diag_kind)
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
        elif (index == 1):  # correlation matrix
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


class Blue_Frame(Frame):  # PLACEHOLDER FRAME, DELETE LATER
    def __init__(self, the_window):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "blue"


class Green_Frame(Frame):  # PLACEHOLDER FRAME, DELETE LATER
    def __init__(self, the_window):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "green"


class Yellow_Frame(Frame):  # PLACEHOLDER FRAME, DELETE LATER
    def __init__(self, the_window):
        super().__init__()
        self["height"] = 150
        self["width"] = 150
        self["bg"] = "yellow"


def raise_frame(frame):
    frame.tkraise()


class PP_Frame(Frame):
    def __init__(self, parent):
        super().__init__()

        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        data = pd.read_csv(data_loc, encoding='latin-1')

        # need column list for the optionMenu for both pp hue and vars
        columns = data.columns
        numeric_columns = data.select_dtypes(exclude=['object'])
        columns_list = list()
        numeric_columns_list = list()

        for column in columns:
            columns_list.append(column)

        for column in numeric_columns:
            numeric_columns_list.append(column)

        # set pairplot settings to defaults
        # which column determines color of points
        pp_hue = Variable(value='None')
        # which columns to use in plot
        pp_vars = None
        # fit regression line?
        pp_kind = Variable(value='scatter')
        # which graphs to use along diagonal
        pp_diag_kind = Variable(value='hist')
        diag_kind_list = list(['auto', 'hist', 'kde'])

        # set pp settings to previous user settings if applicable
        if config.has_section('pairplot'):
            if config.has_option('pairplot', 'hue'):
                pp_hue = Variable(value=config.get('pairplot', 'hue'))
            if config.has_option('pairplot', 'vars'):
                pp_vars = config.get('pairplot', 'vars').split(',')
                if pp_vars == 'None' or pp_vars == ['']:
                    pp_vars = None
            if config.has_option('pairplot', 'kind'):
                pp_kind = Variable(value=config.get('pairplot', 'kind'))
            if config.has_option('pairplot', 'diag_kind'):
                pp_diag_kind = Variable(
                    value=config.get('pairplot', 'diag_kind'))

        pad_size = 20

        vars_frame = Frame(self)
        vars_frame.grid(row=0, column=0, padx=pad_size)
        vars_label = Label(vars_frame, text='Columns to use in plot:')
        vars_label.pack()
        vars_listbox = Listbox(vars_frame, selectmode=MULTIPLE, justify=CENTER)
        for column in numeric_columns_list:
            vars_listbox.insert(END, column)
        if not pp_vars == None:
            for var in pp_vars:
                i = vars_listbox.get(0, END).index(var)
                print(i)
                vars_listbox.select_set(i)
        # vars_listbox.select_set(0, END)  # all columns selected by default
        # update this select_set to go off of which vars from the column list are on
        # based on whats in the ini (pp_vars) instead of just selecting all
        vars_listbox.pack()
        vars_listbox.config(height=0)

        hue_frame = Frame(self)
        hue_frame.grid(row=0, column=1, padx=pad_size)
        hue_label = Label(hue_frame, text='Column that determines hue:')
        hue_label.pack()
        hue_option = Tk.OptionMenu(hue_frame, pp_hue, 'None', *columns_list)
        hue_option.pack()

        kind_frame = Frame(self)
        kind_frame.grid(row=0, column=2, padx=pad_size)
        kind_label = Label(kind_frame, text='Fit regression line:')
        kind_label.pack()

        def update_text():
            kind_checkbox.config(text=str(pp_kind.get()))
        kind_checkbox = Checkbutton(kind_frame, variable=pp_kind, onvalue='reg',
                                    offvalue='scatter', command=update_text, relief=RAISED)
        kind_checkbox.pack()
        update_text()

        diag_kind_frame = Frame(self)
        diag_kind_frame.grid(row=0, column=3, padx=pad_size)
        diag_kind_label = Label(
            diag_kind_frame, text='Graph type along diagonal:')
        diag_kind_label.pack()
        diag_kind_option = Tk.OptionMenu(
            diag_kind_frame, pp_diag_kind, *diag_kind_list)
        diag_kind_option.pack()

        # add preview button as well as apply button
        # since updating the graph as the user makes changes would be too slow
        # but they may want to preview their changes rather than just applying off the bat

        def preview_on_select():
            preview_hue = pp_hue.get()
            if preview_hue == 'None':
                preview_hue = None
            # print(preview_hue)
            items = vars_listbox.curselection()
            preview_vars = [numeric_columns_list[int(item)] for item in items]
            if preview_vars == []:
                preview_vars = None
            # print(preview_vars)
            preview_kind = pp_kind.get()
            # print(preview_kind)
            preview_diag_kind = pp_diag_kind.get()
            # print(preview_diag_kind)
            pp = sns.pairplot(data=data, hue=preview_hue, vars=preview_vars,
                              kind=preview_kind, diag_kind=preview_diag_kind)
            pp.savefig('pp.png')
            fig.clear()
            a = fig.add_subplot(111)
            img_arr = mpimg.imread('pp.png')
            a.imshow(img_arr)
            a.axis('off')
            EDA_Canvas.draw()
            # may have to make graph drawing a seperate function at some point since graphs will be drawn by listbox on select using ini settings, or here without using the ini settings
            # the apply on select may as well select a listbox index just to recall the listbox on select graph redraw since it just updated the ini that will be used by the listbox redrawing
            # but for this preview it will be based on the current settings and not ini
            # could also just leave it as is and avoid complex function nonsense

        def apply_on_select():
            if not config.has_section('pairplot'):
                config.add_section('pairplot')

            apply_hue = pp_hue.get()
            config.set('pairplot', 'hue', apply_hue)
            if apply_hue == 'None':
                apply_hue = None
            # print(apply_hue)

            items = vars_listbox.curselection()
            apply_vars = [numeric_columns_list[int(item)] for item in items]
            config.set('pairplot', 'vars', ','.join(apply_vars))
            # ','.join(map(str, myList)) this does the same thing but for lists of ints
            if apply_vars == []:
                apply_vars = None
            # print(apply_vars)

            apply_kind = pp_kind.get()
            config.set('pairplot', 'kind', apply_kind)
            # print(apply_kind)

            apply_diag_kind = pp_diag_kind.get()
            config.set('pairplot', 'diag_kind', apply_diag_kind)
            # print(apply_diag_kind)

            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

            pp = sns.pairplot(data=data, hue=apply_hue, vars=apply_vars,
                              kind=apply_kind, diag_kind=apply_diag_kind)
            pp.savefig('pp.png')
            fig.clear()
            a = fig.add_subplot(111)
            img_arr = mpimg.imread('pp.png')
            a.imshow(img_arr)
            a.axis('off')
            EDA_Canvas.draw()

        button_frame = Frame(self)
        button_frame.grid(row=0, column=4, padx=pad_size)

        preview_button = Button(
            button_frame, text='Preview Settings', command=preview_on_select)
        preview_button.pack()

        apply_button = Button(
            button_frame, text='Apply Settings', command=apply_on_select)
        apply_button.pack()


class CM_Frame(Frame):
    def __init__(self, parent):
        super().__init__()

        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        data = pd.read_csv(data_loc, encoding='latin-1')

        # set correlation matrix settings to defaults
        # print numbers in cells?
        cm_annot = False
        # show color bar?
        cm_cbar = True
        # make cells square?
        cm_square = False

        # set cm settings to previous user settings if applicable
        if config.has_section('correlation'):
            if config.has_option('correlation', 'annot'):
                cm_annot = config.getboolean('correlation', 'annot')
            if config.has_option('correlation', 'cbar'):
                cm_cbar = config.getboolean('correlation', 'cbar')
            if config.has_option('correlation', 'kind'):
                cm_square = config.getboolean('correlation', 'kind')

        pad_size = 20

        annot_frame = Frame(self)
        annot_frame.grid(row=0, column=0, padx=pad_size)
        annot_label = Label(annot_frame, text='Show numbers in cells:')
        annot_label.pack()

        def update_annot_check():
            annot_checkbox.config(text=str(cm_annot))
        annot_checkbox = Checkbutton(
            annot_frame, variable=cm_annot, command=update_annot_check, relief=RAISED)
        annot_checkbox.pack()
        update_annot_check()

        cbar_frame = Frame(self)
        cbar_frame.grid(row=0, column=1, padx=pad_size)
        cbar_label = Label(cbar_frame, text='Show color bar:')
        cbar_label.pack()

        def update_cbar_check():
            cbar_checkbox.config(text=str(cm_cbar))
        cbar_checkbox = Checkbutton(
            cbar_frame, variable=cm_cbar, command=update_cbar_check, relief=RAISED)
        cbar_checkbox.pack()
        update_cbar_check()

        square_frame = Frame(self)
        square_frame.grid(row=0, column=2, padx=pad_size)
        square_label = Label(square_frame, text='Make cells square:')
        square_label.pack()

        def update_square_check():
            square_checkbox.config(text=str(cm_square))
        square_checkbox = Checkbutton(
            square_frame, variable=cm_square, command=update_square_check, relief=RAISED)
        square_checkbox.pack()
        update_square_check()

        def preview_on_select():
            preview_annot = cm_annot
            preview_cbar = cm_cbar
            preview_square = cm_square

            fig.clear()
            a = fig.add_subplot(111)
            sns.heatmap(data=data, annot=preview_annot,
                        cbar=preview_cbar, square=preview_square, ax=a)
            EDA_Canvas.draw()

        def apply_on_select():
            if not config.has_section('correlation'):
                config.add_section('correlation')

            apply_annot = cm_annot
            config.set('correlation', 'annot', apply_annot)

            apply_cbar = cm_cbar
            config.set('correlation', 'cbar', apply_cbar)

            apply_square = cm_square
            config.set('correlation', 'square', apply_square)

            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

            fig.clear()
            a = fig.add_subplot(111)
            sns.heatmap(data=data, annot=apply_annot,
                        cbar=apply_cbar, square=apply_square, ax=a)
            EDA_Canvas.draw()

        button_frame = Frame(self)
        button_frame.grid(row=0, column=3, padx=pad_size)

        preview_button = Button(
            button_frame, text='Preview Settings', command=preview_on_select)
        preview_button.pack()

        apply_button = Button(
            button_frame, text='Apply Settings', command=apply_on_select)
        apply_button.pack()


class BP_Frame(Frame):
    def __init__(self, parent):
        super().__init__()

        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        data = pd.read_csv(data_loc, encoding='latin-1')

        columns = data.columns
        numeric_columns = data.select_dtypes(exclude=['object'])
        columns_list = list()
        numeric_columns_list = list()

        for column in columns:
            columns_list.append(column)

        for column in numeric_columns:
            numeric_columns_list.append(column)

        # set barplot settings to defaults
        # column for x
        bp_x = None
        # column for y
        bp_y = None
        # which column determines hue?
        bp_hue = None
        # show confidence intervals?
        bp_ci = Variable(value='None')

        # set bp settings to previous user settings if applicable
        if config.has_section('bar'):
            if config.has_option('bar', 'x'):
                bp_x = config.get('bar', 'x')
                if bp_x == 'None':
                    bp_x = None
            if config.has_option('bar', 'y'):
                bp_y = config.get('bar', 'y')
                if bp_y == 'None':
                    bp_y = None
            if config.has_option('bar', 'hue'):
                bp_hue = config.get('bar', 'hue')
                if bp_hue == 'None':
                    bp_hue = None
            if config.has_option('bar', 'ci'):
                bp_ci = config.get('bar', 'ci')
                if bp_ci == 'None':
                    bp_ci = None

        pad_size = 20

        x_frame = Frame(self)
        x_frame.grid(row=0, column=0, padx=pad_size)
        x_label = Label(x_frame, text='Column to use for x:')
        x_label.pack()
        x_listbox = Listbox(x_frame, selectmode=SINGLE, justify=CENTER)
        for column in columns_list:
            x_listbox.insert(END, column)
        x_listbox.pack()
        x_listbox.config(height=0)

        y_frame = Frame(self)
        y_frame.grid(row=0, column=1, padx=pad_size)
        y_label = Label(y_frame, text='Column to use for y:')
        y_label.pack()
        y_listbox = Listbox(y_frame, selectmode=SINGLE, justify=CENTER)
        for column in numeric_columns_list:
            y_listbox.insert(END, column)
        y_listbox.pack()
        y_listbox.config(height=0)

        hue_frame = Frame(self)
        hue_frame.grid(row=0, column=2, padx=pad_size)
        hue_label = Label(hue_frame, text='Column to use for hue:')
        hue_label.pack()
        hue_listbox = Listbox(hue_frame, selectmode=SINGLE, justify=CENTER)
        for column in columns_list:
            hue_listbox.insert(END, column)
        hue_listbox.pack()
        hue_listbox.config(height=0)

        ci_frame = Frame(self)
        ci_frame.grid(row=0, column=3, padx=pad_size)
        ci_label = Label(ci_frame, text='Confidence interval:')
        ci_label.pack()

        def update_text():
            ci_checkbox.config(text=str(bp_ci.get()))
        ci_checkbox = Checkbutton(ci_frame, variable=bp_ci, onvalue='sd',
                                  offvalue='None', command=update_text, relief=RAISED)
        ci_checkbox.pack()
        update_text()

        def preview_on_select():
            preview_x = bp_x
            preview_y = bp_y
            preview_hue = bp_hue
            preview_ci = bp_ci

            fig.clear()
            a = fig.add_subplot(111)
            sns.barplot(data=data, x=preview_x, y=preview_y,
                        hue=preview_hue, ci=preview_ci, ax=a)
            EDA_Canvas.draw()

        def apply_on_select():
            if not config.has_section('bar'):
                config.add_section('bar')

            apply_x = bp_x
            config.set('bar', 'x', apply_x)

            apply_y = bp_y
            config.set('bar', 'y', apply_y)

            apply_hue = bp_hue
            config.set('bar', 'hue', apply_hue)

            apply_ci = bp_ci.get()
            config.set('bar', 'ci', apply_ci)

            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

            fig.clear()
            a = fig.add_subplot(111)
            sns.barplot(data=data, x=apply_x, y=apply_y,
                        hue=apply_hue, ci=apply_ci, ax=a)
            EDA_Canvas.draw()

        button_frame = Frame(self)
        button_frame.grid(row=0, column=4, padx=pad_size)

        preview_button = Button(
            button_frame, text='Preview Settings', command=preview_on_select)
        preview_button.pack()

        apply_button = Button(
            button_frame, text='Apply Settings', command=apply_on_select)
        apply_button.pack()


#################
# Create toolbar
###############
toolbar = Frame(master=root, bd=1, relief='raised')
#toolbar.pack(side=TOP, fill=X)
toolbar.grid(sticky='new')
#toolbar.grid_columnconfigure(0, weight=1)
#toolbar.grid_rowconfigure(0, weight=1)
photo = tk.PhotoImage(file="open_file.png")
import_btn = Button(toolbar, image=photo, command=lambda: Select_Dataset())
# import_btn.pack(side='left')
import_btn.grid(sticky='w')
#import_btn.grid_columnconfigure(0, weight=1)
#import_btn.grid_rowconfigure(0, weight=1)


###############################
# Create tab for data cleaning
#############################
Data_Cleaning_Pane = PanedWindow(orient=HORIZONTAL)
#Data_Cleaning_Pane.pack(fill=BOTH, expand=1)
Data_Cleaning_Pane.grid(sticky='nesw')
#Data_Cleaning_Pane.grid_columnconfigure(0, weight=1)
#Data_Cleaning_Pane.grid_rowconfigure(0, weight=1)
# Leftmost item, listbox
left = Frame(Data_Cleaning_Pane)
Data_Cleaning_Listbox = Create_Listbox(left, Cleaning_list)
Data_Cleaning_Listbox.bind('<<ListboxSelect>>', Cleaning_onSelect)
Data_Cleaning_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
#right.pack(fill=BOTH, expand=1)
right.grid(sticky='nesw')
#right.grid_columnconfigure(0, weight=1)
#right.grid_rowconfigure(0, weight=1)
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
#EDA_Pane.pack(fill=BOTH, expand=1)
EDA_Pane.grid(sticky='nesw')
#EDA_Pane.grid_columnconfigure(0, weight=1)
#DA_Pane.grid_rowconfigure(0, weight=1)
# Leftmost item, listbox
left = Frame(EDA_Pane)
EDA_Listbox = Create_Listbox(left, EDA_list)
EDA_Listbox.bind('<<ListboxSelect>>', EDA_onSelect)
EDA_Pane.add(left)
right = PanedWindow(orient=VERTICAL)
#right.pack(fill=BOTH, expand=1)
right.grid(sticky='nesw')
#right.grid_columnconfigure(0, weight=1)
#right.grid_rowconfigure(0, weight=1)
EDA_Pane.add(right)
# Top right item, canvas
# EDA_Canvas = Red_Frame(EDA_Pane)
EDA_Canvas = FigureCanvasTkAgg(fig, master=right)
top = EDA_Canvas.get_tk_widget()
right.add(top, stretch='first')
# Bottom right item, controls
EDA_Controls = Frame(EDA_Pane)
EDA_Controls.grid(sticky='nesw')
right.add(EDA_Controls)
"""
PP_Controls = PP_Frame(EDA_Controls)
CM_Controls = CM_Frame(EDA_Controls)
BP_Controls = BP_Frame(EDA_Controls)

for frame in (PP_Controls, CM_Controls, BP_Controls):
    #frame.grid(row=0, column=0, sticky='news')
    frame.pack()
"""

###############################
# Add the tabs to the notebook
#############################
note.add(Data_Cleaning_Pane, text="Data Cleaning")
note.add(EDA_Pane, text="EDA")

#note.pack(fill=BOTH, expand=1)
note.grid(sticky='nesw')
#note.grid_columnconfigure(0, weight=1)
#note.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
