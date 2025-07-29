from CrosswordGridLayouts import CrosswordGridLayouts
from typing import Dict, List
from ClueEntry import ClueEntry

class Crossword:
    def __init__(self, entries_by_length: Dict[int, List[ClueEntry]], layout_number: int):
        self.entries_by_length = entries_by_length
        self.grid = CrosswordGridLayouts.load_layout(layout_number)
        
    def solve(self):
        self.grid.set_spots_list()
        self.grid.set_entries(self.entries_by_length)
        if self.grid.backtracking(0):
            print("Eine Lösung wurde gefunden.")
        else:
            print("Es wurde keine Lösung gefunden")

    def print_crossword(self):
        self.grid.display()