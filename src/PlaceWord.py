class PlacedWord:
    def __init__(self, answer: str, row: int, col: int, direction: str, number: int):
        self.answer = answer
        self.row = row
        self.col = col
        self.direction = direction  # 'across' or 'down'
        self.number = number        # z. B. 1, 2, 3 …
