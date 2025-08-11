from Crossword import Crossword
from utils.Utils import Utils
import argparse

def Main():
    parser = argparse.ArgumentParser(description="Crossword Generator")
    parser.add_argument("csv_path", help="Pfad zur CSV-Datei mit Fragen und Antworten")
    args = parser.parse_args()

    entries = Utils.load_csv(args.csv_path)
    Utils.print_number_of_words(entries)
    crossword = Crossword(entries, 3)
    crossword.solve()

if __name__ == "__main__":
    Main()