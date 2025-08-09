from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json

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