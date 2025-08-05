from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='../Frontend/templates')
CORS(app)

data = {
    "0": "H",
    "1": "A",
    "2": "L",
    "3": "L",
    "4": "O"
}

@app.route('/')
def index():
    return render_template('website.html')

@app.route('/api/data')
def get_data():
    return jsonify(data)

app.run(debug=True)