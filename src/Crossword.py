from typing import List, Tuple
from ClueEntry import ClueEntry
from PlaceWord import PlacedWord
from CrosswordGrid import CrosswordGrid, Direction


class Crossword:
    def __init__(self, entries: List[ClueEntry]):
        self.entries = entries
        self.grid = CrosswordGrid(12, 12)
        self.clues: List[Tuple[int, str, PlacedWord]] = []  # (number, Frage, Position)
        self.words = []
        for word in self.entries:
            self.words.append(word.getAnswer())

    def solve(self) -> bool:
        self.grid.place_word(self.words[0], 0, 0, Direction.DOWN)
        first_pos = self.grid.find_all_positions(self.words[1])[0]
        print(first_pos)
        self.grid.place_word(self.words[1], 0, 5, Direction.RIGHT)
        return True

    def print_crossword(self):
        self.grid.display()
        for num, question, word in self.clues:
            print(f"{num}. ({word.get_direction()}) {question}")
