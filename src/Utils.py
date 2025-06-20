import csv
from ClueEntry import ClueEntry
class Utils:
    def __init__(self):
        pass

    def load_csv(path: str):
        entries = []
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entries.append(ClueEntry(row['questions'], row['answers']))
        return entries