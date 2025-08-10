import json
from PlaceWord import PlacedWord
from CrosswordGridLayouts import CrosswordGridLayouts
from typing import DefaultDict, Dict, List
from ClueEntry import ClueEntry
from utils.Utils import Entry

class Crossword:
    def __init__(self, entries_by_length: Dict[int, List[ClueEntry]], layout_number: int):
        self.entries_by_length = entries_by_length
        self.grid = CrosswordGridLayouts.load_layout(layout_number)
        self.layout = self.grid.get_layout()
        
    def solve(self):
        self.grid.set_entries(self.entries_by_length)
        if self.grid.backtracking(1):
            solved_list = self.grid.get_spots()
            self.save_entries_json(solved_list)
            self.save_layout_json()
            print("Eine Lösung wurde gefunden.")
        else:
            print("Es wurde keine Lösung gefunden")

    def convert_to_json(self, placedwords: DefaultDict[int, List[PlacedWord]]) -> List[Entry]:
        entries_json: List[Entry] = []
        for length in placedwords:
            for word in placedwords[length]:

                entry: Entry = {
                    "question": word.get_question(),
                    "answer": word.get_answer(),
                    "row": word.get_row(),
                    "col": word.get_col(),
                    "direction": word.get_direction().value,
                    "number": word.get_number()
                }

                entries_json.append(entry)
        return entries_json
    

    def save_entries_json(self, placedwords: DefaultDict[int, List[PlacedWord]]):
        entries = self.convert_to_json(placedwords)
        with open("assets/crossword_entries.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

    def save_layout_json(self):
        with open("assets/crossword_layout.json", "w", encoding="utf-8") as f:
            json.dump(self.layout, f, ensure_ascii=False, indent=2)