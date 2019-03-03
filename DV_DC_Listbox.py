import tkinter as tk
import pandas as pd
import seaborn as sns
from configparser import ConfigParser

class DC_Listbox(tk.Listbox):
    def __init__(self, root, frames):
        "Creates a listbox to select EDA graphs"
        tk.Listbox.__init__(self, root)

        self.config = ConfigParser()

        self.DC_List = DC_List = ["Find and Replace", "Scaling", "Factorize", "Feature Selection"]
        self.DC_Listbox = DC_Listbox = self.Create_Listbox(root, DC_List)
        #for frame in frames:
        #    print("Values: ", frames[frame])
        #print("Keys: ", frames.keys())
        #print("Usable Name? ", frames['!pp_frame'])
        # REMEMBER: TO PASS EVENT TO MULTI PARAM BOUND FUNCTION YOU MUST USE 'lambda x:' INSTEAD OF 'lambda:' (x IS THE EVENT!)
        DC_Listbox.bind('<<ListboxSelect>>', lambda x: self.Cleaning_onSelect(x, frames))

    def Create_Listbox(self, root, list_items):
        "Returns a listbox populated with list_items"
        # font=('Fixed', 14) #stick this in lbox params after width=...
        self.listbox = listbox = tk.Listbox(root, width=self.Len_Max(list_items))

        self.scrollbar = scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        scrollbar.config(command=listbox.yview)
        # always pack scrollbar before listbox
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        # always pack listbox after scrollbar
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for m in list_items:
            listbox.insert(tk.END, str(m))

        return listbox
    
    def Len_Max(self, list_items):
        "Returns the length of the longest list item"
        len_max = 0
        for m in list_items:
            if len(m) > len_max:
                len_max = len(m)
        return len_max
    
    def raise_frame(self, frame):
        frame.tkraise()

    def Cleaning_onSelect(self, evt, frames):
        "Event that raises correct controls when a selection is made in the cleaning menu"
        self.w = evt.widget
        # print(w.curselection())
        if(self.w.curselection()):
            index = int(self.w.curselection()[0])
            if(index == 0):  # find and replace
                self.raise_frame(frames['!find_replace_frame'])
            elif(index == 1):  # scaling
                self.raise_frame(frames['!scaling_frame'])
            elif (index == 2):  # factorize
                self.raise_frame(frames['!factorize_frame'])
            elif (index == 3):  # feature selection
                self.raise_frame(frames['!feature_selection_frame'])
            """
            elif (index == 4):  # outliers
                self.raise_frame(frames['!outliers_frame'])
            """
