class PlacedWord:
    def __init__(self, answer: str, row: int, col: int, direction: str, number: int, suitable: bool):
        self._answer = answer
        self._row = row
        self._col = col
        self._direction = direction  # 'across' or 'down'
        self._number = number
        self._suitable = suitable

    # Getter
    def get_answer(self) -> str:
        return self._answer

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def get_direction(self) -> str:
        return self._direction

    def get_number(self) -> int:
        return self._number

    def is_suitable(self) -> bool:
        return self._suitable

    # Setter
    def set_answer(self, answer: str):
        self._answer = answer

    def set_row(self, row: int):
        self._row = row

    def set_col(self, col: int):
        self._col = col

    def set_direction(self, direction: str):
        self._direction = direction

    def set_number(self, number: int):
        self._number = number

    def set_suitable(self, suitable: bool):
        self._suitable = suitable
