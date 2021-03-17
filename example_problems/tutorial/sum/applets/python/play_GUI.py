#!/usr/bin/env python3
from sys import exit, argv
import string 
import random

from tkinter import *

class Application(Frame):
           
    def submit_play(self):
        print(self.text.get())
        self.resp["text"] = input()

    def createWidgets(self):
        self.resp = Label(self)
        self.resp.pack()
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.play_button = Button(self)
        self.play_button["text"] = "Play",
        self.play_button["command"] = self.submit_play

        self.play_button.pack({"side": "left"})

        self.text = Entry(self)

        self.text.pack({"side": "left"})


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
       
exit(0)
