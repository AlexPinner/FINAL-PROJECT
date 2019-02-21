import tkinter as tk
from configparser import ConfigParser
import pandas as pd
import seaborn as sns

class DV_Table(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)

        self.frame = tk.Frame(root, width=300, height=300)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.frame, width=300, height=300, scrollregion=(0, 0, 500, 500))

        self.hbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.hbar.grid(row=1, column=0, sticky='nsew')
        self.hbar.config(command=self.canvas.xview)

        self.vbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.vbar.grid(row=0, column=1, sticky='nsew')
        self.vbar.config(command=self.canvas.yview)

        self.canvas.config(width=300, height=300)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.inner_frame = tk.Frame(self.canvas, bg='black')

        config = ConfigParser()
        config.read('datavis.ini')
        if config.has_section('general'):
            data_loc = config.get('general', 'dataset_location')
            data = pd.read_csv(data_loc, encoding='latin-1')
        else:
            data = sns.load_dataset('iris')
        self.create_table(data)

        self.canvas.create_window((0, 0), window=self.inner_frame)
        self.inner_frame.bind("<Configure>", self.onFrameConfigure)

    def create_table(self, data):
        self.clear_table()
        col_num = 0
        for column in data:
            column_header = tk.Label(
                self.inner_frame, text=str(column), relief='raised')
            column_header.grid(row=0, column=col_num, sticky='ew')
            row_num = 1
            for row in data[column]:
                column_data = tk.Label(
                    self.inner_frame, text=str(row), relief='ridge')
                column_data.grid(row=row_num, column=col_num, sticky='ew')
                row_num += 1
            col_num += 1

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def scroll_reset(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def clear_table(self):
        for label in list(self.inner_frame.children.values()):
            label.destroy()
