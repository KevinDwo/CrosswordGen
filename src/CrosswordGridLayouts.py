from CrosswordGridTemplate import CrosswordGridTemplate 
from Direction import Direction

class CrosswordGridLayouts:
    @staticmethod
    def load_layout(number: int) -> CrosswordGridTemplate:
        if number == 1: 
            grid = CrosswordGridTemplate(12, 12)
            grid.set_placeholder(0, 0, 7, Direction.RIGHTABOVE, 1)
            grid.set_placeholder(0, 1, 7, Direction.DOWNABOVE, 2)
            grid.set_placeholder(0, 2, 3, Direction.DOWNABOVE, 3)
            grid.set_placeholder(0, 3, 5, Direction.DOWNABOVE, 4)
            grid.set_placeholder(0, 5, 7, Direction.DOWNRIGHT, 5)
            grid.set_placeholder(0, 7, 5, Direction.DOWNRIGHT, 6)
            grid.set_placeholder(0, 8, 4, Direction.DOWNABOVE, 7)
            grid.set_placeholder(0, 10, 6, Direction.DOWNRIGHT, 8)
            grid.set_placeholder(0, 11, 5, Direction.DOWNABOVE, 9)
            grid.set_placeholder(1, 7, 4, Direction.RIGHTLEFT, 10)
            grid.set_placeholder(2, 0, 4, Direction.RIGHTLEFT, 11)
            grid.set_placeholder(2, 5, 4, Direction.RIGHTLEFT, 12)
            grid.set_placeholder(2, 10, 5, Direction.DOWNABOVE, 13)
            grid.set_placeholder(3, 0, 4, Direction.RIGHTLEFT, 14)
            grid.set_placeholder(3, 5, 3, Direction.DOWNABOVE, 15)
            grid.set_placeholder(3, 7, 4, Direction.RIGHTLEFT, 16)
            grid.set_placeholder(4, 0, 6, Direction.RIGHTABOVE, 17)
            grid.set_placeholder(4, 2, 9, Direction.RIGHTLEFT, 18)
            grid.set_placeholder(5, 6, 6, Direction.DOWNABOVE, 19)
            grid.set_placeholder(5, 7, 3, Direction.DOWNABOVE, 20)
            grid.set_placeholder(5, 8, 3, Direction.RIGHTLEFT, 21)
            grid.set_placeholder(6, 0, 4, Direction.RIGHTABOVE, 22)
            grid.set_placeholder(6, 2, 5, Direction.DOWNABOVE, 23)
            grid.set_placeholder(6, 3, 5, Direction.RIGHTLEFT, 24)
            grid.set_placeholder(6, 9, 5, Direction.DOWNABOVE, 25)
            grid.set_placeholder(6, 11, 5, Direction.DOWNABOVE, 26)
            grid.set_placeholder(7, 4, 4, Direction.DOWNABOVE, 27)
            grid.set_placeholder(7, 5, 2, Direction.RIGHTLEFT, 28)
            grid.set_placeholder(7, 8, 3, Direction.RIGHTLEFT, 29)
            grid.set_placeholder(8, 0, 7, Direction.RIGHTABOVE, 30)
            grid.set_placeholder(8, 1, 3, Direction.DOWNABOVE, 31)
            grid.set_placeholder(8, 3, 3, Direction.DOWNABOVE, 32)
            grid.set_placeholder(8, 5, 2, Direction.RIGHTLEFT, 33)
            grid.set_placeholder(8, 8, 3, Direction.DOWNABOVE, 34)
            grid.set_placeholder(8, 10, 3, Direction.DOWNABOVE, 35)
            grid.set_placeholder(9, 7, 4, Direction.RIGHTLEFT, 36)
            grid.set_placeholder(10, 0, 4, Direction.RIGHTLEFT, 37)
            grid.set_placeholder(10, 5, 6, Direction.RIGHTLEFT, 38)
            grid.set_placeholder(11, 0, 6, Direction.RIGHTLEFT, 39)
            grid.set_placeholder(11, 7, 4, Direction.RIGHTLEFT, 40)

            return grid
        else:
            print("Error: Layout could not be loaded")
            return CrosswordGridTemplate(0,0)