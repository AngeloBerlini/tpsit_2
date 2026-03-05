import socket
import threading
import datetime


class ThreadedTCPServer:
    """Server TCP che gestisce ogni client in un thread separato."""

    def __init__(self, host="localhost", port=1024, buffer_size=1024):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self._is_running = False

    def start(self, backlog=5):
        """Avvia il server e loop di accept che crea thread per ogni client."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permette il riutilizzo rapido dell'indirizzo durante lo sviluppo
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(backlog)
            self._is_running = True
            print(f"Server multithread in ascolto su {self.host}:{self.port}")

            while self._is_running:
                try:
                    conn, addr = self.socket.accept()
                except OSError:
                    break
                t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                t.start()

        except Exception as e:
            print(f"Errore durante l'avvio del server: {e}")
            self.close()

    def handle_client(self, conn, addr):
        """Gestisce la comunicazione con un singolo client in un thread separato."""
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Connessione da {addr}")
        try:
            with conn:
                while True:
                    data = conn.recv(self.buffer_size)
                    if not data:
                        break
                    text = data.decode(errors='replace')
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{thread_name}] Ricevuto da {addr} alle {now}: {text}")

                    # Risposta: echo con info thread e timestamp
                    reply = f"[{thread_name} @ {now}] Ho ricevuto: {text}"
                    try:
                        conn.sendall(reply.encode())
                    except Exception as e:
                        print(f"[{thread_name}] Errore invio a {addr}: {e}")
                        break
        except Exception as e:
            print(f"[{thread_name}] Errore nella gestione client {addr}: {e}")
        finally:
            print(f"[{thread_name}] Connessione chiusa {addr}")

    def close(self):
        """Chiude il socket del server."""
        self._is_running = False
        try:
            if self.socket:
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                self.socket.close()
                self.socket = None
            print("Server multithread chiuso")
        except Exception as e:
            print(f"Errore durante la chiusura: {e}")


if __name__ == "__main__":
    server = ThreadedTCPServer(host="localhost", port=1024)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Ricevuto KeyboardInterrupt, arresto server...")
    finally:
        server.close()
