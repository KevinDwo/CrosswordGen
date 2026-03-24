from Crossword import Crossword
from utils.Utils import Utils
import argparse

def Main():
    parser = argparse.ArgumentParser(description="Crossword Generator")
    parser.add_argument("csv_path", help="Pfad zur CSV-Datei mit Fragen und Antworten")
    args = parser.parse_args()

    entries = Utils.load_csv(args.csv_path)
    Utils.print_number_of_words(entries)
    number_of_layouts = 5  
    amount_of_trys = 100
    for _ in range(amount_of_trys):
        for current_layout in range(number_of_layouts):
            print(f"Layout {current_layout + 1} von {number_of_layouts}:")
            crossword = Crossword(entries, 1)
            crossword.solve()

if __name__ == "__main__":
    Main()