import tkinter as tk
import matplotlib.image as mpimg
from configparser import ConfigParser


class DV_Toolbar(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)

        self.toolbar = tk.Frame(master=root, bd=1, relief='raised')
        self.toolbar.grid(sticky='new')
        self.photo = tk.PhotoImage(file="open_file.png")
        self.import_btn = tk.Button(self.toolbar, image=self.photo, command=self.Select_Dataset)
        self.import_btn.grid(sticky='w')

        self.config = ConfigParser()

    def Select_Dataset(self, root):
        "Prompt user to select a dataset file"
        self.filename = tk.filedialog.askopenfilename(initialdir="/", title="Select Dataset", filetypes=(
            ("csv files", "*.csv"), ("xls files", "*.xls"), ("all files", "*.*")))
        self.config.read('datavis.ini')
        self.curr = self.config.get('general', 'dataset_location')
        print('tests')
        if self.filename and (self.curr != self.filename):  # new dataset?
            if self.config.getboolean('general', 'settings_reset_warning'):  # ask again?
                print('ask?')
                if self.Settings_Reset_Warning(root):  # continue?
                    print('updating')
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
        print('Cont.get: '+str(self.cont.get()))
        return self.cont.get()

    def Update_Data_Loc(self, string):
        "Saves updated data location to ini"
        self.config.read('datavis.ini')
        self.config.set('general', 'dataset_location', string)
        with open('datavis.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

    def Reset_ini(self, degree):  # FINISH ME
        "Reset ini to various degrees. 0 is all settings. 1 is only settings affected by dataset changes."
        if degree == 0:  # full reset
            pass
        else:  # partial reset
            if self.config.has_section('pairplot'):
                pass
