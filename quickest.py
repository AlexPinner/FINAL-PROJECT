from tkinter import *
import pandas as pd

root=Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

data = pd.read_csv('auto-mpg.csv')

frame=Frame(root,width=300,height=300)
frame.config(bg='blue')
frame.grid(row=0,column=0, sticky='nsew')
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas=Canvas(frame,bg='red',width=300,height=300,scrollregion=(0,0,500,500))

hbar=Scrollbar(frame,orient=HORIZONTAL)
#hbar.pack(side=BOTTOM,fill=X)
hbar.grid(row=1, column=0, sticky='nsew')
hbar.config(command=canvas.xview)

vbar=Scrollbar(frame,orient=VERTICAL)
#vbar.pack(side=RIGHT,fill=Y)
vbar.grid(row=0,column=1,sticky='nsew')
vbar.config(command=canvas.yview)

canvas.config(width=300,height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
#canvas.pack(side=LEFT,expand=True,fill=BOTH)
canvas.grid(row=0, column=0, sticky='nsew')

inner_frame = Frame(canvas)

col_num = 0
for column in data:
      column_header = Label(inner_frame, text=str(column), relief='raised')
      column_header.grid(row=0, column=col_num, sticky='ew')
      row_num = 1
      for row in data[column]:
            column_data = Label(inner_frame, text=str(row), relief='ridge')
            column_data.grid(row=row_num, column=col_num, sticky='ew')
            row_num += 1
      col_num += 1

def onFrameConfigure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

canvas.create_window((0,0), window=inner_frame)
inner_frame.bind("<Configure>", onFrameConfigure)

def scroll_reset():
      canvas.xview_moveto(0)
      canvas.yview_moveto(0)

btn = Button(root, text='move scrollbars', command=scroll_reset)
btn.grid()

root.mainloop()
