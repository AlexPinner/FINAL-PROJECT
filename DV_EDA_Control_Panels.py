import tkinter as tk
from configparser import ConfigParser

import matplotlib.image as mpimg
import pandas as pd
import seaborn as sns


class PP_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        
        tk.Frame.__init__(self, root, **options)

        self.config = ConfigParser()
        self.config.read('datavis.ini')
        self.data_loc = self.config.get('general', 'dataset_location')
        self.data = pd.read_csv(self.data_loc, encoding='latin-1')

        # need column list for the optionMenu for pp hue and vars
        self.columns = self.data.columns
        self.numeric_columns = self.data.select_dtypes(exclude=['object'])
        self.columns_list = list()
        self.numeric_columns_list = list()

        for column in self.columns:
            self.columns_list.append(column)

        for num_column in self.numeric_columns:
            self.numeric_columns_list.append(num_column)

        # set pairplot settings to defaults
        # which column determines color of points
        self.pp_hue = tk.Variable(value='None')
        # which columns to use in plot
        self.pp_vars = None
        # fit regression line?
        self.pp_kind = tk.Variable(value='scatter')
        # which graphs to use along diagonal
        self.pp_diag_kind = tk.Variable(value='hist')
        self.diag_kind_list = list(['auto', 'hist', 'kde'])

        # set pp settings to previous user settings if applicable
        if self.config.has_section('pairplot'):
            if self.config.has_option('pairplot', 'hue'):
                self.pp_hue = tk.Variable(value=self.config.get('pairplot', 'hue'))
            if self.config.has_option('pairplot', 'vars'):
                self.pp_vars = self.config.get('pairplot', 'vars').split(',')
                if self.pp_vars == 'None' or self.pp_vars == ['']:
                    self.pp_vars = None
            if self.config.has_option('pairplot', 'kind'):
                self.pp_kind = tk.Variable(value=self.config.get('pairplot', 'kind'))
            if self.config.has_option('pairplot', 'diag_kind'):
                self.pp_diag_kind = tk.Variable(
                    value=self.config.get('pairplot', 'diag_kind'))

        self.pad_size = 50
        self.listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        # vars control
        self.vars_frame = tk.Frame(self)
        self.vars_frame.grid(row=0, column=1, padx=self.pad_size)

        self.vars_label = tk.Label(self.vars_frame, text='Columns to use in plot:')
        self.vars_label.pack()

        self.vars_listbox = tk.Listbox(self.vars_frame, selectmode=tk.MULTIPLE, justify=tk.CENTER)

        for num_column in self.numeric_columns_list:
            self.vars_listbox.insert(tk.END, num_column)

        if not self.pp_vars == None:
            for var in self.pp_vars:
                i = self.vars_listbox.get(0, tk.END).index(var)
                print(i)
                self.vars_listbox.select_set(i)
        # vars_listbox.select_set(0, END)  # all columns selected by default
        # update this select_set to go off of which vars from the column list are on
        # based on whats in the ini (pp_vars) instead of just selecting all
        self.vars_listbox.config(height=self.listbox_height)
        self.vars_listbox.pack(side=tk.LEFT)

        self.vars_scrollbar = tk.Scrollbar(self.vars_frame)
        self.vars_listbox.config(yscrollcommand=self.vars_scrollbar.set)
        self.vars_scrollbar.config(command=self.vars_listbox.yview)
        self.vars_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # hue control
        self.hue_frame = tk.Frame(self)
        self.hue_frame.grid(row=0, column=2, padx=self.pad_size)

        self.hue_label = tk.Label(self.hue_frame, text='Column that determines hue:')
        self.hue_label.pack()

        self.hue_option = tk.OptionMenu(self.hue_frame, self.pp_hue, 'None', *self.columns_list)
        self.hue_option.pack()

        # kind control
        self.kind_frame = tk.Frame(self)
        self.kind_frame.grid(row=0, column=3, padx=self.pad_size)

        self.kind_label = tk.Label(self.kind_frame, text='Fit regression line:')
        self.kind_label.pack()

        def update_text():
            self.kind_checkbox.config(text=str(self.pp_kind.get()))
        self.kind_checkbox = tk.Checkbutton(self.kind_frame, variable=self.pp_kind, onvalue='reg',
                                    offvalue='scatter', command=update_text, relief=tk.RAISED)
        self.kind_checkbox.pack()
        update_text()

        # diag kind control
        self.diag_kind_frame = tk.Frame(self)
        self.diag_kind_frame.grid(row=0, column=4, padx=self.pad_size)

        self.diag_kind_label = tk.Label(
            self.diag_kind_frame, text='Graph type along diagonal:')
        self.diag_kind_label.pack()

        self.diag_kind_option = tk.OptionMenu(
            self.diag_kind_frame, self.pp_diag_kind, *self.diag_kind_list)
        self.diag_kind_option.pack()

        # button controls
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=5, padx=self.pad_size)

        self.preview_button = tk.Button(
            self.button_frame, text='Preview Settings', command=lambda: self.preview_on_select(figure, EDA_Canvas))
        self.preview_button.pack()

        self.apply_button = tk.Button(
            self.button_frame, text='Apply Settings', command=lambda: self.apply_on_select(figure, EDA_Canvas))
        self.apply_button.pack()

    def preview_on_select(self, fig, canvas):
        self.preview_hue = self.pp_hue.get()
        if self.preview_hue == 'None':
            self.preview_hue = None
        self.items = self.vars_listbox.curselection()
        self.preview_vars = [self.numeric_columns_list[int(item)] for item in self.items]
        if self.preview_vars == []:
            self.preview_vars = None
        self.preview_kind = self.pp_kind.get()
        self.preview_diag_kind = self.pp_diag_kind.get()

        print('PP ON PREVIEW:')
        print('Hue: ', self.preview_hue)
        print('Vars: ', self.preview_vars)
        print('kind: ', self.preview_kind)
        print('Diag Kind: ', self.preview_diag_kind)
        self.pp = sns.pairplot(data=self.data, hue=self.preview_hue, vars=self.preview_vars, kind=self.preview_kind, diag_kind=self.preview_diag_kind)
        self.pp.savefig('pp.png')
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
        # may have to make graph drawing a seperate function at some point since graphs will be drawn by listbox on select using ini settings, or here without using the ini settings
        # the apply on select may as well select a listbox index just to recall the listbox on select graph redraw since it just updated the ini that will be used by the listbox redrawing
        # but for this preview it will be based on the current settings and not ini
        # could also just leave it as is and avoid complex function nonsense

    def apply_on_select(self, fig, canvas):
        if not self.config.has_section('pairplot'):
            self.config.add_section('pairplot')

        self.apply_hue = self.pp_hue.get()
        self.config.set('pairplot', 'hue', self.apply_hue)
        if self.apply_hue == 'None':
            self.apply_hue = None

        self.items = self.vars_listbox.curselection()
        self.apply_vars = [self.numeric_columns_list[int(item)] for item in self.items]
        self.config.set('pairplot', 'vars', ','.join(self.apply_vars))
        # ','.join(map(str, myList)) this does the same thing but for lists of ints
        if self.apply_vars == []:
            self.apply_vars = None

        self.apply_kind = self.pp_kind.get()
        self.config.set('pairplot', 'kind', self.apply_kind)

        self.apply_diag_kind = self.pp_diag_kind.get()
        self.config.set('pairplot', 'diag_kind', self.apply_diag_kind)

        with open('datavis.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

        print('PP ON APPLY:')
        print('Hue: ', self.apply_hue)
        print('Vars: ', self.apply_vars)
        print('Kind: ', self.apply_kind)
        print('Diag Kind: ', self.apply_diag_kind)
        self.pp = sns.pairplot(data=self.data, hue=self.apply_hue, vars=self.apply_vars, kind=self.apply_kind, diag_kind=self.apply_diag_kind)
        self.pp.savefig('pp.png')
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()

class CM_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        
        tk.Frame.__init__(self, root, **options)

        self.config = ConfigParser()
        self.config.read('datavis.ini')
        self.data_loc = self.config.get('general', 'dataset_location')
        self.data = pd.read_csv(self.data_loc, encoding='latin-1')

        # set correlation matrix settings to defaults
        # print numbers in cells?
        self.cm_annot = tk.Variable(value='False')
        # show color bar?
        self.cm_cbar = tk.Variable(value='True')
        # make cells square?
        self.cm_square = tk.Variable(value='False')

        # set cm settings to previous user settings if applicable
        if self.config.has_section('correlation'):
            if self.config.has_option('correlation', 'annot'):
                self.cm_annot = tk.Variable(value=self.config.get('correlation', 'annot'))
            if self.config.has_option('correlation', 'cbar'):
                self.cm_cbar = tk.Variable(value=self.config.get('correlation', 'cbar'))
            if self.config.has_option('correlation', 'kind'):
                self.cm_square = tk.Variable(value=self.config.get('correlation', 'kind'))

        self.pad_size = 50
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        # annot control
        self.annot_frame = tk.Frame(self)
        self.annot_frame.grid(row=0, column=1, padx=self.pad_size)

        self.annot_label = tk.Label(self.annot_frame, text='Show numbers in cells:')
        self.annot_label.pack()

        def update_annot_check():
            self.annot_checkbox.config(text=str(self.cm_annot.get()))
        self.annot_checkbox = tk.Checkbutton(self.annot_frame, variable=self.cm_annot, onvalue='True', offvalue='False', command=update_annot_check, relief=tk.RAISED)
        self.annot_checkbox.pack()
        update_annot_check()

        # cbar control
        self.cbar_frame = tk.Frame(self)
        self.cbar_frame.grid(row=0, column=2, padx=self.pad_size)

        self.cbar_label = tk.Label(self.cbar_frame, text='Show color bar:')
        self.cbar_label.pack()

        def update_cbar_check():
            self.cbar_checkbox.config(text=str(self.cm_cbar.get()))
        self.cbar_checkbox = tk.Checkbutton(self.cbar_frame, variable=self.cm_cbar, onvalue='True', offvalue='False', command=update_cbar_check, relief=tk.RAISED)
        self.cbar_checkbox.pack()
        update_cbar_check()

        # square control
        self.square_frame = tk.Frame(self)
        self.square_frame.grid(row=0, column=3, padx=self.pad_size)

        self.square_label = tk.Label(self.square_frame, text='Make cells square:')
        self.square_label.pack()

        def update_square_check():
            self.square_checkbox.config(text=str(self.cm_square.get()))
        self.square_checkbox = tk.Checkbutton(
            self.square_frame, variable=self.cm_square, onvalue='True', offvalue='False', command=update_square_check, relief=tk.RAISED)
        self.square_checkbox.pack()
        update_square_check()

        # button controls
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=4, padx=self.pad_size)

        self.preview_button = tk.Button(
            self.button_frame, text='Preview Settings', command=lambda: self.preview_on_select(figure, EDA_Canvas))
        self.preview_button.pack()

        self.apply_button = tk.Button(
            self.button_frame, text='Apply Settings', command=lambda: self.apply_on_select(figure, EDA_Canvas))
        self.apply_button.pack()

    def preview_on_select(self, fig, canvas):
        self.preview_annot = self.cm_annot
        self.preview_cbar = self.cm_cbar
        self.preview_square = self.cm_square

        print('CM ON PREVIEW:')
        print('Annot: ', self.preview_annot)
        print('Cbar: ', self.preview_cbar)
        print('Square: ', self.preview_square)
        fig.clear()
        a = fig.add_subplot(111)
        sns.heatmap(data=self.data, annot=self.preview_annot, cbar=self.preview_cbar, square=self.preview_square, ax=a)
        canvas.draw()

    def apply_on_select(self, fig, canvas):
        if not self.config.has_section('correlation'):
            self.config.add_section('correlation')

        self.apply_annot = self.cm_annot
        self.config.set('correlation', 'annot', self.apply_annot)

        self.apply_cbar = self.cm_cbar
        self.config.set('correlation', 'cbar', self.apply_cbar)

        self.apply_square = self.cm_square
        self.config.set('correlation', 'square', self.apply_square)

        with open('datavis.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

        print('CM ON APPLY:')
        print('Annot: ', self.apply_annot)
        print('Cbar: ', self.apply_cbar)
        print('Sqaure: ', self.apply_square)
        fig.clear()
        a = fig.add_subplot(111)
        sns.heatmap(data=self.data, annot=self.apply_annot, cbar=self.apply_cbar, square=self.apply_square, ax=a)
        canvas.draw()

class BP_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        tk.Frame.__init__(self, root, **options)

        self.config = ConfigParser()
        self.config.read('datavis.ini')
        self.data_loc = self.config.get('general', 'dataset_location')
        self.data = pd.read_csv(self.data_loc, encoding='latin-1')

        self.columns = self.data.columns
        self.numeric_columns = self.data.select_dtypes(exclude=['object'])
        self.columns_list = list()
        self.numeric_columns_list = list()

        for column in self.columns:
            self.columns_list.append(column)

        for column in self.numeric_columns:
            self.numeric_columns_list.append(column)

        # set barplot settings to defaults
        # column for x
        self.bp_x = None
        # column for y
        self.bp_y = None
        # which column determines hue?
        self.bp_hue = None
        # show confidence intervals?
        self.bp_ci = tk.Variable(value='None')

        # set bp settings to previous user settings if applicable
        if self.config.has_section('bar'):
            if self.config.has_option('bar', 'x'):
                self.bp_x = self.config.get('bar', 'x').split(',')
                if self.bp_x == 'None' or self.bp_x == ['']:
                    self.bp_x = None
            if self.config.has_option('bar', 'y'):
                self.bp_y = self.config.get('bar', 'y').split(',')
                if self.bp_y == 'None' or self.bp_y == ['']:
                    self.bp_y = None
            if self.config.has_option('bar', 'hue'):
                self.bp_hue = self.config.get('bar', 'hue').split(',')
                if self.bp_hue == 'None' or self.bp_hue == ['']:
                    self.bp_hue = None
            if self.config.has_option('bar', 'ci'):
                self.bp_ci = tk.Variable(value=self.config.get('bar', 'ci'))
                if self.bp_ci == 'None':
                    self.bp_ci = None

        self.pad_size = 50
        self.listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        # x control
        self.x_frame = tk.Frame(self)
        self.x_frame.grid(row=0, column=1, padx=self.pad_size)

        self.x_label = tk.Label(self.x_frame, text='Column to use for x:')
        self.x_label.pack()

        self.x_listbox = tk.Listbox(self.x_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        for column in self.columns_list:
            self.x_listbox.insert(tk.END, column)
        self.x_listbox.config(height=self.listbox_height)
        self.x_listbox.pack(side=tk.LEFT)

        self.x_scrollbar = tk.Scrollbar(self.x_frame)
        self.x_listbox.config(yscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.config(command=self.x_listbox.yview)
        self.x_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # y control
        self.y_frame = tk.Frame(self)
        self.y_frame.grid(row=0, column=2, padx=self.pad_size)

        self.y_label = tk.Label(self.y_frame, text='Column to use for y:')
        self.y_label.pack()

        self.y_listbox = tk.Listbox(self.y_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        for column in self.numeric_columns_list:
            self.y_listbox.insert(tk.END, column)
        self.y_listbox.config(height=self.listbox_height)
        self.y_listbox.pack(side=tk.LEFT)

        self.y_scrollbar = tk.Scrollbar(self.y_frame)
        self.y_listbox.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.config(command=self.y_listbox.yview)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # hue control
        self.hue_frame = tk.Frame(self)
        self.hue_frame.grid(row=0, column=3, padx=self.pad_size)

        self.hue_label = tk.Label(self.hue_frame, text='Column to use for hue:')
        self.hue_label.pack()

        self.hue_listbox = tk.Listbox(self.hue_frame, selectmode=tk.SINGLE, justify=tk.CENTER)
        for column in self.columns_list:
            self.hue_listbox.insert(tk.END, column)
        self.hue_listbox.config(height=self.listbox_height)
        self.hue_listbox.pack(side=tk.LEFT)

        self.hue_scrollbar = tk.Scrollbar(self.hue_frame)
        self.hue_listbox.config(yscrollcommand=self.hue_scrollbar.set)
        self.hue_scrollbar.config(command=self.hue_listbox.yview)
        self.hue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # confidence interval control
        self.ci_frame = tk.Frame(self)
        self.ci_frame.grid(row=0, column=4, padx=self.pad_size)

        self.ci_label = tk.Label(self.ci_frame, text='Confidence interval:')
        self.ci_label.pack()

        def update_text():
            self.text = str(self.bp_ci.get())
            if self.text == 'sd':
                self.text = 'Standard Dev.'
            self.ci_checkbox.config(text=self.text)
        self.ci_checkbox = tk.Checkbutton(self.ci_frame, variable=self.bp_ci, onvalue='sd',
                                  offvalue='None', command=update_text, relief=tk.RAISED)
        self.ci_checkbox.pack()
        update_text()

        # button controls
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=5, padx=self.pad_size)

        self.preview_button = tk.Button(
            self.button_frame, text='Preview Settings', command=self.preview_on_select)
        self.preview_button.pack()

        self.apply_button = tk.Button(
            self.button_frame, text='Apply Settings', command=self.apply_on_select)
        self.apply_button.pack()

    def preview_on_select(self, fig, canvas):
            self.x_items = self.x_listbox.curselection()
            self.preview_x = [self.columns_list[int(x_item)] for x_item in self.x_items]
            if self.preview_x == []:
                self.preview_x = None
            
            self.y_items = self.y_listbox.curselection()
            self.preview_y = [self.numeric_columns_list[int(y_item)] for y_item in self.y_items]
            if self.preview_y == []:
                self.preview_y = None

            self.hue_items = self.hue_listbox.curselection()
            self.preview_hue = [self.numeric_columns_list[int(hue_item)] for hue_item in self.hue_items]
            if self.preview_hue == []:
                self.preview_hue = None
            
            self.preview_ci = self.bp_ci.get()
            if self.preview_ci == 'None':
                self.preview_ci = None

            print('BP ON PREVIEW:')
            print('X: ', self.preview_x)
            print('Y: ', self.preview_y)
            print('Hue: ', self.preview_hue)
            print('Ci: ', self.preview_ci)
            fig.clear()
            a = fig.add_subplot(111)
            sns.barplot(data=self.data, x=self.preview_x, y=self.preview_y,
                        hue=self.preview_hue, ci=self.preview_ci, ax=a)
            canvas.draw()

    def apply_on_select(self, fig, canvas):
        if not self.config.has_section('bar'):
            self.config.add_section('bar')

        self.x_items = self.x_listbox.curselection()
        self.apply_x = [self.columns_list[int(x_item)] for x_item in self.x_items]
        self.config.set('bar', 'x', ','.join(self.apply_x))
        if self.apply_x == []:
            self.apply_x = None

        self.y_items = self.y_listbox.curselection()
        self.apply_y = [self.numeric_columns_list[int(y_item)] for y_item in self.y_items]
        self.config.set('bar', 'y', ','.join(self.apply_y))
        if self.apply_y == []:
            self.apply_y = None

        self.hue_items = self.hue_listbox.curselection()
        self.apply_hue = [self.numeric_columns_list[int(hue_item)] for hue_item in self.hue_items]
        self.config.set('bar', 'hue', ','.join(self.apply_hue))
        if self.apply_hue == []:
            self.apply_hue = None

        self.apply_ci = self.bp_ci.get()
        if self.apply_ci == 'None':
            self.apply_ci = None
        self.config.set('bar', 'ci', self.apply_ci)

        with open('datavis.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

        print('BP ON APPLY:')
        print('X: ', self.apply_x)
        print('Y: ', self.apply_y)
        print('Hue: ', self.apply_hue)
        print('Ci: ', self.apply_ci)
        fig.clear()
        a = fig.add_subplot(111)
        sns.barplot(data=self.data, x=self.apply_x, y=self.apply_y, hue=self.apply_hue, ci=self.apply_ci, ax=a)
        canvas.draw()

class SP_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        tk.Frame.__init__(self, root, **options)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.frame = frame = tk.Frame(self)
        frame.grid(row=0, column=1)
        self.label = label =tk.Label(frame, text='SCATTER PLOT CONTROLS')
        label.grid()
        self.notification = notification =tk.Label(frame, text='Under Construction')
        notification.grid()


class PCA_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        tk.Frame.__init__(self, root, **options)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.frame = frame = tk.Frame(self)
        frame.grid(row=0, column=1)
        self.label = label =tk.Label(frame, text='PCA CONTROLS')
        label.grid()
        self.notification = notification =tk.Label(frame, text='Under Construction')
        notification.grid()
