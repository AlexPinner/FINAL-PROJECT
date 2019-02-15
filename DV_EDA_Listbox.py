import tkinter as tk
import pandas as pd
import seaborn as sns
from configparser import ConfigParser
import matplotlib.image as mpimg

class EDA_Listbox(tk.Listbox):
    def __init__(self, root, fig, canvas, frames):
        "Creates a listbox to select EDA graphs"
        tk.Listbox.__init__(self, root)

        self.config = ConfigParser()

        self.EDA_list = EDA_List = ["Pairplot", "Correlation Matrix", "Bar Chart", "Scatter Plot", "PCA"]
        self.EDA_Listbox = EDA_Listbox = self.Create_Listbox(root, EDA_List)
        #for frame in frames:
        #    print("Values: ", frames[frame])
        #print("Keys: ", frames.keys())
        #print("Usable Name? ", frames['!pp_frame'])
        # REMEMBER: TO PASS EVENT TO MULTI PARAM BOUND FUNCTION YOU MUST USE 'lambda x:' INSTEAD OF 'lambda:' (x IS THE EVENT!)
        EDA_Listbox.bind('<<ListboxSelect>>', lambda x: self.EDA_onSelect(x, fig, canvas, frames))

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

    def EDA_onSelect(self, event, fig, canvas, frames):
        self.w = w = event.widget
        config = self.config
        if(w.curselection()):
            # get data about current selection
            index = int(w.curselection()[0])
            value = w.get(index)

            # Check ini for graph settings
            config.read('datavis.ini')

            # display 'please stand by' image
            fig.clear()
            a = fig.add_subplot(111)
            img_arr = mpimg.imread('PSB.png')
            a.imshow(img_arr)
            a.axis('off')
            canvas.draw()
            
            if (index == 0):  # pairplot
                # raise pp controls
                self.raise_frame(frames['!pp_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()

                    # default options
                    pp_hue = tk.Variable(value=None)
                    pp_vars = tk.Variable(value=None)
                    pp_kind = tk.Variable(value='scatter')
                    pp_diag_kind = tk.Variable(value='auto')

                    # import user graph settings, if they don't exist create them and set to default values
                    try:
                        pp_hue = tk.Variable(value=config.get('pairplot', 'hue'))  # which column determines color of points
                        pp_vars = tk.Variable(value=config.get('pairplot', 'vars').split(','))  # which columns to use in plot
                        pp_kind = tk.Variable(value=config.get('pairplot', 'kind'))  # fit regression line?
                        pp_diag_kind = tk.Variable(value=config.get('pairplot', 'diag_kind'))  # graph type to use along diagonal
                    except:
                        if not config.has_section('pairplot'):
                            config.add_section('pairplot')
                        config.set('pairplot', 'hue', str(pp_hue.get()))
                        config.set('pairplot', 'vars', str(pp_vars.get()))
                        config.set('pairplot', 'kind', str(pp_kind.get()))
                        config.set('pairplot', 'diag_kind', str(pp_diag_kind.get()))
                        with open('datavis.ini', 'w') as configfile:
                            config.write(configfile)
                        configfile.close()

                    # prepare variables for graph
                    if pp_hue.get() == 'None' or pp_hue.get() == '':
                        pp_hue = None
                    else:
                        pp_hue = pp_hue.get()

                    if pp_vars.get() == 'None' or pp_vars.get() == '':
                        pp_vars = None
                    else:
                        pp_vars = pp_vars.get()

                    if pp_kind.get() == 'None' or pp_kind.get() == '':
                        pp_kind = None
                    else:
                        pp_kind = pp_kind.get()

                    if pp_diag_kind.get() == 'None' or pp_diag_kind.get() == '':
                        pp_diag_kind = None
                    else:
                        pp_diag_kind = pp_diag_kind.get()
                    
                    # terminal feedback for debugging
                    print('--EDA LB onSelect PP--')
                    print('Pairplot options were:')
                    print('hue: ', pp_hue, type(pp_hue))
                    print('vars: ', pp_vars, type(pp_vars))
                    print('kind: ', pp_kind, type(pp_kind))
                    print('diag_kind: ', pp_diag_kind, type(pp_diag_kind))

                    # create and display custom graph
                    pp = sns.pairplot(data=data, hue=None, vars=pp_vars, kind='scatter', diag_kind='auto')
                    pp.savefig('pp.png')
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('pp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()
                    
                else:  # go with default fig creation
                    data = sns.load_dataset('Iris')
                    data = data.dropna()
                    pp = sns.pairplot(data=data, kind='reg', hue='species')
                    pp.savefig('pp.png')
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('pp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()

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

                    # default options
                    cm_annot = tk.Variable(value=None)
                    cm_cbar = tk.Variable(value=True)
                    cm_square = tk.Variable(value=False)

                    # import user graph settings, if they don't exist create them and set to default values
                    try:
                        cm_annot = tk.Variable(value=config.get('correlation', 'annot'))  # print numbers in cells?
                        cm_cbar = tk.Variable(value=config.get('correlation', 'cbar'))  # show colobar?
                        cm_square = tk.Variable(value=config.get('correlation', 'square'))  # make cells square?
                    except:
                        if not config.has_section('correlation'):
                            config.add_section('correlation')
                        config.set('correlation', 'annot', str(cm_annot.get()))
                        config.set('correlation', 'cbar', str(cm_cbar.get()))
                        config.set('correlation', 'square', str(cm_square.get()))
                        with open('datavis.ini', 'w') as configfile:
                            config.write(configfile)
                        configfile.close()
                    
                    # prepare variables for graph
                    try:
                        cm_annot = bool(int(cm_annot.get()))
                    except:
                        if cm_annot.get() == 'None' or cm_annot.get() == '':
                            cm_annot = None
                        else:
                            cm_annot = cm_annot.get()
                    try:
                        cm_cbar = bool(int(cm_cbar.get()))
                    except:
                        if cm_cbar.get() == 'None' or cm_cbar.get() == '':
                            cm_cbar = None
                        else:
                            cm_cbar = cm_cbar.get()
                    try:
                        cm_square = bool(int(cm_square.get()))
                    except:
                        if cm_square.get() == 'None' or cm_square.get() == '':
                            cm_square = None
                        else:
                            cm_square = cm_square.get()



                    """
                    print("Annot: ", cm_annot.get(), type(cm_annot.get()))
                    if cm_annot.get() == 'None' or ' ':
                        cm_annot = None
                    elif cm_annot.get() == '0' or '1':
                        cm_annot = int(cm_annot.get())
                    print("Cbar: ", cm_cbar.get())
                    if cm_cbar.get() == '0' or '1':
                        cm_cbar = int(cm_cbar.get())
                    elif cm_cbar.get() == 'None' or ' ':
                        cm_cbar = None
                    print("Square: ", cm_square.get())
                    if cm_square.get() == '0' or '1':
                        cm_square = int(cm_square.get())
                    elif cm_square.get() == 'None' or ' ':
                        cm_square = None
                    """

                    # terminal feedback for debugging
                    print('--EDA LB onSelect CM--')
                    print('Correlation Matrix options were:')
                    print('annot: ', cm_annot, type(cm_annot))
                    print('cbar: ', cm_cbar, type(cm_cbar))
                    print('square: ', cm_square, type(cm_square))
                    
                    # create and display custom graph
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.heatmap(data=data, annot=cm_annot, cbar=cm_cbar, square=cm_square, ax=a)
                    canvas.draw()

                else:  # go with default fig creation
                    data = sns.load_dataset('titanic')
                    data = data.dropna()
                    data = data.corr()
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.heatmap(data=data, ax=a)
                    canvas.draw()

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

                    # import user graph settings, if they don't exist create them and set to default values
                    try:
                        bp_x = tk.Variable(value=config.get('bar', 'x'))  # x var
                        bp_y = tk.Variable(value=config.get('bar', 'y'))  # y var
                        bp_hue = tk.Variable(value=config.get('bar', 'hue'))  # hue column
                        bp_ci = tk.Variable(value=config.get('bar', 'ci'))  # confidence intervals
                    except:
                        if not config.has_section('bar'):
                            config.add_section('bar')
                        config.set('bar', 'x', str(bp_x.get()))
                        config.set('bar', 'y', str(bp_y.get()))
                        config.set('bar', 'hue', str(bp_hue.get()))
                        config.set('bar', 'ci', str(bp_ci.get()))
                        with open('datavis.ini', 'w') as configfile:
                            config.write(configfile)
                        configfile.close()

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
                    print('Barplot options were:')
                    print('x: ', bp_x, type(bp_x))
                    print('y: ', bp_y, type(bp_y))
                    print('hue: ', bp_hue, type(bp_hue))
                    print('ci: ', bp_ci, type(bp_ci))

                    # create and display custom graph
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue, ci=bp_ci, ax=a)
                    canvas.draw()

                else:  # go with default fig creation
                    data = sns.load_dataset("flights")
                    data = data.dropna()
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.barplot(data=data, x='month', y='passengers', ci=None, ax=a)
                    canvas.draw()

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
                    
                    # create and display custom graph
                    print('SP ON LISTBOX:')
                    print('X: ', sp_x)
                    print('Y: ', sp_y)
                    print('Hue: ', sp_hue)
                    print('Legend: ', sp_legend)
                    print('Scatter: ', sp_scatter)
                    print('Fit Reg: ', sp_fit_reg)
                    sp = sns.lmplot(data=data, x=sp_x, y=sp_y, hue=sp_hue,
                                    legend=sp_legend, scatter=sp_scatter, fit_reg=sp_fit_reg)
                    sp.savefig('sp.png')
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('sp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()

                else:  # go with default fig creation
                    data = sns.load_dataset("tips")
                    data = data.dropna()
                    sp = sns.lmplot(data=data, x="total_bill", y="tip")
                    sp.savefig('sp.png')
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('sp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    canvas.draw()

            elif (index == 4):  # pca
                # raise pca controls
                self.raise_frame(frames['!pca_frame'])
                # use custom data for fig creation if they have loaded a custom dataset
                if(config.has_section('pca') and config.has_section('general')):
                    print('You selected item %d: "%s"' % (index, value))

                else:  # go with default fig creation
                    print('You selected item %d: "%s"' % (index, value))
                    fig.clear()
                    canvas.draw()