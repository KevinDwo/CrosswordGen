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