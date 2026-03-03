import socket


class TCPServer:
    def __init__(self, host="localhost", port=1024, buffer_size=1024):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.conn = None
        self.client_address = None

    def start(self, backlog=1):
        """Avvia il server in ascolto (TCP)."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(backlog)
            print(f"Server TCP in ascolto su {self.host}:{self.port}")
        except Exception as e:
            print(f"Errore durante l'avvio del server: {e}")
            self.close()

    def receive_data(self):
        """Accetta (se necessario) e riceve dati dalla connessione client."""
        try:
            if self.socket is None:
                print("Server non avviato")
                return None

            # Accetta una connessione se non ce n'è già una
            if self.conn is None:
                self.conn, self.client_address = self.socket.accept()

            data = self.conn.recv(self.buffer_size)
            if not data:
                return None
            return data.decode(), self.client_address
        except Exception as e:
            print(f"Errore durante la ricezione: {e}")
            return None

    def send_data(self, message):
        """Invia dati al client connesso."""
        try:
            if self.conn is None:
                print("Nessuna connessione al client")
                return False
            self.conn.sendall(message.encode())
            return True
        except Exception as e:
            print(f"Errore durante l'invio: {e}")
            return False

    def close(self):
        """Chiude connessione e socket del server."""
        try:
            if self.conn:
                try:
                    self.conn.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                self.conn.close()
                self.conn = None
            if self.socket:
                self.socket.close()
                self.socket = None
            print("Server TCP chiuso")
        except Exception as e:
            print(f"Errore durante la chiusura: {e}")


if __name__ == "__main__":
    server = TCPServer(host="localhost", port=1024)
    server.start()

    # Ricevi dati da un client
    result = server.receive_data()
    if result:
        message, client_addr = result
        print(f"Messaggio ricevuto da {client_addr}: {message}")

        # Invia risposta
        server.send_data("Messaggio ricevuto dal server!")

    server.close()
