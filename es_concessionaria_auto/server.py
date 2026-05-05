#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path.startswith('/api/filtra'):
            self.filtra_auto()
        else:
            self.send_error(404)
    
    def serve_html(self):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
        except:
            self.send_error(404)
    
    def filtra_auto(self):
        try:
            # Estrai i parametri
            params = parse_qs(urlparse(self.path).query)
            marca = params.get('marca', [''])[0].lower().strip()
            modello = params.get('modello', [''])[0].lower().strip()
            alimentazione = params.get('alimentazione', [''])[0].lower().strip()
            colore = params.get('colore', [''])[0].lower().strip()
            
            # Carica le auto
            with open('auto.json', 'r', encoding='utf-8') as f:
                auto = json.load(f)
            
            # Filtra
            risultati = []
            for car in auto:
                if marca and car['marca'].lower() != marca:
                    continue
                if modello and car['modello'].lower() != modello:
                    continue
                if alimentazione and car['alimentazione'].lower() != alimentazione:
                    continue
                if colore and car['colore'].lower() != colore:
                    continue
                risultati.append(car)
            
            # Restituisci JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(risultati, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500)
    
    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('', 8000), Handler)
    print("Server su http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStop")
        server.server_close()
