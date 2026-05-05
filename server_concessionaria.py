# ...existing code...
from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# carica il file JSON relativo al file corrente
DATA_FILE = os.path.join(os.path.dirname(__file__), 'auto.json')
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    auto_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cerca', methods=['POST'])
def cerca_auto():
    dati = request.get_json() or {}
    # leggere valori; considera stringhe vuote come "no filtro"
    marca = dati.get('marca')
    modello = dati.get('modello')
    alimentazione = dati.get('alimentazione')
    colore = dati.get('colore')

    def match(field_value, filtro):
        if filtro is None or filtro == "":
            return True
        if field_value is None:
            return False
        return str(field_value).lower() == str(filtro).lower()

    auto_filtrate = [
        auto for auto in auto_data
        if match(auto.get('marca'), marca)
        and match(auto.get('modello'), modello)
        and match(auto.get('alimentazione'), alimentazione)
        and match(auto.get('colore'), colore)
    ]

    return jsonify(auto_filtrate)

if __name__ == '__main__':
    # in produzione togli debug=True
    app.run(host='127.0.0.1', port=5000, debug=True)