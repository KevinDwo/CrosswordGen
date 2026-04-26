import csv
import json
from typing import List

json_file = "/home/dworkevin/Crossword/CrosswordGen/src/backend/assets/crossword_entries.json"
csv_input_file = "/home/dworkevin/Crossword/CrosswordGen/TestQuestions.csv"
csv_output_file = "/home/dworkevin/Crossword/CrosswordGen/TestQuestions_updated.csv"

json_dict = {}
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    
    for entry in json_data:
        frage = entry.get('question') 
        antwort = entry.get('answer')
        
        if frage is not None and antwort is not None:
            # LOGIK-UPDATE: Die Antwort wird zum Key, die Frage zum Value
            json_dict[antwort] = frage

# --- 3. CSV lesen, abgleichen und neu schreiben ---
with open(csv_input_file, 'r', encoding='utf-8') as csv_in, \
     open(csv_output_file, 'w', encoding='utf-8', newline='') as csv_out:
    
    reader = csv.reader(csv_in, delimiter=',')
    writer = csv.writer(csv_out, delimiter=',')
    
    for row in reader:
        # Leere Zeilen überspringen
        if not row or len(row) < 2:
            writer.writerow(row)
            continue
            
        csv_frage = row[0]
        csv_antwort = row[1]
        
        # Wenn die CSV-Antwort als Schlüssel in unserem JSON-Dictionary gefunden wurde:
        if csv_antwort in json_dict:
            # Hol dir die aktualisierte Frage aus dem JSON
            neue_frage = json_dict[csv_antwort]
            writer.writerow([neue_frage, csv_antwort])
        else:
            # Ansonsten die Zeile unverändert lassen
            writer.writerow(row)

print(f"✅ Das Update war erfolgreich! Die Datei {csv_output_file} wurde erstellt.")