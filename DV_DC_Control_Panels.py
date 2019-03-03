import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import Imputer

import DV_DC_Table

pad_size = 50

class Find_Replace_Frame(tk.Frame):
    def __init__(self, root, table_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # FIND CONTROL FRAME
        find_frame = tk.Frame(self)
        find_frame.grid(row=0, column=1, padx=pad_size)

        find_label = tk.Label(find_frame, text='Type or select what to find:')
        find_label.pack()

        self.find_variable = tk.Variable()
        find_values = (0, np.nan)
        find_combo = ttk.Combobox(find_frame, values=find_values, textvariable=self.find_variable)
        find_combo.pack()

        # REPLACE CONTROL FRAME
        replace_frame = tk.Frame(self)
        replace_frame.grid(row=0, column=2, padx=pad_size)

        replace_label = tk.Label(replace_frame, text='Type or select the method of replacement:')
        replace_label.pack()

        self.replace_variable = tk.Variable()
        replace_values = ('Imputer()', 'DropNa()')
        replace_combo = ttk.Combobox(replace_frame, values=replace_values, textvariable=self.replace_variable)
        replace_combo.pack()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=3, padx=pad_size)

        find_replace_btn = tk.Button(
            button_frame, text='Find and Replace', command=lambda: self.find_and_replace(table_frame))
        find_replace_btn.pack()

        save_df_btn = tk.Button(
            button_frame, text='Save Dataframe Changes', command=lambda: self.save_dataframe())
        save_df_btn.pack()

    def find_and_replace(self, table_frame):
        self.data = self.data.replace(to_replace='?', value=np.nan)
        for column in self.data.select_dtypes(exclude=['int64', 'float64']):
            try:
                self.data[column] = self.data[column].astype('float64')
            except:
                pass
        
        find_val = self.find_variable.get()
        if find_val == '0':
            find_val = 0
        elif find_val == 'NaN':
            find_val = np.nan
        
        replace_val = self.replace_variable.get()

        if replace_val == 'Imputer()':
            #fill_NaN = Imputer(missing_values=find_val, strategy='mean', axis=0)
            #self.data = pd.DataFrame(fill_NaN.fit_transform(self.data))
            #self.data.columns = self.data.columns
            #self.data.index = self.data.index
            for column in self.data.select_dtypes(exclude=['object','category']):
                mean = self.data[column].mean()
                mean = round(mean, 0)
                self.data[column] = self.data[column].replace(to_replace=find_val, value=mean)
        
        elif replace_val == 'DropNa()':
            self.data = self.data.dropna()        
        
        else:
            self.data = self.data.replace(to_replace=find_val, value=replace_val)
        
        DV_DC_Table.DV_DC_Table(table_frame, self.data)

    def save_dataframe(self):
        filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
        if filename is None or filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        elif not '.csv' in filename:
            filename = filename + '.csv'
        self.data.to_csv(filename)

class Scaling_Frame(tk.Frame):
    def __init__(self, root, table_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # COLUMN CHOICE CONTROL FRAME
        column_frame = tk.Frame(self)
        column_frame.grid(row=0, column=1, padx=pad_size)

        column_choice_label = tk.Label(column_frame, text='Select the columns to scale:')
        column_choice_label.pack()

        numeric_columns = self.data.select_dtypes(exclude=['object', 'category'])
        numeric_columns_list = list()
        for num_col in numeric_columns:
            numeric_columns_list.append(num_col)

        self.col_choice = list()

        def col_update(self, event):
            lbTup = event.widget.curselection()
            if lbTup:
                tmp = list()
                for tup in lbTup:
                    tmp.append(numeric_columns_list[tup])
                self.col_choice = tmp

        col_listbox = tk.Listbox(column_frame, selectmode=tk.MULTIPLE, justify=tk.CENTER)
        col_listbox.bind('<<ListboxSelect>>', lambda x: col_update(self, x))
        for num_column in numeric_columns_list:
            col_listbox.insert(tk.END, num_column)
        col_listbox.config(height=5)
        col_listbox.pack(side=tk.LEFT)

        col_scrollbar = tk.Scrollbar(column_frame)
        col_listbox.config(yscrollcommand=col_scrollbar.set)
        col_scrollbar.config(command=col_listbox.yview)
        col_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # SCALE CONTROL FRAME
        scale_frame = tk.Frame(self)
        scale_frame.grid(row=0, column=2, padx=pad_size)

        scale_label = tk.Label(scale_frame, text='Select the scaler to use:')
        scale_label.pack()

        self.scale_var = tk.Variable(value='Standard Scaler')
        option_list = list(['Standard Scaler', 'MinMax Scaler', 'Robust Scaler', 'Normalizer'])
        scale_option = tk.OptionMenu(scale_frame, self.scale_var, *option_list)
        scale_option.pack()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=3, padx=pad_size)

        scale_btn = tk.Button(button_frame, text='Scale or Normalize', command=lambda: self.scale(table_frame))
        scale_btn.pack()

        save_df_btn = tk.Button(
            button_frame, text='Save Dataframe Changes', command=lambda: self.save_dataframe())
        save_df_btn.pack()

    def scale(self, table_frame):
        if self.scale_var.get() == 'Standard Scaler':
            scaler = preprocessing.StandardScaler()
        elif self.scale_var.get() == 'MinMax Scaler':
            scaler = preprocessing.MinMaxScaler()
        elif self.scale_var.get() == 'Robust Scaler':
            scaler = preprocessing.RobustScaler()
        elif self.scale_var.get() == 'Normalizer':
            scaler = preprocessing.Normalizer()
        
        self.data[self.col_choice] = scaler.fit_transform(self.data[self.col_choice])

        DV_DC_Table.DV_DC_Table(table_frame, self.data)

    def save_dataframe(self):
        filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
        if filename is None or filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        elif not '.csv' in filename:
            filename = filename + '.csv'
        self.data.to_csv(filename)

class Factorize_Frame(tk.Frame):
    def __init__(self, root, table_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # COLUMN CHOICE CONTROL FRAME
        column_frame = tk.Frame(self)
        column_frame.grid(row=0, column=1, padx=pad_size)

        column_label = tk.Label(column_frame, text='Select the columns to factorize:')
        column_label.pack()

        columns = self.data.columns
        columns_list = list()
        for col in columns:
            columns_list.append(col)

        self.col_choice = list()

        def col_update(self, event):
            lbTup = event.widget.curselection()
            if lbTup:
                tmp = list()
                for tup in lbTup:
                    tmp.append(columns_list[tup])
                self.col_choice = tmp

        col_listbox = tk.Listbox(column_frame, selectmode=tk.MULTIPLE, justify=tk.CENTER)
        col_listbox.bind('<<ListboxSelect>>', lambda x: col_update(self, x))
        for column in columns_list:
            col_listbox.insert(tk.END, column)
        col_listbox.config(height=5)
        col_listbox.pack(side=tk.LEFT)

        col_scrollbar = tk.Scrollbar(column_frame)
        col_listbox.config(yscrollcommand=col_scrollbar.set)
        col_scrollbar.config(command=col_listbox.yview)
        col_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # FACTORIZE CONTROL FRAME
        factorize_frame = tk.Frame(self)
        factorize_frame.grid(row=0, column=2, padx=pad_size)

        factorize_label = tk.Label(factorize_frame, text='Select the factorizer to use:')
        factorize_label.pack()

        self.factorize_var = tk.Variable(value='Factorize')
        option_list = list(['Factorize', 'OneHot Encode'])
        scale_option = tk.OptionMenu(factorize_frame, self.factorize_var, *option_list)
        scale_option.pack()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=3, padx=pad_size)

        factorize_btn = tk.Button(button_frame, text='Factorize and Enumerate', command=lambda: self.factorize(table_frame))
        factorize_btn.pack()

        save_df_btn = tk.Button(
            button_frame, text='Save Dataframe Changes', command=lambda: self.save_dataframe())
        save_df_btn.pack()

    def factorize(self, table_frame):
        if self.factorize_var == 'Factorize':
            for col in self.col_choice:
                try:
                    labels, _ = pd.factorize(self.data[col])
                    col = 'factorized_'+col
                    self.data[col] = labels
                except:
                    messagebox.showwarning(title='Factoriztion Error', message=('Column: ', col, ' could not be factorized, if there are NaNs in the column, removal should allow factorization to work'))
        elif self.factorize_var == 'OneHot Encode':
            print('Build one hot encode function!')
        DV_DC_Table.DV_DC_Table(table_frame, self.data)

    def save_dataframe(self):
        filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
        if filename is None or filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        elif not '.csv' in filename:
            filename = filename + '.csv'
        self.data.to_csv(filename)

class Feature_Selection_Frame(tk.Frame):
    def __init__(self, root, table_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # FEATURE SELECTION CONTROL FRAME
        feature_selection_frame = tk.Frame(self)
        feature_selection_frame.grid(row=0, column=1, padx=pad_size)

        feature_selection_label = tk.Label(feature_selection_frame, text='Select the target column:')
        feature_selection_label.pack()

        self.feat_sel_var = tk.Variable(value=self.data.columns[0])
        option_list = self.data.columns
        feat_sel_option = tk.OptionMenu(feature_selection_frame, self.feat_sel_var, *option_list)
        feat_sel_option.pack()

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=2, padx=pad_size)

        feature_selection_btn = tk.Button(button_frame, text='Feature Selection', command=lambda: self.feature_selection(table_frame))
        feature_selection_btn.pack()

        save_df_btn = tk.Button(
            button_frame, text='Save Dataframe Changes', command=lambda: self.save_dataframe())
        save_df_btn.pack()

    def feature_selection(self, table_frame):
        cor = self.data.corr()
        cor_target = abs(cor[self.feat_sel_var.get()])
        selected = cor_target[cor_target>0.5]
        message = f'For the target column, {self.feat_sel_var.get()}, the selected columns are:\n{selected}'
        messagebox.showinfo(title='Feature Selection Results', message=message)

        #DV_DC_Table.DV_DC_Table(table_frame, self.data)

    def save_dataframe(self):
        filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
        if filename is None or filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        elif not '.csv' in filename:
            filename = filename + '.csv'
        self.data.to_csv(filename)


class Outliers_Frame(tk.Frame):
    def __init__(self, root, table_frame, **options):
        tk.Frame.__init__(self, root, **options)
        
        config = ConfigParser()
        config.read('datavis.ini')
        data_loc = config.get('general', 'dataset_location')
        self.data = pd.read_csv(data_loc, encoding='latin-1')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # OUTLIERS CONTROL FRAME
        outliers_frame = tk.Frame(self)
        outliers_frame.grid(row=0, column=1, padx=pad_size)

        # BUTTON CONTROL FRAME
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=2, padx=pad_size)

        outliers_btn = tk.Button(button_frame, text='Find Outliers', command=lambda: self.outliers(table_frame))
        outliers_btn.pack()

        save_df_btn = tk.Button(
            button_frame, text='Save Dataframe Changes', command=lambda: self.save_dataframe())
        save_df_btn.pack()

    def outliers(self, table_frame):
        print('Build outliers function!')
        """
        #Determine how many outliers exist in the data
        clf = LocalOutlierFactor()
        predictions = clf.fit_predict(X, y)

        # inliers are 1, outliers are -1
        predictions = np.where(predictions > 0, 'Inlier', 'Outlier')
        print(f'Predictions: {predictions}')
        """
        #DV_DC_Table.DV_DC_Table(table_frame, self.data)

    def save_dataframe(self):
        filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
        if filename is None or filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        elif not '.csv' in filename:
            filename = filename + '.csv'
        self.data.to_csv(filename)
