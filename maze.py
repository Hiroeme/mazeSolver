from classes import Window, Cell
import time, random

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
            seed = None,
        ):

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__window = win

        self.__seed = random.seed(seed) if seed else 0

        # stores cells as a 2D List
        self.__cells = []

        self.__create_cells()

        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)


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
        time.sleep(0.01)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_rows - 1][self.__num_cols - 1].has_bot_wall = False
        self.__draw_cell(self.__num_rows - 1, self.__num_cols - 1)
    
    def __break_walls_r(self, i, j):
        directions = [[0,1], [0,-1], [1,0], [-1, 0]]
        self.__cells[i][j].visited = True

        while True:
            neighbors = []

            # check neighbors
            for dx, dy in directions:
                new_i = i + dx
                new_j = j + dy

                if new_i == self.__num_rows or new_i < 0 or new_j == self.__num_cols or new_j < 0:
                    continue
                if self.__cells[new_i][new_j].visited:
                    continue

                neighbors.append([new_i, new_j])
            # if no neighbors
            if not neighbors:
                # draw current and return
                self.__draw_cell(i, j)
                return

            # pick random neighbor
            neighbor_x, neighbor_y = neighbors[random.randrange(len(neighbors))]
            # knock down wall between current and neighbor

            difference = [neighbor_x - i, neighbor_y - j]
            # up knock neighbor bottom and current top
            if difference == [0, -1]:
                self.__cells[i][j].has_top_wall = False
                self.__cells[neighbor_x][neighbor_y].has_bot_wall = False
            # down knock neighbor top and current bot
            if difference == [0, 1]:
                self.__cells[i][j].has_bot_wall = False
                self.__cells[neighbor_x][neighbor_y].has_top_wall = False
            # right knock neighbor left and current right
            if difference == [1, 0]:
                self.__cells[i][j].has_right_wall = False
                self.__cells[neighbor_x][neighbor_y].has_left_wall = False
            # left knock neighbor right and current left
            if difference == [-1, 0]:
                self.__cells[i][j].has_left_wall = False
                self.__cells[neighbor_x][neighbor_y].has_right_wall = False
            # recurse onto the next neighbor
            self.__break_walls_r(neighbor_x, neighbor_y)