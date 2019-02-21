import tkinter as tk
from configparser import ConfigParser

import matplotlib.image as mpimg
import pandas as pd
import seaborn as sns

class PP_Frame(tk.Frame):
    def __init__(self, root, figure, EDA_Canvas, **options):
        
        tk.Frame.__init__(self, root, **options)

        # Get ini options
        self.config = config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        # Lists for listboxes and option menus
        columns = self.data.columns
        numeric_columns = self.data.select_dtypes(exclude=['object'])
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

        hue_option = tk.OptionMenu(hue_frame, self.pp_hue, *self.columns_list)
        hue_option.pack()

        # PP VARS CONTROL FRAME
        vars_frame = tk.Frame(self)
        vars_frame.grid(row=0, column=1, padx=pad_size)
        vars_label = tk.Label(vars_frame, text='Columns to use in plot:')
        vars_label.pack()

        def vars_update(self, event):
            lbTup = event.widget.curselection()
            tmp = list()
            for tup in lbTup:
                tmp.append(self.numeric_columns_list[tup])
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

        # PP BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=5, padx=pad_size)

        preview_button = tk.Button(
            button_frame, text='Preview Settings', command=lambda: self.preview_on_select(figure, EDA_Canvas))
        preview_button.pack()

        apply_button = tk.Button(
            button_frame, text='Apply Settings', command=lambda: self.apply_on_select(figure, EDA_Canvas))
        apply_button.pack()

    def preview_on_select(self, fig, canvas):
        preview_hue = self.pp_hue.get()
        if preview_hue == 'None':
            preview_hue = None
        preview_vars = self.pp_vars
        if not all(preview_vars) or preview_vars == ():
            preview_vars = None
        preview_kind = self.pp_kind.get()
        preview_diag_kind = self.pp_diag_kind.get()

        print('--PP ON PREVIEW--')
        print('Hue: ', preview_hue, type(preview_hue))
        print('Vars: ', preview_vars, type(preview_vars))
        print('kind: ', preview_kind, type(preview_kind))
        print('Diag Kind: ', preview_diag_kind, type(preview_diag_kind))

        pp = sns.pairplot(data=self.data, hue=preview_hue, vars=preview_vars, kind=preview_kind, diag_kind=preview_diag_kind)
        pp.savefig('pp.png')
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()

    def apply_on_select(self, fig, canvas):
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
        print('Hue: ', apply_hue, type(apply_hue))
        print('Vars: ', apply_vars, type(apply_vars))
        print('Kind: ', apply_kind, type(apply_kind))
        print('Diag Kind: ', apply_diag_kind, type(apply_diag_kind))

        pp = sns.pairplot(data=self.data, hue=apply_hue, vars=apply_vars, kind=apply_kind, diag_kind=apply_diag_kind)
        pp.savefig('pp.png')
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('pp.png')
        a.imshow(img_arr)
        a.axis('off')
        canvas.draw()
