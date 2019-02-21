import tkinter as tk
from configparser import ConfigParser
import seaborn as sns

root = tk.Tk()

config = ConfigParser()
config.read('controls_test.ini')

# OPTION MENU
optVar = tk.Variable(value='None')
optList = ('None', 'One', 'Some', 'All')

try:
    print(optVar.get(), type(optVar.get()))
    optVar = tk.Variable(value=config.get('simple', 'option_var'))
    print(optVar.get(), type(optVar.get()))
except:
    pass

option = tk.OptionMenu(root, optVar, *optList)
option.pack()

# LISTBOX
lbList = ('L', 'I', 'S', 'T')
lbVar = ('T', 'I')

try:
    #print(lbVar, type(lbVar))
    lbVar = tuple(config.get('simple', 'lbox_var').split(','))
    if not all(lbVar):
        lbVar = tuple()
    #print(lbVar, type(lbVar))
except:
    pass

def lbSelect(event):
    global lbVar
    lbTup = event.widget.curselection()
    #print(lbTup, type(lbTup))
    tmp = list()
    for tup in lbTup:
        #print(lbList[tup])
        tmp.append(lbList[tup])
    #print(tmp, type(tmp))
    lbVar = tuple(tmp)
    #print(lbVar, type(lbVar))


lbox = tk.Listbox(root, selectmode=tk.MULTIPLE, justify=tk.CENTER)
lbox.bind('<<ListboxSelect>>', lambda x: lbSelect(x))
for item in lbList:
    lbox.insert(tk.END, item)
for var in lbVar:
    varIndex = lbox.get(0, tk.END).index(var)
    lbox.select_set(varIndex)
lbox.pack()

# CHECKBUTTON
checkVar = tk.Variable(value='Scatter')

try:
    print(checkVar.get(), type(checkVar.get()))
    checkVar = tk.Variable(value=config.get('simple', 'check_var'))
    print(checkVar.get(), type(checkVar.get()))
except:
    pass

chkBtn = tk.Checkbutton(root, variable=checkVar, onvalue='Scatter', offvalue='Reg', text=checkVar.get())
chkBtn.pack()

def chkBtnTextUpdate():
    chkBtn.config(text=checkVar.get())
chkBtn.config(command=lambda: chkBtnTextUpdate())

# COMMIT
def commit():
    if not config.has_section('simple'):
        config.add_section('simple')
    config.set('simple', 'option_var', optVar.get())
    config.set('simple', 'lbox_var', ','.join(lbVar))
    config.set('simple', 'check_var', checkVar.get())
    with open('controls_test.ini', 'w') as configfile:
        config.write(configfile)

# PREVIEW
def preview():
    print(optVar.get(), type(optVar.get()))
    print(','.join(lbVar), type(','.join(lbVar)))
    print(checkVar.get(), type(checkVar.get()))

cmmtBtn = tk.Button(root, text='Commit', command=lambda: commit())
cmmtBtn.pack()

prevBtn = tk.Button(root, text='Preview', command=lambda: preview())
prevBtn.pack()

root.mainloop()