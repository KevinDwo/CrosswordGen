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
        self.grid_counts = [[0 for _ in range(cols)] for _ in range(rows)]
        self._intersect_cache = {} 
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

        for length in self.unocupied_spots.keys():
            for spot in self.unocupied_spots[length]:
                spot.set_domain(list(self.entries[length]))

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
            
            self.add_word_to_grid(spot) 
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
    
    
    # Testing to get a solution
    def backtracking(self, words_tried: int) -> bool:
        first_try = False
        if words_tried == 0:
            first_try = True
            
        if self.crossword_finished():
            return True
            
        entries_and_spot = self.get_current_spot()
        if entries_and_spot == None:
            return False
            
        entries, spot = entries_and_spot[:2]

        domain_backup = {}
        for length in self.unocupied_spots.keys():
            for s in self.unocupied_spots[length]:
                domain_backup[s] = s.get_domain().copy()
        
        for entry in entries:
            self.insert_answer(entry, spot)
            
            domain_wipeout = False
            for length in self.unocupied_spots.keys():
                for s in self.unocupied_spots[length]:
                    new_domain = s.get_domain().copy()
                    
                    # 1. OPTIMIERUNG: Keine doppelten Wörter zulassen!
                    # Das benutzte Wort wird aus ALLEN anderen freien Spots gestrichen
                    if entry in new_domain:
                        new_domain.remove(entry)

                    # 2. Forward Checking (nur wenn sie sich wirklich kreuzen)
                    if self.intersects(spot, s):
                        new_domain = self.get_possible_entries(new_domain, s)
                        
                    s.set_domain(new_domain)
                    
                    if len(new_domain) == 0:
                        domain_wipeout = True
                        break
                if domain_wipeout:
                    break
            
            occupied_count = sum(len(spots) for spots in self.occupied_spots.values())
            unoccupied_count = sum(len(spots) for spots in self.unocupied_spots.values())
            total_spots = occupied_count + unoccupied_count
            
            if total_spots > 0:
                current_fill_ratio = occupied_count / total_spots
                if current_fill_ratio >= 0.85 and current_fill_ratio > self.max_fill_ratio:
                    self.max_fill_ratio = current_fill_ratio
                    print(f"\n--- Zwischenstand: Rätsel ist zu {current_fill_ratio * 100:.1f}% gefüllt ---")
                    self.display()
                    
            if first_try:
                total_count = len(entries)
                print(f"{words_tried/total_count * 100:.1f}% done. Right now {entry.get_answer()} is tested.")
                words_tried += 1
                
            # Rekursion NUR fortsetzen, wenn das Forward-Checking erfolgreich war
            if not domain_wipeout:
                if self.backtracking(words_tried):
                    return True
                    
            # Wenn es hier ankommt, war der Pfad falsch -> Wort wieder entfernen
            self.revert_spot(spot)
            
            for s, backup in domain_backup.items():
                if not s.is_occupied():
                    s.set_domain(backup.copy())
            
        return False

    def fits_entry_on_spot(self, entry: ClueEntry, spot: PlacedWord) -> bool:
        row = spot.get_row()
        col = spot.get_col()
        word = entry.get_answer()
        
        for i in range(spot.get_length()):
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            
            grid_char = self.grid[r][c]
            
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
    
    
    def revert_spot(self, spot: PlacedWord):
        if spot.is_occupied():
            self.remove_word_from_grid(spot)
            spot.revert()
            self.set_spot_occupation(spot, False)
        
    def get_current_spot(self) -> Optional[tuple[List[ClueEntry], PlacedWord, int, bool]]:
        entries: List[tuple[List[ClueEntry], PlacedWord, int, bool]] = []
        
        for length in self.unocupied_spots.keys():
            for spot in self.unocupied_spots[length]:
                possible_entries = spot.get_domain()
                number_of_entries = len(possible_entries)
                
                if number_of_entries == 0:
                    return None
                entries.append((possible_entries, spot, number_of_entries, spot.is_crossed()))
        
        if not entries:
            return None
                
        # Sortiere nach MRV (wenigste verbleibende Möglichkeiten zuerst)
        entries.sort(key=lambda x: (not x[3], x[2]))
        
        # NEU: Nur die Liste für den WIRKLICH ausgewählten Spot mischen!
        best_match = entries[0]
        shuffled_domain = best_match[0].copy()
        random.shuffle(shuffled_domain)
        
        return (shuffled_domain, best_match[1], best_match[2], best_match[3])

    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))

    def add_word_to_grid(self, spot: PlacedWord):
        row = spot.get_row()
        col = spot.get_col()
        for i, char in enumerate(spot.get_answer()):
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            
            self.grid[r][c] = char
            self.grid_counts[r][c] += 1  # Zähler erhöhen

    def remove_word_from_grid(self, spot: PlacedWord):
        row = spot.get_row()
        col = spot.get_col()
        for i in range(spot.get_length()):
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            
            self.grid_counts[r][c] -= 1  # Zähler verringern
            
            # Nur löschen, wenn KEIN anderes Wort mehr diesen Buchstaben nutzt!
            if self.grid_counts[r][c] == 0:
                self.grid[r][c] = '_'

    def intersects(self, spot1: PlacedWord, spot2: PlacedWord) -> bool:
        # Wir erzeugen einen einzigartigen Key für dieses Spot-Paar
        key = frozenset([id(spot1), id(spot2)])
        
        # Wenn wir die Antwort schon kennen, sofort aus dem Cache laden (Millisekunden!)
        if key in self._intersect_cache:
            return self._intersect_cache[key]
            
        r1, c1 = spot1.get_row(), spot1.get_col()
        r2, c2 = spot2.get_row(), spot2.get_col()
        
        cells1 = set()
        for i in range(spot1.get_length()):
            r = r1 + i if spot1.get_direction() == Direction.VERTICAL else r1
            c = c1 + i if spot1.get_direction() == Direction.HORIZONTAL else c1
            cells1.add((r, c))
            
        cells2 = set()
        for i in range(spot2.get_length()):
            r = r2 + i if spot2.get_direction() == Direction.VERTICAL else r2
            c = c2 + i if spot2.get_direction() == Direction.HORIZONTAL else c2
            cells2.add((r, c))
            
        result = bool(cells1 & cells2)
        # Ergebnis im Cache für die Zukunft speichern
        self._intersect_cache[key] = result
        return result