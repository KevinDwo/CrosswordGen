# Crossword Generator 🧩

**🌍 Live Demo:** [Hier das generierte Rätsel spielen!](https://crosswordgen-8zzw.onrender.com/)

Ein Python-basiertes Full-Stack-Projekt zur automatischen Generierung und interaktiven Lösung von Kreuzworträtseln. 

Dieses Projekt wurde entwickelt, um komplexe algorithmische Herausforderungen (Constraint Satisfaction, Backtracking) mit einer sauberen objektorientierten Architektur (OOP) und einer modernen Client-Server-Struktur zu verbinden. Aus einer flexiblen CSV-Wortliste berechnet das Backend gültige Rätsel-Layouts und stellt diese über eine REST-API einem interaktiven Web-Frontend zur Verfügung.

## 📸 Screenshot

Hier ist eine Vorschau des generierten, interaktiven Kreuzworträtsels: ![Screenshot](assets/website_screenshot.png)

## 🚀 Features

* **Algorithmische Rätselgenerierung:** Automatisches Platzieren von Wörtern basierend auf vorgegebenen Grid-Layouts mittels eines optimierten Backtracking-Algorithmus.
* **Intelligente Kollisionsprüfung:** Effiziente Vorab-Filterung (Domain Filtering) und Caching von Schnittpunkten für performante Berechnungen.
* **REST-API:** Bereitstellung der generierten Rätseldaten (Layout und Einträge) über ein Flask-Backend.
* **Interaktives Frontend:** Ein responsives, per CSS-Grid aufgebautes Web-Interface mit Vanilla JavaScript. Unterstützt Tastaturnavigation (Pfeiltasten), dynamische Wort-Hervorhebung und Echtzeit-Validierung.
* **Datenverarbeitung:** Automatisierte Bereinigung und Deduplizierung der initialen CSV-Fragendatenbank.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Flask-CORS
* **Frontend:** HTML5, CSS3 (CSS Grid), Vanilla JavaScript (ES6+)
* **Architektur:** Objektorientierte Programmierung (OOP), MVC-inspirierte Trennung von Logik und Darstellung, RESTful API.

## 🧠 Under the Hood: Der Algorithmus

Die größte Herausforderung dieses Projekts ist die korrekte und performante Platzierung der Wörter. Das Backend löst dies als **Constraint Satisfaction Problem (CSP)**:
1. **Domain Filtering:** Für jeden freien Platz im Raster wird vorab ermittelt, welche Wörter aus der Datenbank basierend auf der Länge und bereits gekreuzten Buchstaben überhaupt in Frage kommen.
2. **Backtracking:** Der Algorithmus probiert rekursiv Wörter aus. Führt ein Pfad in eine Sackgasse (Wipeout der Domain eines verbleibenden Platzes), wird der Zustand sauber zurückgerollt (`revert_spot`).
3. **Optimierung:** Zur Beschleunigung der Kollisionsprüfung wurde ein Caching-Mechanismus (`_intersect_cache`) implementiert, der einmal berechnete Schnittpunkte zwischen Platzhaltern speichert.

## 📂 Projektstruktur

```text
CrosswordGen/
├── src/
│   ├── backend/
│   │   ├── main.py                 # CLI Entry-Point für die Rätsel-Generierung
│   │   ├── website.py              # Flask Webserver & REST-API
│   │   ├── Crossword.py            # Hauptsteuerung der Generierung
│   │   ├── CrosswordGridTemplate.py# Grid-Logik & Backtracking-Algorithmus
│   │   ├── PlaceWord.py, ClueEntry.py # OOP-Datenmodelle
│   │   ├── assets/                 # Generierte JSON-Ergebnisse
│   │   └── utils/                  # CSV-Parsing & Duplikat-Entfernung
│   └── frontend/
│       └── templates/
│           └── website.html        # Interaktives Web-Interface
├── TestQuestions.csv               # Rohdaten (Fragen & Antworten)
└── requirements.txt                # Python-Abhängigkeiten