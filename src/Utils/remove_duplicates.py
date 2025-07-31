import csv
from typing import List

input_file = "/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions.csv"
output_file = "/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions.csv"

unique_entries: set[str] = set()
cleaned_rows: List[List[str]] = []

# Read and remove duplicates
with open(input_file, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    cleaned_rows.append(header)

    for row in reader:
        answer_lower = row[1].lower()
        if answer_lower not in unique_entries:
            unique_entries.add(answer_lower)
            cleaned_rows.append(row)

# Write new file
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(cleaned_rows)

print(f"Bereinigte Datei wurde erstellt: {output_file}")