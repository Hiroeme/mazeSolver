from collections import defaultdict, deque
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

        if self.__num_rows != 0 and self.__num_cols != 0:
            self.__create_cells()
            self.__break_entrance_and_exit()
            self.__break_walls_r(0,0)
            self.__reset_cells_visited()


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
        time.sleep(0.03)

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
            neighbor_i, neighbor_j = neighbors[random.randrange(len(neighbors))]
            # knock down wall between current and neighbor

            difference = [neighbor_i - i, neighbor_j - j]
            # up knock neighbor bottom and current top
            if difference == [0, -1]:
                self.__cells[i][j].has_top_wall = False
                self.__cells[neighbor_i][neighbor_j].has_bot_wall = False
            # down knock neighbor top and current bot
            if difference == [0, 1]:
                self.__cells[i][j].has_bot_wall = False
                self.__cells[neighbor_i][neighbor_j].has_top_wall = False
            # right knock neighbor left and current right
            if difference == [1, 0]:
                self.__cells[i][j].has_right_wall = False
                self.__cells[neighbor_i][neighbor_j].has_left_wall = False
            # left knock neighbor right and current left
            if difference == [-1, 0]:
                self.__cells[i][j].has_left_wall = False
                self.__cells[neighbor_i][neighbor_j].has_right_wall = False
            # recurse onto the next neighbor
            self.__break_walls_r(neighbor_i, neighbor_j)

    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self, start_i, start_j, method="dfs"):
        if method == "dfs":
            return self._solve_r(start_i, start_j)
        if method == "bfs":
            return self._solve_bfs(start_i, start_j)
        
        # no method found
        return True

    def _solve_bfs(self, start_i, start_j):
        directions = [[0,1], [0,-1], [1,0], [-1, 0]]
        parent_map = defaultdict(tuple)
        queue = deque()
        # add current
        queue.append([start_i, start_j])
        
        # need a way to go back to the last split, undoing the paths we traversed 
        # previous cell
        found = False
        levels = []
        # while queue
        while len(queue) > 0:
            if found:
                break
            frontier = []
            for _ in range(len(queue)):
                self.__animate()
                # pop from queue
                i, j = queue.popleft()
                current_cell = self.__cells[i][j]
                current_cell.visited = True

                # if we reached exit exit
                if i == self.__num_rows - 1 and j == self.__num_cols - 1:
                    found = True
                    break

                # add valid neighbors from pop
                for dx, dy in directions:
                    new_i = i + dx
                    new_j = j + dy

                    if new_i == self.__num_rows or new_i < 0 or new_j == self.__num_cols or new_j < 0:
                        continue
                    if self.__cells[new_i][new_j].visited:
                        continue
                    if dx == 1 and current_cell.has_right_wall:
                        continue
                    if dx == -1 and current_cell.has_left_wall:
                        continue
                    if dy == 1 and current_cell.has_bot_wall:
                        continue
                    if dy == -1 and current_cell.has_top_wall:
                        continue
                    
                    parent_map[(new_i, new_j)] = (i, j)
                    frontier.append([new_i, new_j])
                    queue.append([new_i, new_j])
            levels.append(frontier)
            
        if not found:
            return False
        
        solution_path = []
        curr = (self.__num_rows - 1, self.__num_cols - 1)
        while curr != (start_i, start_j):
            solution_path.append(curr)
            curr = parent_map[curr]
        solution_path.append((start_i,start_j))
        solution_path.reverse()

        solution_path_set = set(solution_path)
        for level in levels:
            for i, j in level:
                pi, pj = parent_map[(i, j)]
                parent = self.__cells[pi][pj]
                current = self.__cells[i][j]
                if (i, j) in solution_path_set:
                    parent.draw_move(current)
                else:
                    parent.draw_move(current, undo=True)
                self.__animate()

        return True

    def _solve_r(self, i, j):
        
        directions = [[0,1], [0,-1], [1,0], [-1, 0]]
        self.__animate()
        self.__cells[i][j].visited = True
        current_cell = self.__cells[i][j]
        
        if i == self.__num_rows - 1 and j == self.__num_cols - 1:
            return True
        
        for dx, dy in directions:
            new_i = i + dx
            new_j = j + dy
            
            # valid cell check
            if new_i == self.__num_rows or new_i < 0 or new_j == self.__num_cols or new_j < 0:
                continue

            # is there a wall check
            if dx == 1 and current_cell.has_right_wall:
                continue
            if dx == -1 and current_cell.has_left_wall:
                continue
            if dy == 1 and current_cell.has_bot_wall:
                continue
            if dy == -1 and current_cell.has_top_wall:
                continue
                

            new_cell = self.__cells[new_i][new_j]

            if new_cell.visited:
                continue

            # moving
            current_cell.draw_move(new_cell)
            if (self._solve_r(new_i, new_j)):
                return True
            # undo
            current_cell.draw_move(new_cell, undo=True)

        return False

            