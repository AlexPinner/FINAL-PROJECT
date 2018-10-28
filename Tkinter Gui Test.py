from tkinter import *

my_window = Tk()

blue_frame= Frame(my_window,bg='Blue')

m = PanedWindow(orient=HORIZONTAL)
m.pack(fill=BOTH, expand=1)

top = Label(m, text="left pane")
m.add(blue_frame)

bottom = Label(m, text="right pane")
m.add(bottom)

mainloop()