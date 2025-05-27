from classes import Window, Point, Line

def main():
    win = Window(800, 600)
    fill_color = "black"
    p1 = Point(100, 100)
    p2 = Point(300, 300)
    p3 = Point(500, 200)
    line_one = Line(p1, p2)
    line_two = Line(p2, p3)
    line_three = Line(p1, p3)
    win.draw_line(line_one, fill_color)
    win.draw_line(line_two, fill_color)
    win.draw_line(line_three, fill_color)
    win.wait_for_close()

main()

