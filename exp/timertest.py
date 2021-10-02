import tkinter as tk
import time

class timer():
    def __init__(self, timeLimit):
        self.limit = timeLimit
        self.root = tk.Tk()
        self.label = tk.Label(text="", font=("ＭＳゴシック", 48), fg="black")
        self.label.pack()
        self.updateTimer()
        self.root.mainloop()

    def updateTimer(self):
        self.label.configure(text=self.limit)
        self.limit -= 1
        self.root.after(1000, self.updateTimer)

t = timer(30)