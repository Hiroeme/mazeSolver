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
        self.__root_widget = Tk()
        self.__root_widget.title = "Graphical User Interface Maze Solver"
        self.__canvas = Canvas(bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root_widget.update_idletasks()
        self.__root_widget.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
        self.__root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line : Line, fill_color : str):
        line.draw(self.__canvas, fill_color)

class Cell():
    def __init__(self, window : Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window

    def draw(self, x1, y1, x2, y2):
        if not self.__win:
            return
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            point_one = Point(self.__x1, self.__y1)
            point_two = Point(self.__x1, self.__y2)

            new_line = Line(point_one, point_two)
            self.__win.draw_line(new_line, "black")

        if self.has_right_wall:
            point_one = Point(self.__x2, self.__y1)
            point_two = Point(self.__x2, self.__y2)

            new_line = Line(point_one, point_two)
            self.__win.draw_line(new_line, "black")

        if self.has_top_wall:
            point_one = Point(self.__x1, self.__y1)
            point_two = Point(self.__x2, self.__y1)

            new_line = Line(point_one, point_two)
            self.__win.draw_line(new_line, "black")

        if self.has_bottom_wall:
            point_one = Point(self.__x1, self.__y2)
            point_two = Point(self.__x2, self.__y2)

            new_line = Line(point_one, point_two)
            self.__win.draw_line(new_line, "black")

    def draw_move(self, to_cell, undo=False):
        if not self.__win:
            return
        fill_color = "red" if not undo else "grey"

        mid_x1, mid_y1 = (self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2
        mid_x2, mid_y2 = (to_cell.__x1 + to_cell.__x2) // 2, (to_cell.__y1 + to_cell.__y2) // 2 

        center_point = Point(mid_x1, mid_y1)
        to_cell_center_point = Point(mid_x2, mid_y2)

        new_line = Line(center_point, to_cell_center_point)

        self.__win.draw_line(new_line, fill_color)

