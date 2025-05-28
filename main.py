from classes import Window
from maze import Maze

def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 20, 30, 10, 10, win)

    win.wait_for_close()

main()

