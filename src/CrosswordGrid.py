from typing import List, Optional
from PlaceWord import PlacedWord

class CrosswordGrid:
    def __init__(self, rows: int, cols: int):
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    def try_place_word(self, word: str, number: int) -> Optional[PlacedWord]:
        rows = len(self.grid)
        cols = len(self.grid[0])
        length = len(word)
        best_position = None
        best_overlap = -1
        
        def count_overlap_and_fits(row, col, direction):
            overlap = 0
            for i, letter in enumerate(word):
                r, c = (row, col + i) if direction == "across" else (row + i, col)
                cell = self.grid[r][c]
                if cell != ' ' and cell != letter:
                    return -1 
                if cell == letter:
                    overlap += 1
            return overlap
        
        # horizontal
        for row in range(rows):
            for col in range(cols - length + 1):
                overlap = count_overlap_and_fits(row, col, "across")
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_position = ("across", row, col)
                    
        # vertical
        for col in range(cols):
            for row in range(rows - length + 1):
                overlap = count_overlap_and_fits(row, col, "down")
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_position = ("down", row, col)

        if best_position:
            direction, row, col = best_position
            for i, letter in enumerate(word):
                r, c = (row, col + i) if direction == "across" else (row + i, col)
                self.grid[r][c] = letter
            return PlacedWord(word, row, col, direction, number, True)

        return None  # Kein gültiger Platz



    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))
