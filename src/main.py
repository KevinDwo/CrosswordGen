from Crossword import Crossword
from Utils import Utils

def Main():
    entries = Utils.load_csv("../../Questions.csv")
    puzzle = Crossword(entries)
    puzzle.generate()
    puzzle.print_crossword()

if __name__ == "__main__":
    Main()


# 40 Einträge