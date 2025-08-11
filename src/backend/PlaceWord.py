from Direction import Direction
class PlacedWord:
    def __init__(self, answer: str, question: str, row: int, col: int, length: int, direction: Direction, number: int):
        self._answer = answer
        self._question = question
        self._row = row
        self._col = col
        self._direction = direction
        self._number = number
        self._length = length
        self._occupied: bool = False
        self._cross: bool = False
    
    # Getter
    def get_answer(self) -> str:
        return self._answer

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def get_direction(self) -> Direction:
        return self._direction

    def get_number(self) -> int:
        return self._number

    def get_question(self) -> str:
        return self._question

    def get_length(self) -> int:
        return self._length
    
    def is_occupied(self) -> bool:
        return self._occupied

    def is_crossed(self) -> bool:
        return self._cross
    # Setter
    def set_answer(self, answer: str):
        self._answer = answer

    def set_row(self, row: int):
        self._row = row

    def set_col(self, col: int):
        self._col = col

    def set_direction(self, direction: Direction):
        self._direction = direction

    def set_number(self, number: int):
        self._number = number

    def set_question(self, question: str):
        self._question = question

    def set_length(self, length: int):
        self._length = length
    
    def set_occupation(self, occupation: bool):
        self._occupied = occupation

    def set_crossed(self, crossed: bool):
        self._cross = crossed

    def revert(self):
        self.set_answer("_" * self.get_length())
        self.set_question("?")
        self.set_crossed(False)