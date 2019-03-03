import os.path
import time
import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk

import matplotlib.image as mpimg
import seaborn as sns

import DV_DC_Control_Panels
import DV_DC_Listbox
import DV_DC_Table
import DV_EDA_Control_Panels
import DV_EDA_Listbox
import DV_Toolbar


class DataVis():
    def __init__(self):
        
        # create main window
        self.root = root = tk.Tk()
        root.title('DataVis')
        #root.geometry('{}x{}'.format(2400, 1200))                   # REMOVE THIS ANNN....

        # print(font.names()) #all available fonts
        #self.myfont = myfont = tk.font.nametofont('TkDefaultFont')
        #myfont.configure(size=24)                                   # ......NNND THIS, to get normal resolution on non mac monitors
        # Pre-brake fonts and window size so it doesn't happen later
        #self.data = data = sns.load_dataset('Iris')
        #sns.pairplot(data=data)                                     # ALSO REMOVE THIS SINCE IT'S NOT NEEDED ON NON MAC MONITORS

        # if config file doesn't exist, create it
        if not os.path.isfile('datavis.ini'):
            file = open('datavis.ini', 'w')
            file.close()
        config = ConfigParser()
        config.read('datavis.ini')
        if os.path.isfile('auto-mpg.csv') and not config.has_section('general'):
            config.add_section('general')
            config.set('general', 'dataset_location', 'auto-mpg.csv')
            with open('datavis.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()
                
        # create notebook (thing that controls the tabs)
        self.note = note = ttk.Notebook(root)

        #################
        # Create toolbar
        ###############
        self.toolbar = DV_Toolbar.DV_Toolbar(root)
        #toolbar.grid()

        ###############################
        # Create tab for data cleaning
        #############################
        self.DC_Bottom_Pane = DC_Bottom_Pane = tk.PanedWindow(note)
        DC_Bottom_Pane.config(orient='vertical', sashwidth=4)
        DC_Bottom_Pane.grid(sticky='nsew')

        self.DC_Top_Pane = DC_Top_Pane = tk.PanedWindow(DC_Bottom_Pane)
        DC_Top_Pane.config(orient='horizontal', sashwidth=4)
        DC_Top_Pane.grid(sticky='nsew')
        DC_Bottom_Pane.add(DC_Top_Pane, stretch='always')

        self.DC_Controls_Frame = DC_Controls_Frame = tk.Frame(DC_Bottom_Pane)
        DC_Controls_Frame.config(width=200, height=100)
        DC_Controls_Frame.grid(sticky='nsew')
        DC_Controls_Frame.grid_columnconfigure(0, weight=1)
        DC_Bottom_Pane.add(DC_Controls_Frame, stretch='never')

        self.DC_Listbox_Frame = DC_Listbox_Frame = tk.Frame(DC_Top_Pane)
        DC_Listbox_Frame.config(width=100, height=200)
        DC_Listbox_Frame.grid(sticky='nsew')
        DC_Top_Pane.add(DC_Listbox_Frame, stretch='never')

        self.DC_Table_Frame = DC_Table_Frame = tk.Frame(DC_Top_Pane)
        DC_Table_Frame.grid(sticky='nsew')
        DC_Table_Frame.grid_rowconfigure(0, weight=1)
        DC_Table_Frame.grid_columnconfigure(0, weight=1)
        DC_Top_Pane.add(DC_Table_Frame, stretch='always')

        self.table = table = DV_DC_Table.DV_DC_Table(DC_Table_Frame, None)
        table.grid(sticky='nsew')
        
        find_replace_controls = DV_DC_Control_Panels.Find_Replace_Frame(DC_Controls_Frame, DC_Table_Frame)
        scaling_controls = DV_DC_Control_Panels.Scaling_Frame(DC_Controls_Frame, DC_Table_Frame)
        factorize_controls = DV_DC_Control_Panels.Factorize_Frame(DC_Controls_Frame, DC_Table_Frame)
        feature_selection_controls = DV_DC_Control_Panels.Feature_Selection_Frame(DC_Controls_Frame, DC_Table_Frame)
        #outlier_controls = DV_DC_Control_Panels.Outliers_Frame(DC_Controls_Frame, DC_Table_Frame)
        DC_placeholder_frame = tk.Frame(DC_Controls_Frame)
        DC_placeholder_frame.grid(row=0, column=0, sticky='nsew')
        DC_placeholder_frame.grid_rowconfigure(0, weight=1)
        DC_placeholder_frame.grid_columnconfigure(0, weight=1)
        DC_hint_frame = tk.Frame(DC_placeholder_frame)
        DC_hint_frame.grid(row=0, column=0)
        DC_select_start = tk.Label(DC_hint_frame, text='Select an option to begin cleaning')
        DC_select_start.grid(sticky='nsew')

        self.DC_control_frames = DC_control_frames = {}

        for frame in (find_replace_controls, scaling_controls, factorize_controls, feature_selection_controls):
            frame.grid(row=0, column=0, sticky='nsew')
            DC_control_frames[frame._name] = frame
        
        DC_placeholder_frame.tkraise()
        
        self.DC_Listbox = DV_DC_Listbox.DC_Listbox(DC_Listbox_Frame, DC_control_frames)

        #################################################
        # Create tab for exploratory data analysis (EDA)
        ###############################################
        self.EDA_Bottom_Pane = EDA_Bottom_Pane = tk.PanedWindow(note)
        EDA_Bottom_Pane.config(orient='vertical', bd=0, sashwidth=4)
        EDA_Bottom_Pane.grid(sticky='nsew')

        self.EDA_Top_Pane = EDA_Top_Pane = tk.PanedWindow(EDA_Bottom_Pane)
        EDA_Top_Pane.config(orient='horizontal', bd=0, sashwidth=4)
        EDA_Top_Pane.grid(sticky='nsew')
        EDA_Bottom_Pane.add(EDA_Top_Pane, stretch='always')

        self.EDA_Controls_Frame = EDA_Controls_Frame = tk.Frame(EDA_Bottom_Pane)
        EDA_Controls_Frame.config(width=200, height=100)
        EDA_Controls_Frame.grid(sticky='nsew')
        EDA_Controls_Frame.grid_columnconfigure(0, weight=1)
        EDA_Bottom_Pane.add(EDA_Controls_Frame, stretch='never')

        self.EDA_Listbox_Frame = EDA_Listbox_Frame = tk.Frame(EDA_Top_Pane)
        EDA_Listbox_Frame.config(width=100, height=200)
        EDA_Listbox_Frame.grid(sticky='nsew')
        EDA_Top_Pane.add(EDA_Listbox_Frame, stretch='never')

        self.EDA_Canvas_Frame = EDA_Canvas_Frame = tk.Frame(EDA_Top_Pane)
        EDA_Canvas_Frame.config(bg='black')
        EDA_Canvas_Frame.grid(sticky='nsew')
        EDA_Canvas_Frame.grid_rowconfigure(0, weight=1)
        EDA_Canvas_Frame.grid_columnconfigure(0, weight=1)
        EDA_Top_Pane.add(EDA_Canvas_Frame, stretch='always')

        #pp_controls = ppControlsTest.PP_Frame(EDA_Controls_Frame, EDA_Canvas)
        pp_controls = DV_EDA_Control_Panels.PP_Frame(EDA_Controls_Frame, EDA_Canvas_Frame)
        cm_controls = DV_EDA_Control_Panels.CM_Frame(EDA_Controls_Frame, EDA_Canvas_Frame)
        bp_controls = DV_EDA_Control_Panels.BP_Frame(EDA_Controls_Frame, EDA_Canvas_Frame)
        sp_controls = DV_EDA_Control_Panels.SP_Frame(EDA_Controls_Frame, EDA_Canvas_Frame)
        EDA_placeholder_frame = tk.Frame(EDA_Controls_Frame)
        EDA_placeholder_frame.grid(row=0, column=0, sticky='nsew')
        EDA_placeholder_frame.grid_rowconfigure(0, weight=1)
        EDA_placeholder_frame.grid_columnconfigure(0, weight=1)
        EDA_hint_frame = tk.Frame(EDA_placeholder_frame)
        EDA_hint_frame.grid(row=0, column=0)
        EDA_select_start = tk.Label(EDA_hint_frame, text='Select a graph type to begin EDA')
        EDA_select_start.grid(sticky='nsew')

        self.EDA_control_frames = EDA_control_frames = {}

        for frame in (pp_controls, cm_controls, bp_controls, sp_controls):
            frame.grid(row=0, column=0, sticky='nsew')
            EDA_control_frames[frame._name] = frame
        EDA_placeholder_frame.tkraise()

        self.EDA_Listbox = DV_EDA_Listbox.EDA_Listbox(EDA_Listbox_Frame, EDA_Canvas_Frame, EDA_control_frames)


        ###############################
        # Add the tabs to the notebook
        #############################
        note.add(DC_Bottom_Pane, text="Data Cleaning")
        note.add(EDA_Bottom_Pane, text="EDA")

        note.grid(sticky='nesw')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        while(not table.winfo_ismapped()):
            time.sleep(0.25)
            root.update()

        table.scroll_reset()

def main():
    dv = DataVis()
    dv.root.mainloop()

if __name__ == '__main__': 
    main()

#################################################################################################
#### TODO: ######################################################################################

# FINALIZE AND TEST DATAFRAME VIEW
# TEST ALL THE CONTROL PANELS, AS MANY OPTIONS AND COMBINATIONS AS POSSIBLE TO CHECK FOR ERRORS

# LOADING BAR AMOUNT AND/OR ERROR REPORTING CAN BE PLACED AT (THESE ARE GUESSES):
    # ERROR READING INI, 0% ACT, %0 DIS
    # ERROR UPDATING LOADSCREEN OR LOADBAR, 2% ACT, %5 DIS
    # ERROR RAISING CONTROL PANEL, 5% ACT, 15% DIS
    # ERROR READING DATA, 8% ACT, 25% DIS
    # ERROR SETTING VARIABLES, 12% ACT, 45% DIS
    # ERROR PLOTTING GRAPH, BAD OPTION IN GRAPH SETTINGS, 95% ACT, 70% DIS
    # ERROR SAVING TO PNG, 96% ACT, 75% DIS
    # ERROR CLEARING CANVAS, 97% ACT, 80% DIS
    # ERROR READING PNG, 98% ACT, 85% DIS
    # ERROR DISPLAYING PNG, 99% ACT, DIS 95%
# LOCATIONS IN EXAMPLE CODE:
"""
    #EDA ON SELECT STARTS
        index = int(w.curselection()[0])
        value = w.get(index)
        # Check ini for graph settings
        config.read('datavis.ini')
# ERROR READING INI, 0% ACT, %0 DIS

        # display 'please stand by' image
        fig.clear()
        a = fig.add_subplot(111)
        img_arr = mpimg.imread('PSB.png')
        a.imshow(img_arr)
        a.axis('off')
        EDA_Canvas.draw()
# ERROR UPDATING LOADSCREEN OR LOADBAR, 2% ACT, %5 DIS

        elif (index == 3):  # scatter plot
            raise_frame(sp_frame)
# ERROR RAISING CONTROL PANEL, 5% ACT, 15% DIS

            # use custom vals for fig creation
            if(config.has_section('scatter') and config.has_section('general')):
                # import user data set
                data = config.get('general', 'dataset_location')
                data = data.dropna()
# ERROR READING DATA, 8% ACT, 25% DIS
                
                # import user graph settings
                sp_x = config.get('scatter', 'x')  # x var
                sp_y = config.get('scatter', 'y')  # y var
                sp_hue = config.get('scatter', 'hue')  # hue column
                sp_legend = config.getboolean(
                    'scatter', 'legend')  # display legend?
                sp_scatter = config.getboolean(
                    'scatter', 'scatter')  # draw scatter?
                # fit linear regression line?
                sp_fit_reg = config.get('scatter', 'fit_reg')

                print('SP ON LISTBOX:')
                print('X: ', sp_x)
                print('Y: ', sp_y)
                print('Hue: ', sp_hue)
                print('Legend: ', sp_legend)
                print('Scatter: ', sp_scatter)
                print('Fit Reg: ', sp_fit_reg)
# ERROR SETTING VARIABLES, 12% ACT, 45% DIS

                sp = sns.lmplot(data=data, x=sp_x, y=sp_y, hue=sp_hue,
                                legend=sp_legend, scatter=sp_scatter, fit_reg=sp_fit_reg)
# ERROR PLOTTING GRAPH, BAD OPTION IN GRAPH SETTINGS, 95% ACT, 70% DIS

                sp.savefig('sp.png')
# ERROR SAVING TO PNG, 96% ACT, 75% DIS

                fig.clear()
                a = fig.add_subplot(111)
# ERROR CLEARING CANVAS, 97% ACT, 80% DIS
                img_arr = mpimg.imread('sp.png')
# ERROR READING PNG, 98% ACT, 85% DIS
                a.imshow(img_arr)
                a.axis('off')
                EDA_Canvas.draw()
# ERROR DISPLAYING PNG, 99% ACT, DIS 95%
"""
# MAY HAVE TO ADD DELAYS TO SHOW LOADING BAR CHANGING AT ALL
# SOMEHOW SEPERATE THE DELAY ON BAR FROM ACTUAL CODE PROGRESS

# ERROR ON STARTUP COULD ASK IF THE USER WANTS TO RESET INI TO DEFAULT TO SEE IF THAT HELPS

# IN DV_EDA_LISTBOX.PY THE EDA ON SELECT FUNCTION UNDER THE '# prepare variables for graph' SECTION
# THIS SECTION CAN HANDLE BOOL, STR, OR INT AT THE SAME TIME FOR EXAMPLE:
"""
                    if bp_ci.get() == 'None' or bp_ci.get() == ' ':
                        bp_ci = None
                    else:
                        try:
                            bp_ci = int(bp_ci.get())
                        except:
                            bp_ci = bp_ci.get()
"""
# BUT THIS VARIABLE IS IN A CHECKBUTTON WHICH DOES NOT ALLOW INTS, WHAT IF
# WHILE IT IS CHECKED ON THERE IS AN ENTRY FOR 0-100 CONFIDENCE INTERVALS?
