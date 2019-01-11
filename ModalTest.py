from tkinter import *

root = Tk()

def raise_message():
    box = Toplevel(root)
    box.title('Error')
    box.transient(root)
    box.grab_set()
    message = Label(box, text="uhhh")
    tip = Label(box, text="[ Tip: Regular expressions can also be used to centre labels ]")
    button = Button(box, text='OK', command=lambda: box.destroy())
    message.grid(row=0, padx=5, pady=5)
    tip.grid(row=2, padx=5, pady=5)
    button.grid(row=3, padx=5, pady=5)
    root.wait_window(window=box)
    return 'uhhhhmmmmm'

test = raise_message()
print(test)
root.mainloop()