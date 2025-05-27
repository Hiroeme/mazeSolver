from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.root_widget = Tk()
        
        
        self.root_widget.title = "Graphical User Interface Maze Solver"
        self.canvas = Canvas(bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

win = Window(800, 600)
win.wait_for_close()
