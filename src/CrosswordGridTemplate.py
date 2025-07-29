from PlaceWord import PlacedWord
from Direction import Direction
from typing import Dict, List, DefaultDict, Union
from collections import defaultdict
from ClueEntry import ClueEntry

class CrosswordGridTemplate:
    def __init__(self, rows: int, cols: int):
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.open_spots_by_length: DefaultDict[int, List[PlacedWord]] = defaultdict(list)
        self.occupied_spots: DefaultDict[int, List[PlacedWord]] = defaultdict(list)
        self.spots_sorted: List[PlacedWord] = []
        self.entries: Dict[int, List[ClueEntry]] 
    
    def set_spots_list(self):
        spots_sorted: List[PlacedWord] = []
        for length in sorted(self.open_spots_by_length.keys(), reverse=True):
            for spot in self.open_spots_by_length[length]:
                spots_sorted.append(spot)
        self.spots_sorted = spots_sorted
 
    def set_entries(self, entries: Dict[int, List[ClueEntry]]):
        self.entries = entries

    #Loading Layout
    def set_placeholder(self, row: int, col: int, length: int, direction: Direction, number: int) -> bool:
        answer = "_" * length
        if self.__can_place_word(answer, row, col, direction):
            new_PlaceWord_values: List[Union[int, Direction]] = self.__place_word(answer, row, col, direction)
            spot = PlacedWord(answer, "?", new_PlaceWord_values[0], new_PlaceWord_values[1], length, new_PlaceWord_values[2], number) # type: ignore
            self.open_spots_by_length[length].append(spot)
            return True
        else:
            print(f"Number {number} is false!")
            return False


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
                print("Index gets out of grid")
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
            self.update_grid(spot)
            self.update_all_spots()
            #self.display()
            return True
        else:
            print("Answer is too long/short")
            return False
    
    def set_spot_occupation(self, spot: PlacedWord, occupation: bool):
        length = spot.get_length()
        spot.set_occupation(occupation)
        if occupation:
            self.open_spots_by_length[length].remove(spot)
            self.occupied_spots[length].append(spot)
        else:
            self.occupied_spots[length].remove(spot)
            self.open_spots_by_length[length].append(spot)

    def update_grid(self, spot: PlacedWord):
        row = spot.get_row()
        col = spot.get_col()
        for i, char in enumerate(spot.get_answer()):
            r = row + i if spot.get_direction() == Direction.VERTICAL else row
            c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
            self.grid[r][c] = char
    
    # Testing to get a solution
    def backtracking(self, depth: int) -> bool:
        depth = depth
        spot = self.spots_sorted[depth]
        length = spot.get_length()
        if self.crossword_finished():
            self.display()
            return True
        # Entries = Alle entries mit mindestens einem spot
        entries = self.get_all_possible_entries(length)
        if not entries:
            print(f"Ebene {depth} hat keine möglichen entrys mehr.")
            return False

        possible_insertions = self.get_possible_entries(entries, spot)

        # Über alle spots drüber iterieren und den mit höchstem score auswählen
        for insertion in possible_insertions:
            self.insert_answer(insertion[0], insertion[1])
            print(f"In Ebene {depth} wurde {insertion[0].get_answer()} inserted")

            
            # Rekursion
            if self.backtracking(depth + 1):
                return True
            else:
                self.revert_spot(insertion[1])
                print(f"In Ebene {depth} wurde die Antowrt {insertion[0].get_answer()} zu {insertion[1].get_answer()} reverted.")
        return False
    
    # Gibt eine Liste an entries, die an mind. einem spot passen
    def get_all_possible_entries(self, length: int) -> List[ClueEntry]:
        entries_copy: List[ClueEntry] = []
        for entry in self.entries[length]:
            if self.is_entry_possible(entry, length):
                entries_copy.append(entry)
        return entries_copy

    # Testet einen entry, ob er in irgendeinen spot passt, sonst false
    def is_entry_possible(self, entry: ClueEntry, length: int):
        for spot in self.open_spots_by_length[length]:
            if self.fits_entry_on_spot(entry, spot):
                return True
        return False

    # Must be same length
    def fits_entry_on_spot(self, entry: ClueEntry, spot: PlacedWord) -> bool:
        for i, char in enumerate(spot.get_answer()):
            if char != "_" and char != entry.get_answer()[i]:
                    return False
        return True
    
    def get_possible_entries(self, entries: List[ClueEntry], spot: PlacedWord) -> List[tuple[ClueEntry, PlacedWord, float]]:
        possible_insertions: List[tuple[ClueEntry, PlacedWord, float]] = []
        for entry in entries:
            if self.fits_entry_on_spot(entry, spot):
                score = self.calculate_score(entry, spot)
                possible_insertions.append((entry, spot, score))
        #Höchster score zuerst 
        possible_insertions.sort(key=lambda x: x[2], reverse=True)
        return possible_insertions

    def calculate_score(self, entry: ClueEntry, spot: PlacedWord) -> float:
        score: float = 0.0
        for i, char in enumerate(spot.get_answer()):
            if char == entry.get_answer()[i]:
                    score += 1
        return score
    def crossword_finished(self) -> bool:
        for lenght in list(self.open_spots_by_length.keys()):
            for spot in self.open_spots_by_length[lenght]:
                if spot.is_occupied():
                    continue
                else:
                    return False
        return True
    
    # Updates all spots answers to match the current grid
    def update_all_spots(self):
        for lenght in list(self.occupied_spots.keys()):
            for spot in self.occupied_spots[lenght]:
                if spot.is_occupied():
                    self.update_grid(spot)
                else:
                    raise ValueError("Spot in the false list")

        for lenght in list(self.open_spots_by_length.keys()):
            for spot in self.open_spots_by_length[lenght]:
                if not spot.is_occupied():
                    current_answer = ""
                    row = spot.get_row()
                    col = spot.get_col()
                    for i in range(spot.get_length()):
                        r = row + i if spot.get_direction() == Direction.VERTICAL else row
                        c = col + i if spot.get_direction() == Direction.HORIZONTAL else col
                        current_answer = current_answer + self.grid[r][c]
                    spot.set_answer(current_answer)
                else:
                    raise ValueError("Spot in the fals list")
        return True
    
    def revert_spot(self, spot: PlacedWord):

        if spot.is_occupied():
            spot.revert()
            self.set_spot_occupation(spot, False)
            self.update_grid(spot)
            self.update_all_spots()
            #self.display()
        else:
            raise ValueError("Tried to revert an unoccupied spot")
        

    def display(self):
        for row in self.grid:
            print(' '.join(c if c != ' ' else '.' for c in row))