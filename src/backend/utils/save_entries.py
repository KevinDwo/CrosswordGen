import csv
import json
from typing import List

json_file = "/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/src/backend/assets/crossword_entries.json"
csv_input_file = "/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions.csv"
csv_output_file = "/mnt/e/Programmier-Aufgaben/Crossword/CrosswordGen/TestQuestions_updated.csv"

json_dict = {}
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    
    for entry in json_data:
        frage = entry.get('question') 
        antwort = entry.get('answer')
        
        if frage is not None and antwort is not None:
            # Beide Seiten vereinheitlichen (alles in Großbuchstaben umwandeln)
            # .strip() entfernt zusätzlich mögliche unsichtbare Leerzeichen
            json_dict[antwort.strip().upper()] = frage

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
        
        # Die CSV-Antwort für den Abgleich ebenfalls in Großbuchstaben umwandeln
        csv_antwort_check = csv_antwort.strip().upper()
        
        # Wenn die CSV-Antwort als Schlüssel in unserem JSON-Dictionary gefunden wurde:
        if csv_antwort_check in json_dict:
            # Hol dir die aktualisierte Frage aus dem JSON
            neue_frage = json_dict[csv_antwort_check]
            # Wir schreiben die neue Frage, aber behalten die originale Schreibweise der CSV-Antwort bei
            writer.writerow([neue_frage, csv_antwort])
        else:
            # Ansonsten die Zeile unverändert lassen
            writer.writerow(row)

print(f"✅ Das Update war erfolgreich! Die Datei {csv_output_file} wurde erstellt.")