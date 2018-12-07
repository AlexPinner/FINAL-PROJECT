from tkinter import *
from tkinter import ttk

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()

class Yellow_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="yellow"

class Orange_Frame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self["height"]=150
        self["width"]=150
        self["bg"]="orange"

big_pane = PanedWindow(orient=HORIZONTAL)
big_pane.pack(fill=BOTH, expand=1)

"""
#This section works for listboxes in paned windows
listbox = Listbox(big_pane)
listbox.pack()

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

big_pane.add(listbox)
"""

"""
#this section is like the previous one but with a scrollbar
left = Frame(big_pane)
left.pack()

len_max = 0
list_items = ["item1", "item2", "Testing to see if expanddddddddddddddd", "item33"]
#Cleaning_list = ["Find and Replace","Scaling","Factorize","Feature Selection", "Outliers"]
#EDA_list = ["Pairplot","Correlation Matrix","Bar Chart","Scatter Plot","PCA"]

for m in list_items:
    if len(m) > len_max:
        len_max = len(m)

listbox = Listbox(left, width= len_max)

scrollbar = Scrollbar(left, orient=VERTICAL)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)

listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

for m in list_items:
    listbox.insert(END, str(m))

for i in range(1000):
    listbox.insert(END, str(i))

big_pane.add(left)
"""

#This section is like the previous one with scrollbar but with a listbox selection event
def EDA_onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    #replace this with meaningful switches
    if(value=="item1"):
        print('You selected item %d: "%s"' % (index, value))
    elif(index==3):
        print('You selected item %d: "%s"' % (index, value))

def Cleaning_onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print(w.curselection()[0])

left = Frame(big_pane)
left.pack()

len_max = 0
list_items = ["item1", "item2", "Testing to see if expanddddddddddddddd", "item33"]
#Cleaning_list = ["Find and Replace","Scaling","Factorize","Feature Selection", "Outliers"]
#EDA_list = ["Pairplot","Correlation Matrix","Bar Chart","Scatter Plot","PCA"]

for m in list_items:
    if len(m) > len_max:
        len_max = len(m)

listbox = Listbox(left, width= len_max)
listbox.bind('<<ListboxSelect>>', Cleaning_onSelect)

scrollbar = Scrollbar(left, orient=VERTICAL)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)

listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

for m in list_items:
    listbox.insert(END, str(m))

for i in range(1000):
    listbox.insert(END, str(i))

big_pane.add(left)


right = PanedWindow(orient=VERTICAL)
right.pack(fill=BOTH, expand=1)
big_pane.add(right)
top = Orange_Frame(big_pane)
right.add(top)
bottom = Yellow_Frame(big_pane)
right.add(bottom)

mainloop()