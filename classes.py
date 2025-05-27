from tkinter import Tk, BOTH, Canvas

class Point():
    def __init__(self, x : int, y: int):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1 : Point, p2 : Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas : Canvas, fill_color : str):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

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

    def draw_line(self, line : Line, fill_color : str):
        line.draw(self.canvas, fill_color)