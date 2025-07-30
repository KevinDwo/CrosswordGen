from collections import defaultdict
import csv
from ClueEntry import ClueEntry
from typing import List, Dict

class Utils:

    @staticmethod
    def load_csv(path: str):
        entries_by_length: Dict[int, List[ClueEntry]] = defaultdict(list)
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entry = ClueEntry(row['questions'], row['answers'])
                entries_by_length[len(entry.get_answer())].append(entry)
        return entries_by_length
    @staticmethod
    def print_number_of_words(entries: Dict[int, List[ClueEntry]]):
        sorted_entries = dict(sorted(entries.items(), key=lambda item: item[0]))
        total: int = 0
        for length in sorted_entries.keys():
            current_number = len(sorted_entries[length])
            if length > 9:
                break
            total += current_number
            print(f"Länge {length} hat {current_number} Wörter")
        print(f"In total we use {total} words.")
    
    @staticmethod
    def get_words_by_length(entries: Dict[int, List[ClueEntry]], length: int):
        for word in entries[length]:
            print(word.get_answer())