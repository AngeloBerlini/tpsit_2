import socket


class TCPClient:
    def __init__(self, host="localhost", port=1024):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self, timeout=None):
        """Crea il socket TCP e si connette al server."""
        try:
            addr = socket.gethostbyname(self.host)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if timeout is not None:
                self.socket.settimeout(timeout)
            self.socket.connect((addr, self.port))
            print(f"Client TCP connesso a {addr}:{self.port}")
            return True
        except Exception as e:
            print(f"Errore durante la connessione del client: {e}")
            self.socket = None
            return False

    def send_data(self, message):
        """Invia dati al server (blocking)."""
        try:
            if self.socket is None:
                print("Client non connesso")
                return False
            self.socket.sendall(message.encode())
            return True
        except Exception as e:
            print(f"Errore durante l'invio: {e}")
            return False

    def receive_data(self, buffer_size=1024):
        """Riceve dati dal server; ritorna stringa o None."""
        try:
            if self.socket is None:
                print("Client non connesso")
                return None
            data = self.socket.recv(buffer_size)
            if not data:
                return None
            return data.decode()
        except Exception as e:
            print(f"Errore durante la ricezione: {e}")
            return None

    def close(self):
        """Chiude il client"""
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
            print("Client TCP chiuso")
        except Exception as e:
            print(f"Errore durante la chiusura: {e}")


if __name__ == "__main__":
    client = TCPClient(host="localhost", port=1024)
    if client.connect():
        client.send_data("Ciao, server!")
        response = client.receive_data()
        if response:
            print(f"Messaggio ricevuto dal server: {response}")
        client.close()
