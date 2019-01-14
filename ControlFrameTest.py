import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

root = Tk()

config = ConfigParser()
config.read('controls_test.ini')

pp_frame = Frame(root).pack()

cars = pd.read_csv(
    r'C:\Users\Alex Pinner\Desktop\Full Sail\FINAL PROJECT\auto-mpg.csv', encoding='latin-1')

columns_list = cars.columns
pp_hue_combo_list = []

for column in columns_list:
    pp_hue_combo_list.append(column)

print(pp_hue_combo_list)

pp_hue = Variable()
# var.set(pp_hue_combo_list[0]) # default option if applicable, leave out if option is none or blank to start with
#if leaving it out to be none doesn't work with how the config.set and save work then have none (like a string) be the default value to begin with


def hue_on_select(Event):
    # replace this with graph updates to allow user to preview changes before applying?
    print(pp_hue.get())


# The Combobox is also a bit easier to add and remove items after the widget has been created
pp_hue_combo = ttk.Combobox(
    pp_frame, values=pp_hue_combo_list, textvariable=pp_hue)
pp_hue_combo.pack()
pp_hue_combo.bind('<<ComboboxSelected>>', hue_on_select)

# The OptionMenu was designed to have a static number of items that are set when the widget is created
pp_hue_option = OptionMenu(
    pp_frame, pp_hue, *pp_hue_combo_list, command=hue_on_select)
pp_hue_option.pack()

def apply_on_select():
    config.set('pairplot', 'hue', pp_hue.get())
    #rest of settings here
    with open('controls_test.ini', 'w') as configfile:
        config.write(configfile)

apply_button = Button(pp_frame, text='Apply', command=apply_on_select).pack()

# PUT ALL THE NECESSARY STUFF IN A FRAME CLASS FOR EACH GRAPH TPYE, for ex: def pp_frame(Frame):

root.mainloop()
