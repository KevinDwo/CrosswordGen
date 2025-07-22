from typing import List, Optional, Tuple
from PlaceWord import PlacedWord

class CrosswordGrid:
    def __init__(self, rows: int, cols: int):
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.arrow_down = '\u2193'
        self.arrow_right = '\u2192'
        
    def evaluate_position(start_row, start_col, direction):
        pass

    def find_all_positions(self, word):
        positions = []
        for direction in Direction:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    if self.can_place_word(word, row, col, direction):
                        positions.append((row, col, direction))
        return positions


    def can_place_word(self, word, row, col, direction) -> bool:
        for i, char in enumerate(word):
            r = row + i if direction == Direction.RIGHT else row
            c = col + i if direction == Direction.DOWN else col

            if r >= len(self.grid) or c >= len(self.grid[0]):
                return False
            current = self.grid[r][c]
            if current != ' ' and current != char:
                return False
        return True

    def place_word(self, word:str, row:int, col:int, direction):
        
        for i, char in enumerate(word):
            r = row + i if direction == Direction.DOWN else row
            c = col + i if direction == Direction.RIGHT else col
            self.grid[r][c] = char

    def remove_word(self, word, row, col, direction):
        for i in range(len(word)):
            r = row + i if direction == Direction.DOWN else row
            c = col + i if direction == Direction.RIGHT else col
            self.grid[r][c] = ' '


    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))


from enum import Enum

class Direction(Enum):
    RIGHT = 0
    DOWN = 1