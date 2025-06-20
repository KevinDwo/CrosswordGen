from typing import List, Optional
from PlaceWord import PlacedWord

class CrosswordGrid:
    def __init__(self, rows: int, cols: int):
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.placed_words: List[PlacedWord] = []

    def try_place_word(self, word: str, number: int) -> Optional[PlacedWord]:
        row = 0
        col = 0

        # Einfügen ins Grid (horizontal)
        for i, letter in enumerate(word):
            self.grid[row][col + i] = letter

        # Dummy-Rückgabe fürs Testen
        return PlacedWord(word, row, col, "across", number)

    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))
