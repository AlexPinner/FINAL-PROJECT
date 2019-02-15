import tkinter as tk
from configparser import ConfigParser
import matplotlib.image as mpimg

class DV_Listbox(tk.Frame):
    def __init__(self, root, list_items):
        "Returns a listbox created in window and populated with list_items"
        tk.Frame.__init__(self, root)

        # font=('Fixed', 14) #stick this in Listbox() after width=...
        self.listbox = tk.Listbox(root, width=self.Len_Max(list_items))

        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # always pack scrollbar before listbox

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        # always pack scrollbar before listbox
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for m in list_items:
            self.listbox.insert(tk.END, str(m))

        self.config = ConfigParser()

    def Len_Max(self, list_item):
        "Returns the length of the longest list item"
        self.len_max = 0
        for m in list_item:
            if len(m) > self.len_max:
                self.len_max = len(m)
        return self.len_max

    def raise_frame(self, frame):
        frame.tkraise()

    def Cleaning_onSelect(self, evt):
        "Event that raises correct controls when a selection is made in the cleaning menu"
        self.w = evt.widget
        # print(w.curselection())
        if(self.w.curselection()):
            index = int(self.w.curselection()[0])
            value = self.w.get(index)
            if(index == 0):  # find and replace
                print('You selected item %d: "%s"' % (index, value))
            elif(index == 1):  # scaling
                print('You selected item %d: "%s"' % (index, value))
            elif (index == 2):  # factorize
                print('You selected item %d: "%s"' % (index, value))
            elif (index == 3):  # feature selection
                print('You selected item %d: "%s"' % (index, value))
            elif (index == 4):  # outliers
                print('You selected item %d: "%s"' % (index, value))
    
    def EDA_onSelect(self, evt, figure, EDA_Canvas, pp_frame, cm_frame, bp_frame):
        self.w = evt.widget
        if(self.w.curselection()):
            # get data about current selection
            index = int(self.w.curselection()[0])
            value = self.w.get(index)
            # Check ini for graph settings
            self.config.read('datavis.ini')
            # display 'please stand by' image
            fig.clear()
            a = fig.add_subplot(111)
            img_arr = mpimg.imread('PSB.png')
            a.imshow(img_arr)
            a.axis('off')
            EDA_Canvas.draw()
            if (index == 0):  # pairplot
                self.raise_frame(pp_frame)
                # use custom vals for fig creation
                if(config.has_section('pairplot') and config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()

                    # import user graph settings
                    # which column determines color of points
                    pp_hue = config.get('pairplot', 'hue')
                    if pp_hue == 'None':
                        pp_hue = None
                    
                    # which columns to use in plot
                    pp_vars = config.get('pairplot', 'vars').split(',')
                    if pp_vars == ['None'] or pp_vars == ['']:
                        pp_vars = None

                    # fit regression line?
                    pp_kind = config.get('pairplot', 'kind')

                    # which graphs to use along diagonal
                    pp_diag_kind = config.get('pairplot', 'diag_kind')

                    # create and display custom graph
                    print('PP ON LISTBOX:')
                    print('Hue: ', pp_hue)
                    print('Vars: ', pp_vars)
                    print('Kind: ', pp_kind)
                    print('Diag_Kind: ', pp_diag_kind)
                    pp = sns.pairplot(data=data, hue=pp_hue, vars=pp_vars,
                                    kind=pp_kind, diag_kind=pp_diag_kind)
                    pp.savefig('pp.png')
                    fig.clear()
                    a = fig.add_subplot(111)
                    img_arr = mpimg.imread('pp.png')
                    a.imshow(img_arr)
                    a.axis('off')
                    EDA_Canvas.draw()
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
                    EDA_Canvas.draw()
            elif (index == 1):  # correlation matrix
                self.raise_frame(cm_frame)
                # use custom vals for fig creation
                if(config.has_section('correlation') and config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()
                    data = data.corr()

                    # import user graph settings
                    cm_annot = config.getboolean(
                        'correlation', 'annot')  # print numbers in cells?
                    cm_cbar = config.getboolean(
                        'correlation', 'cbar')  # show colobar?
                    cm_square = config.getboolean(
                        'correlation', 'square')  # make cells square?
                    
                    # create and display custom graph
                    print('CM ON LISTBOX:')
                    print('Annot: ', cm_annot)
                    print('Cbar: ', cm_cbar)
                    print('Square: ', cm_square)
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.heatmap(data=data, annot=cm_annot,
                                cbar=cm_cbar, square=cm_square, ax=a)
                    EDA_Canvas.draw()
                else:  # go with default fig creation
                    data = sns.load_dataset('titanic')
                    data = data.dropna()
                    data = data.corr()
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.heatmap(data=data, ax=a)
                    EDA_Canvas.draw()
            elif (index == 2):  # bar chart
                self.raise_frame(bp_frame)
                # use custom vals for fig creation
                if(config.has_section('bar') and config.has_section('general')):
                    # import user data set
                    data_loc = config.get('general', 'dataset_location')
                    data = pd.read_csv(data_loc, encoding='latin-1')
                    data = data.dropna()
                    
                    # import user graph settings
                    bp_x = config.get('bar', 'x')  # x var
                    bp_y = config.get('bar', 'y')  # y var
                    bp_hue = config.get('bar', 'hue')  # hue column
                    bp_ci = config.get('bar', 'ci')  # confidence intervals

                    # create and display custom graph
                    print('BP ON LISTBOX:')
                    print('X: ', bp_x)
                    print('Y: ', bp_y)
                    print('Hue: ', bp_hue)
                    print('Ci: ', bp_ci)
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue,
                                ci=bp_ci, ax=a)
                    EDA_Canvas.draw()
                else:  # go with default fig creation
                    data = sns.load_dataset("flights")
                    data = data.dropna()
                    fig.clear()
                    a = fig.add_subplot(111)
                    sns.barplot(data=data, x='month',
                                y='passengers', ci=None, ax=a)
                    EDA_Canvas.draw()
            elif (index == 3):  # scatter plot
                self.raise_frame(sp_frame)
                # use custom vals for fig creation
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
                    EDA_Canvas.draw()
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
                    EDA_Canvas.draw()
            elif (index == 4):  # pca
                self.raise_frame(pca_frame)
                # use custom vals for fig creation
                if(config.has_section('pca') and config.has_section('general')):
                    print('You selected item %d: "%s"' % (index, value))
                else:  # go with default fig creation
                    print('You selected item %d: "%s"' % (index, value))
                    fig.clear()
                    EDA_Canvas.draw()