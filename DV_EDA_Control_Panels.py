import tkinter as tk
from configparser import ConfigParser
from tkinter import messagebox

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import DV_ZoomableCanvas


class PP_Frame(tk.Frame):
    def __init__(self, root, canvas_frame, **options):
        tk.Frame.__init__(self, root, **options)

        # Get ini options
        self.config = config = ConfigParser()
        config.read('datavis.ini')
        if config.has_section('general'):
            data_loc = config.get('general', 'dataset_location')
            self.data = pd.read_csv(data_loc, encoding='latin-1')
        else:
            self.data = sns.load_dataset('iris')
        self.data = self.data.dropna()

        # Lists for listboxes and option menus
        columns = self.data.columns
        numeric_columns = self.data.select_dtypes(exclude=['object', 'category'])
        self.columns_list = list()
        self.numeric_columns_list = list()
        self.columns_list.append('None') # so hue coloring can be set to off
        for col in columns:
            self.columns_list.append(col)
        for num_col in numeric_columns:
            self.numeric_columns_list.append(num_col)
        self.diag_kind_list = list(['auto', 'hist', 'kde'])

        # Default graph options
        self.pp_hue = tk.Variable(value='None') # which column determines color of points
        self.pp_vars = tuple() # which columns to use in plot
        self.pp_kind = tk.Variable(value='scatter') # fit regression line?
        self.pp_diag_kind = tk.Variable(value='auto') # graph type to use along diagonal

        # Load graph options from ini, if they don't exist create them and set to default values
        try:
            self.pp_hue = tk.Variable(value=config.get('pairplot', 'hue'))
            self.pp_vars = tuple(config.get('pairplot', 'vars').split(','))
            if not all(self.pp_vars):
                self.pp_vars = tuple()
            self.pp_kind = tk.Variable(value=config.get('pairplot', 'kind'))
            self.pp_diag_kind = tk.Variable(value=config.get('pairplot', 'diag_kind'))
        except:
            if not config.has_section('pairplot'):
                config.add_section('pairplot')
                config.set('pairplot', 'hue', self.pp_hue.get())
                config.set('pairplot', 'vars', ','.join(self.pp_vars))
                config.set('pairplot', 'kind', self.pp_kind.get())
                config.set('pairplot', 'diag_kind', self.pp_diag_kind.get())
                with open('datavis.ini', 'w') as configfile:
                    config.write(configfile)
                configfile.close()
        
        # General frame settings
        pad_size = 50
        listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        # PP HUE CONTROL FRAME
        hue_frame = tk.Frame(self)
        hue_frame.grid(row=0, column=2, padx=pad_size)

        hue_label = tk.Label(hue_frame, text='Column that determines hue:')
        hue_label.pack()

        def hue_update(self, choice):
            if choice in self.pp_vars:
                messagebox.showwarning(title='Invalid Choice', message='The column selected for hue cannot also be selected for use in plot.')
                self.pp_hue.set('None')

        hue_option = tk.OptionMenu(hue_frame, self.pp_hue, *self.columns_list, command=lambda x: hue_update(self, x))
        hue_option.pack()

        # PP VARS CONTROL FRAME
        vars_frame = tk.Frame(self)
        vars_frame.grid(row=0, column=1, padx=pad_size)
        vars_label = tk.Label(vars_frame, text='Columns to use in plot:')
        vars_label.pack()

        def vars_update(self, event):
            lbTup = event.widget.curselection()
            if lbTup:
                tmp = list()
                for tup in lbTup:
                    if not self.pp_hue.get() == self.numeric_columns_list[tup]: # make sure the vars selected are not overlapping with pp_hue
                        tmp.append(self.numeric_columns_list[tup])
                    else:
                        messagebox.showwarning(title='Invalid Selection', message='Columns chosen for graph cannot also be used for hue, the current selection has been updated')
                        vars_listbox.select_clear(tup)
                self.pp_vars = tuple(tmp)
                
        vars_listbox = tk.Listbox(vars_frame, selectmode=tk.MULTIPLE, justify=tk.CENTER)
        vars_listbox.bind('<<ListboxSelect>>', lambda x: vars_update(self, x))
        for num_column in self.numeric_columns_list:
            vars_listbox.insert(tk.END, num_column)
        for var in self.pp_vars:
            i = vars_listbox.get(0, tk.END).index(var)
            vars_listbox.select_set(i)
        vars_listbox.config(height=listbox_height)
        vars_listbox.pack(side=tk.LEFT)

        vars_scrollbar = tk.Scrollbar(vars_frame)
        vars_listbox.config(yscrollcommand=vars_scrollbar.set)
        vars_scrollbar.config(command=vars_listbox.yview)
        vars_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # PP KIND CONTROL FRAME
        kind_frame = tk.Frame(self)
        kind_frame.grid(row=0, column=3, padx=pad_size)

        kind_label = tk.Label(kind_frame, text='Fit regression line:')
        kind_label.pack()

        def update_text():
            kind_checkbox.config(text=str(self.pp_kind.get()))
        kind_checkbox = tk.Checkbutton(kind_frame, variable=self.pp_kind, onvalue='reg',
                                    offvalue='scatter', command=update_text, relief=tk.RAISED)
        kind_checkbox.pack()
        update_text()

        # PP DIAG KIND CONTROL FRAME
        diag_kind_frame = tk.Frame(self)
        diag_kind_frame.grid(row=0, column=4, padx=pad_size)

        diag_kind_label = tk.Label(
            diag_kind_frame, text='Graph type along diagonal:')
        diag_kind_label.pack()
        
        diag_kind_option = tk.OptionMenu(
            diag_kind_frame, self.pp_diag_kind, *self.diag_kind_list)
        diag_kind_option.pack()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=5, padx=pad_size)

        preview_button = tk.Button(
            button_frame, text='Preview Settings', command=lambda: self.preview_on_select(canvas_frame))
        preview_button.pack()

        apply_button = tk.Button(
            button_frame, text='Apply Settings', command=lambda: self.apply_on_select(canvas_frame))
        apply_button.pack()

    def preview_on_select(self, canvas_frame):
        preview_hue = self.pp_hue.get()
        if preview_hue == 'None':
            preview_hue = None
        preview_vars = self.pp_vars
        if not all(preview_vars) or preview_vars == ():
            preview_vars = None
        preview_kind = self.pp_kind.get()
        preview_diag_kind = self.pp_diag_kind.get()

        print('--PP ON PREVIEW--')
        print('Vars: ', preview_vars, type(preview_vars))
        print('Hue: ', preview_hue, type(preview_hue))
        print('kind: ', preview_kind, type(preview_kind))
        print('Diag Kind: ', preview_diag_kind, type(preview_diag_kind))

        plt.clf()
        pp = sns.pairplot(data=self.data, hue=preview_hue, vars=preview_vars, kind=preview_kind, diag_kind=preview_diag_kind)
        pp.savefig('pp.png')
        """
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
        """
        file = 'pp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

    def apply_on_select(self, canvas_frame):
        config = self.config

        apply_hue = self.pp_hue.get()
        config.set('pairplot', 'hue', apply_hue)
        if apply_hue == 'None':
            apply_hue = None
        
        apply_vars = self.pp_vars
        if not all(apply_vars) or apply_vars == ():
            apply_vars = tuple()
        config.set('pairplot', 'vars', ','.join(apply_vars))
        if not all(apply_vars) or apply_vars == ():
            apply_vars = None
        
        apply_kind = self.pp_kind.get()
        config.set('pairplot', 'kind', apply_kind)
        
        apply_diag_kind = self.pp_diag_kind.get()
        config.set('pairplot', 'diag_kind', apply_diag_kind)
        
        with open('datavis.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()

        print('--PP ON APPLY--')
        print('Vars: ', apply_vars, type(apply_vars))
        print('Hue: ', apply_hue, type(apply_hue))
        print('Kind: ', apply_kind, type(apply_kind))
        print('Diag Kind: ', apply_diag_kind, type(apply_diag_kind))

        plt.clf()
        pp = sns.pairplot(data=self.data, hue=apply_hue, vars=apply_vars, kind=apply_kind, diag_kind=apply_diag_kind)
        pp.savefig('pp.png')
        """
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
        """
        file = 'pp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

class CM_Frame(tk.Frame):
    def __init__(self, root, canvas_frame, **options):
        tk.Frame.__init__(self, root, **options)

        # Get ini options
        self.config  = config = ConfigParser()
        config.read('datavis.ini')
        if config.has_section('general'):
            data_loc = config.get('general', 'dataset_location')
            self.data = pd.read_csv(data_loc, encoding='latin-1')
        else:
            self.data = sns.load_dataset('titanic')
        self.data = self.data.dropna()
        self.data = self.data.corr()

        # Default graph options
        self.cm_annot = tk.BooleanVar(value='False') # print numbers in cells?
        self.cm_cbar = tk.BooleanVar(value='True') # show color bar?
        self.cm_square = tk.BooleanVar(value='False') # make cells square?

        # Load graph options from ini, if they don't exist create them and set to default values
        try:
            self.cm_annot = tk.BooleanVar(value=config.get('correlation', 'annot'))
            self.cm_cbar = tk.BooleanVar(value=config.get('correlation', 'cbar'))
            self.cm_square = tk.BooleanVar(value=config.get('correlation', 'square'))
        except:
            if not config.has_section('correlation'):
                config.add_section('correlation')
            config.set('correlation', 'annot', str(self.cm_annot.get()))
            config.set('correlation', 'cbar', str(self.cm_cbar.get()))
            config.set('correlation', 'square', str(self.cm_square.get()))
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

        # General frame settings
        pad_size = 50
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        # CM ANNOT CONTROL FRAME
        annot_frame = tk.Frame(self)
        annot_frame.grid(row=0, column=1, padx=pad_size)

        annot_label = tk.Label(annot_frame, text='Show numbers in cells:')
        annot_label.pack()

        def update_annot_check():
            annot_checkbox.config(text=str(self.cm_annot.get()))
        annot_checkbox = tk.Checkbutton(annot_frame, variable=self.cm_annot, onvalue='True', offvalue='False', command=update_annot_check, relief=tk.RAISED)
        annot_checkbox.pack()
        update_annot_check()

        # CM CBAR CONTROL FRAME
        cbar_frame = tk.Frame(self)
        cbar_frame.grid(row=0, column=2, padx=pad_size)

        cbar_label = tk.Label(cbar_frame, text='Show color bar:')
        cbar_label.pack()

        def update_cbar_check():
            cbar_checkbox.config(text=str(self.cm_cbar.get()))
        cbar_checkbox = tk.Checkbutton(cbar_frame, variable=self.cm_cbar, onvalue='True', offvalue='False', command=update_cbar_check, relief=tk.RAISED)
        cbar_checkbox.pack()
        update_cbar_check()

        # CM SQUARE CONTROL FRAME
        square_frame = tk.Frame(self)
        square_frame.grid(row=0, column=3, padx=pad_size)

        square_label = tk.Label(square_frame, text='Make cells square:')
        square_label.pack()

        def update_square_check():
            square_checkbox.config(text=str(self.cm_square.get()))
        square_checkbox = tk.Checkbutton(
            square_frame, variable=self.cm_square, onvalue='True', offvalue='False', command=update_square_check, relief=tk.RAISED)
        square_checkbox.pack()
        update_square_check()

        # CM BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=4, padx=pad_size)

        preview_button = tk.Button(
            button_frame, text='Preview Settings', command=lambda: self.preview_on_select(canvas_frame))
        preview_button.pack()

        apply_button = tk.Button(
            button_frame, text='Apply Settings', command=lambda: self.apply_on_select(canvas_frame))
        apply_button.pack()

    def preview_on_select(self, canvas_frame):
        preview_annot = self.cm_annot.get()
        preview_cbar = self.cm_cbar.get()
        preview_square = self.cm_square.get()

        print('--CM ON PREVIEW--')
        print('Annot: ', preview_annot, type(preview_annot))
        print('Cbar: ', preview_cbar, type(preview_cbar))
        print('Square: ', preview_square, type(preview_square))
        """
        fig.clear()
        a = fig.add_subplot(111)
        canvas.draw()
        """
        plt.clf()
        cm = sns.heatmap(data=self.data, annot=preview_annot, cbar=preview_cbar, square=preview_square)
        cm.get_figure().savefig('cm.png', bbox_inches='tight')
        file = 'cm.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

    def apply_on_select(self, canvas_frame):
        config = self.config

        apply_annot = self.cm_annot.get()
        config.set('correlation', 'annot', str(apply_annot))

        apply_cbar = self.cm_cbar.get()
        config.set('correlation', 'cbar', str(apply_cbar))

        apply_square = self.cm_square.get()
        config.set('correlation', 'square', str(apply_square))

        with open('datavis.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()

        print('--CM ON APPLY--')
        print('Annot: ', apply_annot, type(apply_annot))
        print('Cbar: ', apply_cbar, type(apply_cbar))
        print('Square: ', apply_square, type(apply_square))
        """
        fig.clear()
        a = fig.add_subplot(111)
        canvas.draw()
        """
        plt.clf()
        cm = sns.heatmap(data=self.data, annot=apply_annot, cbar=apply_cbar, square=apply_square)
        cm.get_figure().savefig('cm.png', bbox_inches='tight')
        file = 'cm.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

class BP_Frame(tk.Frame):
    def __init__(self, root, canvas_frame, **options):
        tk.Frame.__init__(self, root, **options)

        # Get ini options
        self.config = config = ConfigParser()
        config.read('datavis.ini')
        if config.has_section('general'):
            self.data_loc = config.get('general', 'dataset_location')
            self.data = pd.read_csv(self.data_loc, encoding='latin-1')
        else:
            self.data = sns.load_dataset('flights')
        self.data = self.data.dropna()

        # Lists for listboxes and option menus
        numeric_columns = self.data.select_dtypes(exclude=['object', 'category'])
        self.numeric_columns_list = list()
        for num_col in numeric_columns:
            self.numeric_columns_list.append(num_col)
        
        # Default graph options
        self.bp_x = tk.Variable(value='None') # column for x
        self.bp_y = tk.Variable(value='None') # column for y
        self.bp_hue = tk.Variable(value='None') # which column determines hue?
        self.bp_ci = tk.Variable(value='None') # show confidence intervals?

        # Load graph options from ini, if they don't exist create them and set to default values
        try:
            self.bp_x = tk.Variable(value=config.get('bar', 'x'))
            self.bp_y = tk.Variable(value=config.get('bar', 'y'))
            self.bp_hue = tk.Variable(value=config.get('bar', 'hue'))
            self.bp_ci = tk.Variable(value=config.get('bar', 'ci'))
        except:
            if not config.has_section('bar'):
                config.add_section('bar')
            config.set('bar', 'x', self.bp_x.get())
            config.set('bar', 'y', self.bp_y.get())
            config.set('bar', 'hue', self.bp_hue.get())
            config.set('bar', 'ci', self.bp_ci.get())
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

        # General frame settings
        pad_size = 50
        listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        # BP X CONTROL FRAME
        x_frame = tk.Frame(self)
        x_frame.grid(row=0, column=1, padx=pad_size)

        x_label = tk.Label(x_frame, text='Column to use for x:')
        x_label.pack()

        def x_update(self, event):
            lbTup = event.widget.curselection()
            for tup in lbTup:
                print (tup, type(tup))
                self.bp_x = tk.Variable(value=self.numeric_columns_list[tup])
        
        x_listbox = tk.Listbox(x_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        x_listbox.bind('<<ListboxSelect>>', lambda x: x_update(self, x))
        for column in self.numeric_columns_list:
            x_listbox.insert(tk.END, column)
        x_listbox.config(height=listbox_height)
        x_listbox.pack(side=tk.LEFT)

        x_scrollbar = tk.Scrollbar(x_frame)
        x_listbox.config(yscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=x_listbox.yview)
        x_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # BP Y CONTROL FRAME
        y_frame = tk.Frame(self)
        y_frame.grid(row=0, column=2, padx=pad_size)

        y_label = tk.Label(y_frame, text='Column to use for y:')
        y_label.pack()

        def y_update(self, event):
            lbTup = event.widget.curselection()
            for tup in lbTup:
                print (tup, type(tup))
                self.bp_y = tk.Variable(value=self.numeric_columns_list[tup])

        y_listbox = tk.Listbox(y_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        y_listbox.bind('<<ListboxSelect>>', lambda x: y_update(self, x))
        for column in self.numeric_columns_list:
            y_listbox.insert(tk.END, column)
        y_listbox.config(height=listbox_height)
        y_listbox.pack(side=tk.LEFT)

        y_scrollbar = tk.Scrollbar(y_frame)
        y_listbox.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=y_listbox.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # BP HUE CONTROL FRAME
        hue_frame = tk.Frame(self)
        hue_frame.grid(row=0, column=3, padx=pad_size)
        hue_label = tk.Label(hue_frame, text='Column to use for hue:')
        hue_label.pack()

        def hue_update(self, event):
            if self.bp_x.get() == '' or self.bp_x.get() == 'None' or self.bp_y.get() == '' or self.bp_y.get() == 'None':
                pass
            else:
                lbTup = event.widget.curselection()
                for tup in lbTup:
                    self.bp_hue = tk.Variable(value=self.numeric_columns_list[tup])
        
        # AT SOME POINT SET THIS LBOX UP TO BE DISABLED UNTIL AN X AND Y ARE CHOSEN
        hue_listbox = tk.Listbox(hue_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        hue_listbox.bind('<<ListboxSelect>>', lambda x: hue_update(self, x))
        for column in self.numeric_columns_list:
            hue_listbox.insert(tk.END, column)
        hue_listbox.config(height=listbox_height)
        hue_listbox.pack(side=tk.LEFT)

        hue_scrollbar = tk.Scrollbar(hue_frame)
        hue_listbox.config(yscrollcommand=hue_scrollbar.set)
        hue_scrollbar.config(command=hue_listbox.yview)
        hue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # BP CI CONTROL FRAME
        ci_frame = tk.Frame(self)
        ci_frame.grid(row=0, column=4, padx=pad_size)

        ci_label = tk.Label(ci_frame, text='Confidence interval:')
        ci_label.pack()

        def update_text():
            text = str(self.bp_ci.get())
            if text == 'sd':
                text = 'Standard Dev.'
            ci_checkbox.config(text=text)
        ci_checkbox = tk.Checkbutton(ci_frame, variable=self.bp_ci, onvalue='sd',
                                  offvalue='None', command=update_text, relief=tk.RAISED)
        ci_checkbox.pack()
        update_text()

        # BP BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=5, padx=pad_size)

        preview_button = tk.Button(
            button_frame, text='Preview Settings', command= lambda: self.preview_on_select(canvas_frame))
        preview_button.pack()

        apply_button = tk.Button(
            button_frame, text='Apply Settings', command=lambda: self.apply_on_select(canvas_frame))
        apply_button.pack()

    def preview_on_select(self, canvas_frame):
        preview_x = self.bp_x.get()
        if preview_x == '' or preview_x == 'None':
            preview_x = None
        preview_y = self.bp_y.get()
        if preview_y == '' or preview_y == 'None':
            preview_y = None
        preview_hue = self.bp_hue.get()
        if preview_hue == '' or preview_hue == 'None':
            preview_hue = None
        preview_ci = self.bp_ci.get()
        if preview_ci == '95':
            preview_ci = 95
        elif preview_ci == 'None':
            preview_ci = None

        print('--BP ON PREVIEW--')
        print('X: ', preview_x, type(preview_x))
        print('Y: ', preview_y, type(preview_y))
        print('Hue: ', preview_hue, type(preview_hue))
        print('Ci: ', preview_ci, type(preview_ci))

        plt.clf()
        bp = sns.barplot(data=self.data, x=preview_x, y=preview_y, hue=preview_hue, ci=preview_ci)
        plt.xticks(rotation=45)
        bp.figure.savefig('bp.png', bbox_inches='tight')
        """
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('bp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
        """
        file = 'bp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

    def apply_on_select(self, canvas_frame):
        config = self.config

        apply_x = self.bp_x.get()
        config.set('bar', 'x', apply_x)
        if apply_x == '' or apply_x == 'None':
            apply_x = None

        apply_y = self.bp_y.get()
        config.set('bar', 'y', apply_y)
        if apply_y == '' or apply_y == 'None':
            apply_y = None
        
        apply_hue = self.bp_hue.get()
        config.set('bar', 'hue', apply_hue)
        if apply_hue == '' or apply_hue == 'None':
            apply_hue = None
        
        apply_ci = self.bp_ci.get()
        config.set('bar', 'ci', apply_ci)
        if apply_ci == '95':
            apply_ci = 95
        elif apply_ci == 'None':
            apply_ci = None

        with open('datavis.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()

        print('--BP ON APPLY--')
        print('X: ', apply_x, type(apply_x))
        print('Y: ', apply_y, type(apply_y))
        print('Hue: ', apply_hue, type(apply_hue))
        print('Ci: ', apply_ci, type(apply_ci))

        plt.clf()
        bp = sns.barplot(data=self.data, x=apply_x, y=apply_y, hue=apply_hue, ci=apply_ci)
        plt.xticks(rotation=45)
        bp.figure.savefig('bp.png', bbox_inches='tight')
        """
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('bp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
        """
        file = 'bp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

class SP_Frame(tk.Frame):
    def __init__(self, root, canvas_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        # Get ini options
        self.config  = config = ConfigParser()
        config.read('datavis.ini')
        if config.has_section('general'):
            data_loc = config.get('general', 'dataset_location')
            self.data = pd.read_csv(data_loc, encoding='latin-1')
        else:
            self.data = sns.load_dataset('tips')
        self.data = self.data.dropna()
        
        # Lists for listboxes and option menus
        columns = self.data.columns
        numeric_columns = self.data.select_dtypes(exclude=['object', 'category'])
        self.columns_list = list()
        self.numeric_columns_list = list()
        self.columns_list.append('None') # so hue coloring can be set to off
        for col in columns:
            self.columns_list.append(col)
        for num_col in numeric_columns:
            self.numeric_columns_list.append(num_col)

        # Default graph options
        self.sp_x = tk.Variable(value=numeric_columns.columns[0]) # x var
        self.sp_y = tk.Variable(value=numeric_columns.columns[1]) # y var
        self.sp_hue = tk.Variable(value='None') # which column determines hue?
        self.sp_legend = tk.BooleanVar(value='True') # display legend?
        self.sp_scatter = tk.BooleanVar(value='True') # draw scatter?
        self.sp_fit_reg = tk.BooleanVar(value='True') # fit linear regression line?

        # Load graph options from ini, if they don't exist create them and set to default values
        try:
            self.sp_x = tk.Variable(value=config.get('scatter', 'x'))
            self.sp_y = tk.Variable(value=config.get('scatter', 'y'))
            self.sp_hue = tk.Variable(value=config.get('scatter', 'hue'))
            self.sp_legend = tk.BooleanVar(value=config.getboolean('scatter', 'legend'))
            self.sp_scatter = tk.BooleanVar(value=config.getboolean('scatter', 'scatter'))
            self.sp_fit_reg = tk.BooleanVar(value=config.getboolean('scatter', 'fit_reg'))
        except:
            if not config.has_section('scatter'):
                config.add_section('scatter')
                config.set('scatter', 'x', self.sp_x.get())
                config.set('scatter', 'y', self.sp_y.get())
                config.set('scatter', 'hue', self.sp_hue.get())
                config.set('scatter', 'legend', str(self.sp_legend.get()))
                config.set('scatter', 'scatter', str(self.sp_scatter.get()))
                config.set('scatter', 'fit_reg', str(self.sp_fit_reg.get()))
                with open('datavis.ini', 'w') as configfile:
                    config.write(configfile)
                configfile.close()
        
        # General frame settings
        pad_size = 50
        listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(8, weight=1)

        # SP X CONTROL FRAME
        x_frame = tk.Frame(self)
        x_frame.grid(row=0, column=1, padx=pad_size)

        x_label = tk.Label(x_frame, text='Column to use for x:')
        x_label.pack()

        def x_update(self, event):
            x = event.widget.curselection()
            if x:
                self.sp_x = tk.Variable(value=self.numeric_columns_list[x[0]])
        
        x_listbox = tk.Listbox(x_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        x_listbox.bind('<<ListboxSelect>>', lambda x: x_update(self, x))
        for column in self.numeric_columns_list:
            x_listbox.insert(tk.END, column)
        x_listbox.config(height=listbox_height)
        x_listbox.pack(side=tk.LEFT)

        x_scrollbar = tk.Scrollbar(x_frame)
        x_listbox.config(yscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=x_listbox.yview)
        x_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # SP Y CONTROL FRAME
        y_frame = tk.Frame(self)
        y_frame.grid(row=0, column=2, padx=pad_size)

        y_label = tk.Label(y_frame, text='Column to use for y:')
        y_label.pack()

        def y_update(self, event):
            y = event.widget.curselection()
            if y:
                self.sp_y = tk.Variable(value=self.numeric_columns_list[y[0]])
        
        y_listbox = tk.Listbox(y_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        y_listbox.bind('<<ListboxSelect>>', lambda x: y_update(self, x))
        for column in self.numeric_columns_list:
            y_listbox.insert(tk.END, column)
        y_listbox.config(height=listbox_height)
        y_listbox.pack(side=tk.LEFT)

        y_scrollbar = tk.Scrollbar(y_frame)
        y_listbox.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=y_listbox.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # SP HUE CONTROL FRAME
        hue_frame = tk.Frame(self)
        hue_frame.grid(row=0, column=3, padx=pad_size)

        hue_label = tk.Label(hue_frame, text='Column that determines hue:')
        hue_label.pack()

        hue_option = tk.OptionMenu(hue_frame, self.sp_hue, *self.columns_list)
        hue_option.pack()

        # SP LEGEND CONTROL FRAME
        legend_frame = tk.Frame(self)
        legend_frame.grid(row=0, column=4, padx=pad_size)

        legend_label = tk.Label(legend_frame, text='Show legend:')
        legend_label.pack()

        def update_legend_check():
            legend_checkbox.config(text=str(self.sp_legend.get()))
        legend_checkbox = tk.Checkbutton(legend_frame, variable=self.sp_legend, onvalue='True', offvalue='False', command=update_legend_check, relief=tk.RAISED)
        legend_checkbox.pack()
        update_legend_check()

        # SP SCATTER CONTROL FRAME
        scatter_frame = tk.Frame(self)
        scatter_frame.grid(row=0, column=5, padx=pad_size)

        scatter_label = tk.Label(scatter_frame, text='Scatter:')
        scatter_label.pack()

        def update_scatter_check():
            scatter_checkbox.config(text=str(self.sp_scatter.get()))
        scatter_checkbox = tk.Checkbutton(scatter_frame, variable=self.sp_scatter, onvalue='True', offvalue='False', command=update_scatter_check, relief=tk.RAISED)
        scatter_checkbox.pack()
        update_scatter_check()

        # SP FIT REG CONTROL FRAME
        fit_reg_frame = tk.Frame(self)
        fit_reg_frame.grid(row=0, column=6, padx=pad_size)

        fit_reg_label = tk.Label(fit_reg_frame, text='Fit regression line:')
        fit_reg_label.pack()

        def update_fit_reg_check():
            fit_reg_checkbox.config(text=str(self.sp_fit_reg.get()))
        fit_reg_checkbox = tk.Checkbutton(fit_reg_frame, variable=self.sp_fit_reg, onvalue='True', offvalue='False', command=update_fit_reg_check, relief=tk.RAISED)
        fit_reg_checkbox.pack()
        update_fit_reg_check()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=7, padx=pad_size)

        preview_button = tk.Button(
            button_frame, text='Preview Settings', command=lambda: self.preview_on_select(canvas_frame))
        preview_button.pack()

        apply_button = tk.Button(
            button_frame, text='Apply Settings', command=lambda: self.apply_on_select(canvas_frame))
        apply_button.pack()

    def preview_on_select(self, canvas_frame):
        preview_x = self.sp_x.get()
        preview_y = self.sp_y.get()
        preview_hue = self.sp_hue.get()
        if preview_hue == 'None':
            preview_hue = None
        preview_legend = self.sp_legend.get()
        preview_scatter = self.sp_scatter.get()
        preview_fit_reg = self.sp_fit_reg.get()

        print('--SP ON PREVIEW--')
        print('X: ', preview_x, type(preview_x))
        print('Y: ', preview_y, type(preview_y))
        print('Hue: ', preview_hue, type(preview_hue))
        print('Legend: ', preview_legend, type(preview_legend))
        print('Scatter: ', preview_scatter, type(preview_scatter))
        print('Fit Reg: ', preview_fit_reg, type(preview_fit_reg))

        plt.clf()
        sp = sns.lmplot(data=self.data, x=preview_x, y=preview_y, hue=preview_hue, legend=preview_legend, scatter=preview_scatter, fit_reg=preview_fit_reg)
        sp.savefig('sp.png')
        file = 'sp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()

    def apply_on_select(self, canvas_frame):
        config = self.config

        apply_x = self.sp_x.get()
        config.set('scatter', 'x', apply_x)
        
        apply_y = self.sp_y.get()
        config.set('scatter', 'y', apply_y)
        
        apply_hue = self.sp_hue.get()
        config.set('scatter', 'hue', apply_hue)
        if apply_hue == 'None':
            apply_hue = None
        
        apply_scatter = self.sp_scatter.get()
        config.set('scatter', 'scatter', str(apply_scatter))

        apply_legend = self.sp_legend.get()
        config.set('scatter', 'legend', str(apply_legend))

        apply_fit_reg = self.sp_fit_reg.get()
        config.set('scatter', 'fit_reg', str(apply_fit_reg))
        
        with open('datavis.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()

        print('--SP ON APPLY--')
        print('X: ', apply_x, type(apply_x))
        print('Y: ', apply_y, type(apply_y))
        print('Hue: ', apply_hue, type(apply_hue))
        print('Legend: ', apply_legend, type(apply_legend))
        print('Scatter: ', apply_scatter, type(apply_scatter))
        print('Fit Reg: ', apply_fit_reg, type(apply_fit_reg))

        plt.clf()
        sp = sns.lmplot(data=self.data, x=apply_x, y=apply_y, hue=apply_hue, legend=apply_legend, scatter=apply_scatter, fit_reg=apply_fit_reg)
        sp.savefig('sp.png')
        file = 'sp.png'
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
        canvas.grid()
