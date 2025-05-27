from classes import Window, Point, Line, Cell

def main():
    win = Window(800, 600)

    cell_one = Cell(win)
    cell_one.draw(100, 100, 300, 300)

    cell_two = Cell(win)
    cell_two.draw(50, 50, 75, 75)

    cell_one.draw_move(cell_two)
    win.wait_for_close()

main()

