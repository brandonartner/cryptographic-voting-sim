from tkinter import *

import TreeMaker as TM

def t_command(event=None):
    text = E1.get()
    tm.parse(text)
    tm.parse('display')
    E1.delete(0, 'end')

tm = TM.TreeMaker()

top = Tk()
L1 = Label(top, text="REPL Command:")
L1.grid(row=0, column=0)
E1 = Entry(top)
E1.bind('<Return>', t_command)
E1.grid(row=0, column=1)

top.mainloop()
