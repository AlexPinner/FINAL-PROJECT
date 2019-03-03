import tkinter as tk
from tkinter import filedialog, ttk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelBinarizer

data = pd.read_csv('auto-mpg.csv', encoding='latin-1')
data = data.replace(to_replace='?', value=np.nan)
data = data.dropna()
#data.info()

print(data.columns[0])

"""
labels, uniques = pd.factorize(data['model_year'])
print('labels: ', labels, labels.size)
print('uniques: ', uniques)
data['fact_model_year'] = labels
print(data)
"""
"""
col_choice = list(['model_year','origin','car_name'])

for col in col_choice:
    labels, uniques = pd.factorize(data[col])
    print('labels: ', labels, labels.size)
    col = 'factorized_'+col
    data[col] = labels
    print(data[col])

print(data)
"""

"""
scaler = preprocessing.MinMaxScaler()
cols = list(['mpg','displacement','weight','acceleration'])
print(cols, type(cols))
data[cols] = scaler.fit_transform(data[cols])

print(data)
data.info()
"""

"""
data = pd.read_csv('auto-mpg.csv', encoding='latin-1')
data=data.replace(to_replace='?', value=np.nan)

for column in data.select_dtypes(exclude=['int64', 'float64']):
    try:
        data[column] = data[column].astype('float64')
    except:
        pass

data=data.dropna()

print(data)
data.info()
"""

"""
root=tk.Tk()
find_variable = tk.Variable()
find_values = (0, np.nan)

def printVar():
    print(find_variable.get(), type(find_variable.get()))

find_combo = ttk.Combobox(root, values=find_values, textvariable=find_variable)
find_combo.pack()

print_btn = tk.Button(root, text='Print Box Var', command=lambda: printVar())
print_btn.pack()

filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save file as", filetypes = (("csv files","*.csv"),("xls files","*.xls"),("all files","*.*")))
if filename is '': # asksaveasfile return `None` if dialog closed with "cancel".
    print('save_df in dc_controls; filename was None')
print(filename + '.csv', type(filename))
root.mainloop()
"""
