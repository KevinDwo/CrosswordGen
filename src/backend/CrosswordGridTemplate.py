from PlaceWord import PlacedWord
from Direction import Direction
from typing import Dict, List, DefaultDict, Optional, Union
from collections import defaultdict
from ClueEntry import ClueEntry
from utils.Utils import Spot
import random


class CrosswordGridTemplate:
    def __init__(self, rows: int, cols: int):
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.unocupied_spots: DefaultDict[int, List[PlacedWord]] = defaultdict(list)
        self.occupied_spots: DefaultDict[int, List[PlacedWord]] = defaultdict(list)
        self.entries: Dict[int, List[ClueEntry]] 
        self.layout: List[Spot] = []
        self.max_fill_ratio = 0.0
    
    def get_spots(self) -> DefaultDict[int, List[PlacedWord]]:
        return self.occupied_spots

    def get_layout(self) -> List[Spot]:
        return self.layout
    
    def set_entries(self, entries: Dict[int, List[ClueEntry]]):
        new_entries: Dict[int, List[ClueEntry]] = defaultdict(list)
        for length in self.unocupied_spots:
            new_entries[length] = entries[length]
        self.entries = new_entries

    #Loading Layout
    def set_placeholder(self, row: int, col: int, length: int, direction: Direction, number: int) -> bool:
        self.set_layout_spot(row, col, length, direction, number)
        answer = "_" * length
        if self.__can_place_word(answer, row, col, direction):
            new_PlaceWord_values: List[Union[int, Direction]] = self.__place_word(answer, row, col, direction)
            spot = PlacedWord(answer, "?", new_PlaceWord_values[0], new_PlaceWord_values[1], length, new_PlaceWord_values[2], number) # type: ignore
            self.unocupied_spots[length].append(spot)
            return True
        else:
            print(f"Number {number} is false!")
            return False

    def set_layout_spot(self, row: int, col: int, length: int, direction: Direction, number: int):
        spot: Spot = {
            "col": col,
            "row": row,
            "direction": direction.value,
            "length": length,
            "number": number
        }
        self.layout.append(spot)

    def __can_place_word(self, word: str, row: int, col: int, direction: Direction) -> bool:
        if ' ' != self.grid[row][col]:
            print("Arrow overlapses")
            return False

        for i, char in enumerate(word):
            i = i + 1
            match direction:
                case Direction.RIGHTLEFT:
                    r = row
                    c = col + i
                case Direction.RIGHTABOVE:
                    r = row + 1
                    c = col  + i - 1
                case Direction.RIGHTDOWN:
                    r = row - 1
                    c = col + i - 1
                case Direction.DOWNLEFT:
                    r = row + i - 1
                    c = col + 1
                case Direction.DOWNABOVE:
                    r = row + i
                    c = col
                case Direction.DOWNRIGHT:
                    r = row + i -1
                    c = col -1
                case _:
                    raise ValueError("Somethin in can_place went wrong")
            if r >= len(self.grid) or r < 0 or c >= len(self.grid[0]) or c < 0:
                print(f"Index gets out of grid: row = {r} and col = {c}")
                return False
            current = self.grid[r][c]
            if current != ' ' and current != char:
                print("Word overlapses with an arrow")
                return False
        return True
                
    def __place_word(self, word:str, row:int, col:int, direction: Direction) -> List[Union[int, Direction]]:
        match direction:
            case Direction.RIGHTLEFT:
                self.grid[row][col] = "\u2192" # →
                new_values: List[Union[int, Direction]] = [row, col + 1, Direction.HORIZONTAL]
            case Direction.RIGHTABOVE:
                self.grid[row][col] = "\u21B3" # ↳
                new_values: List[Union[int, Direction]] = [row + 1, col, Direction.HORIZONTAL]
            case Direction.RIGHTDOWN:
                self.grid[row][col] = "\u21B1" # ↱
                new_values: List[Union[int, Direction]] = [row - 1, col, Direction.HORIZONTAL]
            case Direction.DOWNLEFT:
                self.grid[row][col] = "\u2B0E" # ⬎
                new_values: List[Union[int, Direction]] = [row, col + 1, Direction.VERTICAL]
            case Direction.DOWNABOVE:
                self.grid[row][col] = "\u2193" # ↓
                new_values: List[Union[int, Direction]] = [row + 1, col, Direction.VERTICAL]
            case Direction.DOWNRIGHT:
                self.grid[row][col] = "\u2B10" # ⬐
                new_values: List[Union[int, Direction]] = [row, col - 1, Direction.VERTICAL]
            case _:
                raise ValueError("Something in place_word went wrong")

        for i, char in enumerate(word):
            i = i + 1
            match direction:
                case Direction.RIGHTLEFT:
                    r = row
                    c = col + i
                case Direction.RIGHTABOVE:
                    r = row + 1
                    c = col  + i - 1
                case Direction.RIGHTDOWN:
                    r = row - 1
                    c = col + i - 1
                case Direction.DOWNLEFT:
                    r = row + i - 1
                    c = col + 1
                case Direction.DOWNABOVE:
                    r = row + i
                    c = col
                case Direction.DOWNRIGHT:
                    r = row + i -1
                    c = col -1
                case _:
                    r = -1
                    c = -1
            self.grid[r][c] = char
        return new_values

    def insert_answer(self, entry: ClueEntry, spot: PlacedWord) -> bool:
        if spot.is_occupied():
            raise ValueError("Tried to insert at an occupied spot")
        if spot.get_length() == len(entry.get_answer()):
            spot.set_answer(entry.get_answer())
            spot.set_question(entry.get_question())
            self.set_spot_occupation(spot, True)
            self.update_all_spots()
            return True
        else:
            print("Answer does not match length")
            return False
    
    def set_spot_occupation(self, spot: PlacedWord, occupation: bool):
        length = spot.get_length()
        spot.set_occupation(occupation)
        if occupation:
            self.unocupied_spots[length].remove(spot)
            self.occupied_spots[length].append(spot)
        else:
            self.occupied_spots[length].remove(spot)
            self.unocupied_spots[length].append(spot)
    
    def update_grid(self, spot: PlacedWord):
        row = spot.get_row()
        col = spot.get_col()
        for i, char in enumerate(spot.get_answer()):
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            self.grid[r][c] = char
    
    # Testing to get a solution
    # Testing to get a solution
    def backtracking(self, words_tried: int) -> bool:
        first_try = False
        if words_tried == 0:
            first_try = True
        if self.crossword_finished():
            return True
        # Current spot
        entries_and_spot = self.get_current_spot()
        # Es gibt mindestens einen Spot, der 0 mögliche entrys hat
        if entries_and_spot == None:
            return False
        entries, spot = entries_and_spot[:2]
        # Über alle spots drüber iterieren und den mit höchstem score auswählen
        for entry in entries:
            self.insert_answer(entry, spot)
            occupied_count = sum(len(spots) for spots in self.occupied_spots.values())
            unoccupied_count = sum(len(spots) for spots in self.unocupied_spots.values())
            total_spots = occupied_count + unoccupied_count
            
            if total_spots > 0:
                current_fill_ratio = occupied_count / total_spots
                
                # Wenn mindestens 85% erreicht sind und es ein neuer Höchststand ist
                if current_fill_ratio >= 0.65 and current_fill_ratio > self.max_fill_ratio:
                    self.max_fill_ratio = current_fill_ratio
                    print(f"\n--- Zwischenstand: Rätsel ist zu {current_fill_ratio * 100:.1f}% gefüllt ---")
                    self.display()
            if first_try:
                total_count = len(entries)
                print(f"{words_tried/total_count * 100:.1f}% done. {total_count - words_tried} trys are still needed. Right now {entry.get_answer()} is tested.")
                words_tried += 1
            # Rekursion
            if self.backtracking(words_tried):
                return True
            else:
                self.revert_spot(spot)
        return False

    def fits_entry_on_spot(self, entry: ClueEntry, spot: PlacedWord) -> bool:
        row = spot.get_row()
        col = spot.get_col()
        word = entry.get_answer()
        
        for i in range(spot.get_length()):
            # Bestimme die aktuelle Zelle im Grid
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            
            grid_char = self.grid[r][c]
            
            # Ist das Feld nicht leer (' ') und nicht der Startmarker ('_') 
            # UND der Buchstabe stimmt nicht mit dem Wort überein?
            if grid_char != ' ' and grid_char != '_' and grid_char != word[i]:
                return False
                
        return True

    # Gibt alle Entries für einen spot in Form einer Liste
    def get_possible_entries(self, entries: List[ClueEntry], spot: PlacedWord) -> List[ClueEntry]:
        possible_insertions: List[ClueEntry] = []
        for entry in entries:
            if self.fits_entry_on_spot(entry, spot):
                possible_insertions.append((entry))
        return possible_insertions

    def crossword_finished(self) -> bool:
        for lenght in list(self.unocupied_spots.keys()):
            for spot in self.unocupied_spots[lenght]:
                if spot.is_occupied():
                    continue
                else:
                    return False
        return True
    
    # Updates all spots to match the current grid
    def update_all_spots(self):
        # Wir aktualisieren nur noch die bereits platzierten Wörter im Grid
        for length in self.occupied_spots.keys():
            for spot in self.occupied_spots[length]:
                if spot.is_occupied():
                    self.update_grid(spot)
                else:
                    raise ValueError("Spot in der falschen Liste (sollte occupied sein)")
        
        # Der rechenintensive Teil für unbesetzte Spots entfällt komplett,
        # da fits_entry_on_spot nun direkt das self.grid liest.
        return True
    
    def revert_spot(self, spot: PlacedWord):

        if spot.is_occupied():
            spot.revert()
            self.set_spot_occupation(spot, False)
            self.update_grid(spot)
            self.update_all_spots()
        else:
            raise ValueError("Tried to revert an unoccupied spot")
        
    def get_current_spot(self) -> Optional[tuple[List[ClueEntry], PlacedWord, int, bool]]:
        entries: List[tuple[List[ClueEntry], PlacedWord, int, bool]] = []
        
        for length in self.unocupied_spots.keys():
            all_words_of_length = self.entries[length] 
            
            for spot in self.unocupied_spots[length]:
                possible_entries = self.get_possible_entries(all_words_of_length, spot)
                random.shuffle(possible_entries)
                number_of_entries = len(possible_entries)
                if number_of_entries == 0:
                    return None
                entries.append((possible_entries, spot, number_of_entries, spot.is_crossed()))
                
        entries.sort(key=lambda x: (not x[3], x[2]))
        return entries[0]

    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))