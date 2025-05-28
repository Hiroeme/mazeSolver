import unittest
from maze import Maze

class Test(unittest.TestCase):
    def test_maze_create_cells_1(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells),
            num_rows,
        )

    def test_maze_create_cells_2(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells),
            num_rows,
        )

    def test_maze_create_cells_3(self):
        num_cols = 0
        num_rows = 0
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )

        self.assertEqual(
            len(m1._Maze__cells),
            num_rows,
        )

    def test_maze_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__break_entrance_and_exit()
        self.assertEqual(
            m1._Maze__cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._Maze__cells[num_rows - 1][num_cols - 1].has_bot_wall,
            False,
        )


if __name__ == "__main__":
    unittest.main()