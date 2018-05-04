from tkinter import *
import datetime

root = Tk()

lab = Label(root)
lab.pack()

def clock():
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    lab.config(text=time)
    root.after(1000, clock)

clock()
root.mainloop()
