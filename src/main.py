from Crossword import Crossword
from Utils import Utils

def Main():
    entries = Utils.load_csv("/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions.csv")
    crossword = Crossword(entries, 1)
    crossword.solve()

if __name__ == "__main__":
    Main()