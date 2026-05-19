
from flask import Flask, request, jsonify, render_template
import json, os, re

app = Flask(__name__)
JSON_FILE = 'users.json'

def load_users():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(JSON_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def validate_user(data):
    if not re.match(r"^[A-Za-zÀ-ÿ\s]{2,30}$", data.get('nome', '')):
        return False
    if not re.match(r"^[A-Za-zÀ-ÿ\s]{2,30}$", data.get('cognome', '')):
        return False
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", data.get('data_nascita', '')):
        return False
    if not re.match(r"^[A-Za-zÀ-ÿ\s]{2,50}$", data.get('mansione', '')):
        return False
    return True

@app.route('/')
@app.route('/gestionale_utenti/')
def home():
    return render_template('index.html')

@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(load_users()), 200
    if request.method == 'POST':
        data = request.get_json()
        if not data or not validate_user(data):
            return jsonify({'errore': 'Dati non validi'}), 400
        users = load_users()
        new_id = max((u['id'] for u in users), default=0) + 1
        new_user = {
            'id': new_id,
            'nome': data['nome'],
            'cognome': data['cognome'],
            'data_nascita': data['data_nascita'],
            'mansione': data['mansione']
        }
        users.append(new_user)
        save_users(users)
        return jsonify(new_user), 201
    return jsonify({'errore': 'Metodo non consentito'}), 405

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(id):
    if not re.match(r'^\d+$', id):
        return jsonify({'errore': 'ID non valido'}), 400
    id = int(id)
    users = load_users()
    user = next((u for u in users if u['id'] == id), None)
    if user is None:
        return jsonify({'errore': 'Utente non trovato'}), 404
    if request.method == 'GET':
        return jsonify(user), 200
    if request.method == 'PUT':
        data = request.get_json()
        if not data or not validate_user(data):
            return jsonify({'errore': 'Dati non validi'}), 400
        user.update({
            'nome': data['nome'],
            'cognome': data['cognome'],
            'data_nascita': data['data_nascita'],
            'mansione': data['mansione']
        })
        save_users(users)
        return jsonify(user), 200
    if request.method == 'DELETE':
        users.remove(user)
        save_users(users)
        return jsonify({'messaggio': 'Utente eliminato'}), 200
    return jsonify({'errore': 'Metodo non consentito'}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5000)
