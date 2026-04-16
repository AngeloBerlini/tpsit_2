from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'comuni.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/cerca')
def cerca():
    q = request.args.get('q', '').strip()
    if len(q) == 0:
        return jsonify([])
    conn = get_db()
    rows = conn.execute(
        "SELECT name, lat, lng, codice_provincia_istat FROM comuni WHERE name LIKE ? ORDER BY name LIMIT 50",
        (q + '%',)
    ).fetchall()
    conn.close()
    risultati = [{'nome': r['name'], 'lat': r['lat'], 'lng': r['lng'], 'prov': r['codice_provincia_istat']} for r in rows]
    return jsonify(risultati)

if __name__ == '__main__':
    app.run(debug=True, port=5050)