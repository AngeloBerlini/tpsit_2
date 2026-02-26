import socket


class UDPServer:
    def __init__(self, host="localhost", port=1024, buffer_size=1024):
        
        self.host = socket.gethostbyname(host)
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.client_address = None

    def start(self):
        """Avvia il server in ascolto"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
            print(f"Server UDP in ascolto su {self.host}:{self.port}")
            
        except Exception as e:
            print(f"Errore durante l'avvio del server: {e}")
            self.close()

    def receive_data(self):
        """Riceve dati da un client"""
        try:
            if self.socket is None:
                print("Server non avviato")
                return None
            
            data, self.client_address = self.socket.recvfrom(self.buffer_size)
            return data.decode(), self.client_address
            
        except Exception as e:
            print(f"Errore durante la ricezione: {e}")
            return None

    def send_data(self, message, address=None):
        """Invia dati a un client"""
        try:
            if self.socket is None:
                print("Server non avviato")
                return False
            
            # Se non specifici un indirizzo, usa l'ultimo client che ha inviato
            target_address = address if address else self.client_address
            
            if target_address is None:
                print("Indirizzo del client non specificato")
                return False
            
            self.socket.sendto(message.encode(), target_address)
            return True
            
        except Exception as e:
            print(f"Errore durante l'invio: {e}")
            return False

    def close(self):
        """Chiude il server"""
        try:
            if self.socket:
                self.socket.close()
            print("Server UDP chiuso")
        except Exception as e:
            print(f"Errore durante la chiusura: {e}")


if __name__ == "__main__":
    server = UDPServer(host="localhost", port=1024)
    server.start()
    
    # Ricevi dati da un client
    result = server.receive_data()
    if result:
        message, client_addr = result
        print(f"Messaggio ricevuto da {client_addr}: {message}")
        
        # Invia risposta
        server.send_data("Messaggio ricevuto dal server!", client_addr)
    
    server.close()
