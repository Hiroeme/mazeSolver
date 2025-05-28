from classes import Window, Cell
import time

class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win: Window = None,
        ):

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__window = win
        
        # stores cells as a 2D List
        self.__cells = []

        self.__create_cells()

    def __create_cells(self):

        self.__cells = []

        for _ in range(self.__num_rows):
            row = []
            for _ in range(self.__num_cols):
                row.append(Cell(self.__window))
            self.__cells.append(row)

        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                self.__draw_cell(i, j)

            
    def __draw_cell(self, i, j):
        if not self.__window:
            return
        x1 = (i * self.__cell_size_x) + self.__x1
        y1 = (j * self.__cell_size_y) + self.__y1

        # x1 = x - (self.__cell_size_x // 2) 
        # y1 = y - (self.__cell_size_y // 2)

        # x2 = x + (self.__cell_size_x // 2)
        # y2 = y + (self.__cell_size_y // 2)

        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        
        # print(x1, y1, x2, y2)
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if not self.__window:
            return
        self.__window.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_rows - 1][self.__num_cols - 1].has_bot_wall = False
        self.__draw_cell(self.__num_rows - 1, self.__num_cols - 1)
        