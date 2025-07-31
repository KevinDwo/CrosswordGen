from Crossword import Crossword
from Utils.Utils import Utils

def Main():
    entries = Utils.load_csv("/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions.csv")
    Utils.print_number_of_words(entries)
    #Utils.get_words_by_length(entries, 2)
    crossword = Crossword(entries, 2)
    crossword.solve()

if __name__ == "__main__":
    Main()