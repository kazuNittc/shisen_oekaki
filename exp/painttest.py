import tkinter
from PIL import Image, ImageDraw

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()
        self.setup()

    def create_widgets(self):
        self.vr = tkinter.IntVar()
        self.vr.set(1)
        self.test_canvas = tkinter.Canvas(self, bg='white', width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.test_canvas.grid(row=1, column=0, columnspan=4)
        self.test_canvas.bind('<B1-Motion>', self.paint)
        self.test_canvas.bind('<ButtonRelease-1>', self.reset)

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.im = Image.new('RGB', (self.winfo_screenwidth(), self.winfo_screenheight()), 'white')
        self.draw = ImageDraw.Draw(self.im)

    def clear_canvas(self, event):
        self.test_canvas.delete(tkinter.ALL)

    def paint(self, event):
        paint_color = 'black'
        if self.old_x and self.old_y:
            self.test_canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5.0, fill=paint_color, capstyle=tkinter.ROUND, smooth=tkinter.TRUE, splinesteps=36)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=paint_color, width=5)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

root = tkinter.Tk()
app = Application(master=root)
root.bind('<KeyPress-space>', app.clear_canvas)
root.bind('<Control-c>', root.quit)
root.attributes('-fullscreen', True)
root.mainloop()
