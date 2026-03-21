from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder='../frontend/templates')
CORS(app)

with open("assets/crossword_entries.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

with open("assets/crossword_layout.json", "r", encoding="utf-8") as f:
    layout = json.load(f)

@app.route('/')
def index():
    return render_template('website.html')

@app.route('/api/entries')
def get_entries():
    return jsonify(entries)

@app.route('/api/layout')
def get_layout():
    return jsonify(layout)

app.run(debug=True)


if __name__ == '__main__':
    # Render weist dynamisch einen Port zu. Wenn wir lokal testen, nehmen wir 5000.
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' ist wichtig, damit der Server von außen erreichbar ist
    app.run(host='0.0.0.0', port=port)