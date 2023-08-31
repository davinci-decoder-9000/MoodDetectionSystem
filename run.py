import sys
import os
from tkinter import *

window=Tk()
window.title("Student's Mood Recognition System")
window.geometry('640x410')
window.resizable(0, 0)

def run():
    os.system('python "d:\PYTHON FILES\Emotion-detection-master\src\main.py" --mode display')


x = Label(window,
                  text = "Student's Mood Recognition System",
                  font = 'Arial 24 bold').place(x = 40, 
                                                y = 120)               

btn = Button(window, 
             text="Analyze", 
             font = 'Arial 12 bold',
             bg="blue", 
             fg="white",
             height= 2, 
             width=15,
             command= run)
btn.place(relx=0.5, rely=0.5, anchor=CENTER)


window.mainloop()