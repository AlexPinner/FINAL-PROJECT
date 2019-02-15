import tkinter as tk

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

def canvas_resizing(event):
    print('Resizing')

canvas = tk.Canvas(root)
canvas.config(bg='blue')
canvas.grid(row=0, column=0, sticky='nsew')
canvas.grid_rowconfigure(0, weight=1)
canvas.grid_columnconfigure(0, weight=1)
canvas.bind('<Configure>', canvas_resizing)

vsb = tk.Scrollbar(root, orient='vertical', command=canvas.yview_scroll)
vsb.grid(row=0, column=1, sticky='nse')
hsb = tk.Scrollbar(root, orient='horizontal', command=canvas.xview_scroll)
hsb.grid(row=1, column=0, sticky='sew')
canvas.config(xscrollcommand=vsb.set, yscrollcommand=hsb.set)

inner_frame = tk.Frame(canvas)
inner_frame.config(bg='red', width=200, height=800)
canvas.create_window(0, 0, window=inner_frame)



root.mainloop()