import tkinter as tk
import tkinter.filedialog
import matplotlib.image as mpimg
from configparser import ConfigParser


class DV_Toolbar(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)

        self.toolbar = tk.Frame(master=root, bd=1, relief='raised')
        self.toolbar.grid(sticky='new')
        self.import_photo = tk.PhotoImage(file="open_file.png")
        self.import_btn = tk.Button(self.toolbar, image=self.import_photo, command=lambda: self.Select_Dataset(root))
        self.import_btn.grid(row=0, column=1, sticky='nw')
        self.reset_photo = tk.PhotoImage(file="reset_ini.png")
        self.reset_btn = tk.Button(self.toolbar, image=self.reset_photo, command=lambda: self.ini_Reset_Dialog(root))
        self.reset_btn.grid(row=0, column=0, sticky='nw')

        self.config = ConfigParser()

    def Select_Dataset(self, root):
        "Prompt user to select a dataset file"
        self.filename = tk.filedialog.askopenfilename(initialdir="/", title="Select Dataset", filetypes=(
            ("csv files", "*.csv"), ("xls files", "*.xls"), ("all files", "*.*")))
        self.config.read('datavis.ini')
        self.curr = self.config.get('general', 'dataset_location')
        if self.filename and (self.curr != self.filename):  # new dataset?
            if not self.config.has_option('general', 'settings_reset_warning'):
                self.config.set('general', 'settings_reset_warning', 'True')
            if self.config.getboolean('general', 'settings_reset_warning'):  # ask again?
                if self.Settings_Reset_Warning(root):  # continue?
                    self.Update_Data_Loc(self.filename)  # change dataset
            else:
                self.Update_Data_Loc(self.filename)

    def Settings_Reset_Warning(self, root):
        "Creates modal dialog to ensure user wants to change dataset even if it resets ini settings"
        self.dlg = tk.Toplevel(master=root)
        self.dlg.transient(root)
        self.dlg.grab_set()
        self.ask = tk.BooleanVar()
        self.cont =tk.BooleanVar()

        def Yes():
            self.cont.set(True)
            self.dlg.destroy()

        def No():
            self.cont.set(False)
            self.dlg.destroy()

        tk.Label(self.dlg, text="Switching datasets will reset any graph settings\n that are sensitive to data changes. Continue?").grid(
            row=0, columnspan=2)
        tk.Button(self.dlg, text="Continue", command=Yes).grid(
            row=1, column=0, sticky='ne')
        tk.Button(self.dlg, text="Cancel", command=No).grid(
            row=1, column=1, sticky='nw')
        tk.Checkbutton(self.dlg, variable=self.ask, text="Don't ask again", padx=2,
                    pady=2).grid(row=2, columnspan=2, sticky='s')
        self.dlg.wait_window(self.dlg)
        if(self.ask.get()):
            self.config.read('datavis.ini')
            self.config.set('general', 'settings_reset_warning', 'False')
            with open('datavis.ini', 'w') as configfile:
                self.config.write(configfile)
            configfile.close()
        return self.cont.get()

    def Update_Data_Loc(self, string):
        "Saves updated data location to ini"
        self.config.read('datavis.ini')
        self.config.set('general', 'dataset_location', string)
        with open('datavis.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()
        self.Reset_ini(1)

    def Reset_ini(self, degree):  # FINISH ME
        "Reset ini to various degrees. 0 is all settings. 1 is only settings affected by dataset changes"
        config = self.config
        if degree == 0:  # full reset
            if config.has_section('pairplot'):
                config.remove_section('pairplot')
            if config.has_section('correlation'):
                config.remove_section('correlation')
            if config.has_section('bar'):
                config.remove_section('bar')
            if config.has_section('scatter'):
                config.remove_section('scatter')
            if config.has_section('pca'):
                config.remove_section('pca')
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()
        else:  # partial reset
            if config.has_section('pairplot'):
                config.set('pairplot', 'hue', 'None')
                config.set('pairplot', 'vars', '')
            if config.has_section('bar'):
                config.set('bar', 'x', 'None')
                config.set('bar', 'y', 'None')
                config.set('bar', 'hue', 'None')
            if config.has_section('scatter'):
                config.remove_section('scatter')
            if config.has_section('pca'):
                config.remove_section('pca')
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()
    
    def ini_Reset_Dialog(self, root):
        "Ask user if they want to reset ini and to what degree"
        self.dlg = tk.Toplevel(master=root)
        self.dlg.transient(root)
        self.dlg.grab_set()

        def reset_and_close(self, degree):
            self.Reset_ini(degree)
            self.dlg.destroy()

        all_lbl = tk.Label(self.dlg, text='Reset all settings?')
        all_lbl.grid(row=0, column=0)
        all_btn = tk.Button(self.dlg, text='All', command=lambda: reset_and_close(self, 0))
        all_btn.grid(row=1, column=0)
        some_lbl = tk.Label(self.dlg, text='Reset settings reliant on dataframe?')
        some_lbl.grid(row=0, column=1)
        some_btn = tk.Button(self.dlg, text='Some', command=lambda: reset_and_close(self, 1))
        some_btn.grid(row=1, column=1)
        cancel_btn = tk.Button(self.dlg, text='Cancel', command=lambda: self.dlg.destroy())
        cancel_btn.grid(columnspan=2)