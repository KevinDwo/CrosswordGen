from Crossword import Crossword
from Utils import Utils

def Main():
    entries = Utils.load_csv("../TestQuestions.csv")
    crossword = Crossword(entries)
    crossword.solve()
    crossword.print_crossword()

if __name__ == "__main__":
    Main()