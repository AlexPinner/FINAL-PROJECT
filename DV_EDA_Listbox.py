import tkinter as tk
from configparser import ConfigParser

import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import DV_ZoomableCanvas


class EDA_Listbox(tk.Listbox):
    def __init__(self, root, canvas_frame, frames):
        "Creates a listbox for selecting EDA graphs"
        tk.Listbox.__init__(self, root)

        self.config = ConfigParser()

        self.EDA_list = EDA_List = ["Pairplot", "Correlation Matrix", "Bar Chart", "Scatter Plot", "PCA"]
        self.EDA_Listbox = EDA_Listbox = self.Create_Listbox(root, EDA_List)
        #for frame in frames:
        #    print("Values: ", frames[frame])
        #print("Keys: ", frames.keys())
        #print("Usable Name? ", frames['!pp_frame'])
        # REMEMBER: TO PASS EVENT TO MULTI PARAM BOUND FUNCTION YOU MUST USE 'lambda x:' INSTEAD OF 'lambda:' (x IS THE EVENT!)
        EDA_Listbox.bind('<<ListboxSelect>>', lambda x: self.EDA_onSelect(x, canvas_frame, frames))

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
        "Returns the length of the longest item in a list"
        len_max = 0
        for m in list_items:
            if len(m) > len_max:
                len_max = len(m)
        return len_max
    
    def raise_frame(self, frame):
        "Raises a frame"
        frame.tkraise()

    def EDA_onSelect(self, event, canvas_frame, frames):
        "Creates selected graph type using current settings and displays it"
        self.w = w = event.widget
        config = self.config
        if(w.curselection()):
            # get data about current selection
            index = int(w.curselection()[0])
            value = w.get(index)

            # Check ini for graph settings
            config.read('datavis.ini')

            # display 'please stand by' image
            """
            fig.clear()
            a = fig.add_subplot(111)
            img_arr = mpimg.imread('PSB.png')
            a.imshow(img_arr)
            a.axis('off')
            canvas.draw()
            """

            for widget in canvas_frame.winfo_children():
                widget.destroy()
            file = 'PSB.png'
            canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
            canvas.grid()
            
            if (index == 0):  # pairplot
                # raise pp controls
                self.raise_frame(frames['!pp_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()

                    # import user graph settings
                    pp_hue = tk.Variable(value=config.get('pairplot', 'hue'))  # which column determines color of points
                    if pp_hue.get() == 'None':
                        pp_hue = None
                    else:
                        pp_hue = pp_hue.get()
                    pp_vars = tuple(config.get('pairplot', 'vars').split(','))  # which columns to use in plot
                    if not all(pp_vars):
                        pp_vars = None
                    pp_kind = tk.Variable(value=config.get('pairplot', 'kind'))  # fit regression line?
                    pp_kind = pp_kind.get()
                    pp_diag_kind = tk.Variable(value=config.get('pairplot', 'diag_kind'))  # graph type to use along diagonal
                    pp_diag_kind = pp_diag_kind.get()

                    # terminal feedback for debugging
                    print('--EDA LB onSelect PP--')
                    print('vars: ', pp_vars, type(pp_vars))
                    print('hue: ', pp_hue, type(pp_hue))
                    print('kind: ', pp_kind, type(pp_kind))
                    print('diag_kind: ', pp_diag_kind, type(pp_diag_kind))

                    # create and display custom graph
                    plt.clf()
                    pp = sns.pairplot(data=data, hue=pp_hue, vars=pp_vars, kind=pp_kind, diag_kind=pp_diag_kind)
                    pp.savefig('pp.png')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('pp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'pp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()
                    
                else:  # go with default fig creation
                    data = sns.load_dataset('Iris')
                    data = data.dropna()
                    plt.clf()
                    pp = sns.pairplot(data=data, kind='reg', hue='species')
                    pp.savefig('pp.png')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('pp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'pp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

            elif (index == 1):  # correlation matrix
                # raise cm controls
                self.raise_frame(frames['!cm_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()
                    data = data.corr()

                    # import user graph settings
                    cm_annot = tk.BooleanVar(value=config.get('correlation', 'annot'))  # print numbers in cells?
                    cm_annot = cm_annot.get()
                    cm_cbar = tk.BooleanVar(value=config.get('correlation', 'cbar'))  # show color bar?
                    cm_cbar = cm_cbar.get()
                    cm_square = tk.BooleanVar(value=config.get('correlation', 'square'))  # make cells square?
                    cm_square = cm_square.get()

                    # terminal feedback for debugging
                    print('--EDA LB onSelect CM--')
                    print('annot: ', cm_annot, type(cm_annot))
                    print('cbar: ', cm_cbar, type(cm_cbar))
                    print('square: ', cm_square, type(cm_square))
                    
                    # create and display custom graph
                    plt.clf()
                    cm = sns.heatmap(data=data, annot=cm_annot, cbar=cm_cbar, square=cm_square)
                    cm.get_figure().savefig('cm.png', bbox_inches='tight')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('cm.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'cm.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

                else:  # go with default fig creation
                    data = sns.load_dataset('titanic')
                    data = data.dropna()
                    data = data.corr()
                    plt.clf()
                    cm = sns.heatmap(data=data)
                    cm.get_figure().savefig('cm.png', bbox_inches='tight')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('cm.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'cm.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

            elif (index == 2):  # bar chart
                # raise bp controls
                self.raise_frame(frames['!bp_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()
                    
                    # default options
                    bp_x = tk.Variable(value=None)
                    bp_y = tk.Variable(value=None)
                    bp_hue = tk.Variable(value=None)
                    bp_ci = tk.Variable(value=95)

                    # import user graph settings
                    bp_x = tk.Variable(value=config.get('bar', 'x'))  # x var
                    bp_y = tk.Variable(value=config.get('bar', 'y'))  # y var
                    bp_hue = tk.Variable(value=config.get('bar', 'hue'))  # hue column
                    bp_ci = tk.Variable(value=config.get('bar', 'ci'))  # confidence intervals

                    # prepare variables for graph
                    if bp_x.get() == 'None' or bp_x.get() == '':
                        bp_x = None
                    else:
                        bp_x = bp_x.get()
                    if bp_y.get() == 'None' or bp_y.get() == '':
                        bp_y = None
                    else:
                        bp_y = bp_y.get()
                    if bp_hue.get() == 'None' or bp_hue.get() == '':
                        bp_hue = None
                    else:
                        bp_hue = bp_hue.get()
                    if bp_ci.get() == 'None' or bp_ci.get() == '':
                        bp_ci = None
                    else:
                        try:
                            bp_ci = int(bp_ci.get())
                        except:
                            bp_ci = bp_ci.get()
                    
                    # terminal feedback for debugging
                    print('--EDA LB onSelect BP--')
                    print('x: ', bp_x, type(bp_x))
                    print('y: ', bp_y, type(bp_y))
                    print('hue: ', bp_hue, type(bp_hue))
                    print('ci: ', bp_ci, type(bp_ci))

                    # create and display custom graph
                    plt.clf()
                    bp = sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue, ci=bp_ci)
                    plt.xticks(rotation=45)
                    bp.figure.savefig('bp.png', bbox_inches='tight')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('bp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'bp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

                else:  # go with default fig creation
                    data = sns.load_dataset("flights")
                    data = data.dropna()
                    plt.clf()
                    bp = sns.barplot(data=data, x='month', y='passengers', ci=None)
                    plt.xticks(rotation=45)
                    bp.figure.savefig('bp.png', bbox_inches='tight')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('bp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'bp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

            elif (index == 3):  # scatter plot
                # raise sp controls
                self.raise_frame(frames['!sp_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('scatter') and config.has_section('general')):
                    # import user data set
                    data = config.get('general', 'dataset_location')
                    data = data.dropna()
                    
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
                    
                    # terminal feedback for debugging
                    print('SP ON LISTBOX:')
                    print('X: ', sp_x)
                    print('Y: ', sp_y)
                    print('Hue: ', sp_hue)
                    print('Legend: ', sp_legend)
                    print('Scatter: ', sp_scatter)
                    print('Fit Reg: ', sp_fit_reg)

                    # create and display custom graph
                    plt.clf()
                    sp = sns.lmplot(data=data, x=sp_x, y=sp_y, hue=sp_hue,
                                    legend=sp_legend, scatter=sp_scatter, fit_reg=sp_fit_reg)
                    sp.savefig('sp.png')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('sp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'sp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

                else:  # go with default fig creation
                    data = sns.load_dataset("tips")
                    data = data.dropna()
                    plt.clf()
                    sp = sns.lmplot(data=data, x="total_bill", y="tip")
                    sp.savefig('sp.png')
                    """
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('sp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    """
                    file = 'sp.png'
                    for widget in canvas_frame.winfo_children():
                        widget.destroy()
                    canvas = DV_ZoomableCanvas.ZoomCanvas(canvas_frame, file)
                    canvas.grid()

            elif (index == 4):  # pca
                # raise pca controls
                self.raise_frame(frames['!pca_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('pca') and config.has_section('general')):
                    print('You selected item %d: "%s"' % (index, value))

                else:  # go with default fig creation
                    print('You selected item %d: "%s"' % (index, value))
