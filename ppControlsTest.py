import tkinter as tk
from configparser import ConfigParser

import matplotlib.image as mpimg
import pandas as pd
import seaborn as sns

class PP_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        
        tk.Frame.__init__(self, root, **options)

        self.config = config = ConfigParser()
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
        pp_hue = tk.Variable(value=None)
        pp_vars = tk.Variable(value=None)
        pp_kind = tk.Variable(value='scatter')
        pp_diag_kind = tk.Variable(value='auto')
        self.diag_kind_list = list(['auto', 'hist', 'kde'])

        # set pp settings to previous user settings if applicable
        try:
            self.pp_hue = pp_hue = tk.Variable(value=config.get('pairplot', 'hue'))  # which column determines color of points
            self.pp_vars = pp_vars = tk.Variable(value=config.get('pairplot', 'vars').split(','))  # which columns to use in plot
            self.pp_kind = pp_kind = tk.Variable(value=config.get('pairplot', 'kind'))  # fit regression line?
            self.pp_diag_kind = pp_diag_kind = tk.Variable(value=config.get('pairplot', 'diag_kind'))  # graph type to use along diagonal
        except:
            if not config.has_section('pairplot'):
                config.add_section('pairplot')
            config.set('pairplot', 'hue', str(pp_hue.get()))
            config.set('pairplot', 'vars', str(pp_vars.get()))
            config.set('pairplot', 'kind', str(pp_kind.get()))
            config.set('pairplot', 'diag_kind', str(pp_diag_kind.get()))
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

        self.pad_size = 50
        self.listbox_height = 4
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        # vars control
        self.vars_frame = tk.Frame(self)
        self.vars_frame.grid(row=0, column=1, padx=self.pad_size)
        self.vars_label = tk.Label(self.vars_frame, text='Columns to use in plot:')
        self.vars_label.pack()

        def vars_update(self, event):
            print(event)
            w = event.widget
            print(w.curselection())
            #for var in w.curselection().items:
            #    print(var)
                
        self.vars_listbox = tk.Listbox(self.vars_frame, selectmode=tk.MULTIPLE, justify=tk.CENTER)
        self.vars_listbox.bind('<<ListboxSelect>>', lambda x: vars_update(self, x))
        for num_column in self.numeric_columns_list:
            self.vars_listbox.insert(tk.END, num_column)

        if not self.pp_vars.get() == None or self.pp_vars.get() == 'None' or self.pp_vars.get() == '':
            for var in self.pp_vars.get():
                i = self.vars_listbox.get(0, tk.END).index(var)
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