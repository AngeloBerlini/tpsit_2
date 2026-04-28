#Realizza una pagina web in tecnologia AJAX che consenta di visualizzare il prezzo e le caratteristiche tecniche dei prodotti di un'azienda di informatica.
# La pagina è costituita da un form contenente un campo di
#testo editabile dall'utente. Il campo di testo deve consentire all'utente di inserire il codice identificativo del
#prodotto di interesse. Il codice è costituito da una stringa composta da un carattere alfabetico seguito da
#tre caratteri numerici. Il form inoltre è dotato di un bottone che consente di inviare la request al server; a
#seguito della pressione del bottone la pagina deve:
#a. verificare che il codice identificativo del prodotto immesso dall'utente rispetti il formato specificato;
#b. nel caso in cui il codice identificativo del prodotto verifichi il formato specificato, ti si chiede di inserire
#sotto il form una lista puntata in cui vengano riportati prezzo e caratteristiche del prodotto cercato. Per
#semplicità assumiamo che il prodotto sia sempre presente sul server e che i dati che questi ci restituisce
#siano in formato XML e organizzati come segue:
#
#<? xml version='1.0' encoding='UTF-16'?>
#<prodotto>
#<prezzo> prezzo </prezzo>
#<marca> marca </marca>
#<modello> modello </modello>
#</prodotto>
#
#dove prezzo, marca e modello rappresentano rispettivamente il prezzo del prodotto, la sua marca e il
#suo modello. Le informazioni devono essere richieste al server in modo asincrono tramite una chiamata
#GET e passando il codice del prodotto richiesto;
#c. nel caso in cui il codice identificativo del prodotto non verifichi il formato specificato, ti si chiede che
#venga presentato un pop-up che segnali il problema all'utente.

#flask server
#breve spiegazione di quello che ho fatto: ho creato un server Flask che gestisce le richieste GET per ottenere le informazioni dei prodotti.
#Il server ha una lista di prodotti di esempio indicizzati da un codice identificativo (una lettera seguita da tre cifre).
#Quando viene ricevuta una richiesta con un codice prodotto, il server verifica se il formato del codice è valido e restituisce le informazioni del prodotto in formato JSON.
#Se il codice non è valido o se il prodotto non viene trovato, restituisce un messaggio di errore appropriato.


from flask import Flask, request, jsonify, send_from_directory
import re

# Configura il server Flask con la cartella statica
app = Flask(__name__, static_folder='.')

# Prodotti di esempio (indicizzati dal codice maiuscolo)
SAMPLE_PRODUCTS = {
    'A001': {"prezzo": 1020, "marca": "Dell", "modello": "XPS 13"},
    'A002': {"prezzo": 750, "marca": "Lenovo", "modello": "Thinkercad"},
    'A003': {"prezzo": 499, "marca": "Asus", "modello": "AsusBook"},
    'A067': {"prezzo": 1200, "marca": "Apple", "modello": "MecBuck Bro"}
}


@app.route('/prodotto', methods=['GET'])
def get_prodotto():
    codice = request.args.get('codice', '')

    # Validazione del codice: una lettera seguita da tre cifre
    if not re.match(r'^[A-Za-z]\d{3}$', codice):
        return jsonify({'error': 'Codice non valido'}), 400

    # Converti il codice in maiuscolo per la ricerca
    codice_up = codice.upper()
    prodotto = SAMPLE_PRODUCTS.get(codice_up)
    if prodotto:
        return jsonify(prodotto)
    else:
        return jsonify({'error': 'Prodotto non trovato'}), 404


@app.route('/')
def index():

    # Restituisce la pagina HTML dal server per evitare problemi di CORS (Cross-Origin Resource Sharing)
    return send_from_directory('.', '28_04.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

