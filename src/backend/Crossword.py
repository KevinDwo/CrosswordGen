import json
import random
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
        if self.grid.backtracking(0):
            solved_list = self.grid.get_spots()
            self.save_entries_json(solved_list)
            self.save_layout_json()
            # NEU: Lösungswort berechnen und speichern (z.B. Länge 7)
            self.generate_and_save_solution_word(solved_list, num_letters=7)
            print("Eine Lösung wurde gefunden.")
        else:
            print("Es wurde keine Lösung gefunden")

    # NEUE METHODE
    def generate_and_save_solution_word(self, placedwords, num_letters=7):
        # 1. Alle Buchstaben und ihre Koordinaten im Grid sammeln
        available_letters = defaultdict(list)
        for length in placedwords:
            for word in placedwords[length]:
                r = word.get_row()
                c = word.get_col()
                answer = word.get_answer()
                for i in range(word.get_length()):
                    curr_r = r + i if word.get_direction().value == "vertical" else r
                    curr_c = c + i if word.get_direction().value == "horizontal" else c
                    char = answer[i]
                    # Koordinate nur speichern, wenn sie noch nicht für den Buchstaben hinterlegt ist (bei Kreuzungen)
                    if (curr_r, curr_c) not in available_letters[char]:
                        available_letters[char].append((curr_r, curr_c))

        # 2. Ein echtes Wort aus der Datenbank suchen, das aus den verfügbaren Buchstaben gebildet werden kann
        possible_solution_words = []
        if num_letters in self.entries_by_length:
            for entry in self.entries_by_length[num_letters]:
                word = entry.get_answer()
                temp_available = {k: list(v) for k, v in available_letters.items()}
                valid = True
                selected_coords = []
                
                for char in word:
                    if char in temp_available and len(temp_available[char]) > 0:
                        # Eine zufällige Koordinate für diesen Buchstaben wählen
                        coord = random.choice(temp_available[char])
                        temp_available[char].remove(coord)
                        selected_coords.append(coord)
                    else:
                        valid = False
                        break
                        
                if valid:
                    possible_solution_words.append(selected_coords)
        
        # 3. Wenn gültige Wörter gefunden wurden, wähle eines. Sonst Fallback (zufällige Zellen)
        if possible_solution_words:
            final_coords = random.choice(possible_solution_words)
        else:
            all_coords = list(set([coord for coords in available_letters.values() for coord in coords]))
            final_coords = random.sample(all_coords, min(num_letters, len(all_coords)))

        # 4. JSON vorbereiten und speichern
        solution_data = []
        for i, (r, c) in enumerate(final_coords):
            solution_data.append({
                "row": r,
                "col": c,
                "number": i + 1
            })
            
        with open("assets/crossword_solution.json", "w", encoding="utf-8") as f:
            json.dump(solution_data, f, ensure_ascii=False, indent=2)
            
    def display_grid(self):
        self.grid.display()

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