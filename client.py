import socket


class UDPClient:
    def __init__(self, host="localhost", port=1024):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.socket = None
        self.server_address = (self.host, self.port)

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Client UDP pronto per comunicare con {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"Errore durante la preparazione del client: {e}")
            return False

    def send_data(self, message):
        """Invia dati al server"""
        try:
            if self.socket is None:
                print("Client non preparato")
                return False
            
            self.socket.sendto(message.encode(), self.server_address)
            return True
            
        except Exception as e:
            print(f"Errore durante l'invio: {e}")
            return False

    def receive_data(self, buffer_size=1024):
        """Riceve dati dal server"""
        try:
            if self.socket is None:
                print("Client non preparato")
                return None
            
            data, server_addr = self.socket.recvfrom(buffer_size)
            return data.decode()
            
        except Exception as e:
            print(f"Errore durante la ricezione: {e}")
            return None

    def close(self):
        """Chiude il client"""
        try:
            if self.socket:
                self.socket.close()
            print("Client UDP chiuso")
        except Exception as e:
            print(f"Errore durante la chiusura: {e}")


if __name__ == "__main__":
    client = UDPClient(host="localhost", port=1024)
    
    if client.connect():
        # Invia messaggio al server
        client.send_data("Ciao, server!")
        
        # Ricevi risposta dal server
        response = client.receive_data()
        if response:
            print(f"Messaggio ricevuto dal server: {response}")
        
        client.close()
