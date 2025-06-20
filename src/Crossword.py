from typing import List, Tuple
from ClueEntry import ClueEntry
from PlaceWord import PlacedWord
from CrosswordGrid import CrosswordGrid


class Crossword:
    def __init__(self, entries: List[ClueEntry]):
        self.entries = entries
        self.grid = CrosswordGrid(12, 12)
        self.clues: List[Tuple[int, str, PlacedWord]] = []  # (number, Frage, Position)

    def generate(self):
        clue_number = 0
        for entry in self.entries:
            placement = self.grid.try_place_word(entry.getAnswer(), clue_number)
            if placement is not None:
                placement.number = clue_number
                self.grid.placed_words.append(placement)
                self.clues.append((clue_number, entry.question, placement))
                clue_number += 1

    def print_crossword(self):
        self.grid.display()
        for num, question, word in self.clues:
            print(f"{num}. ({word.direction}) {question}")
