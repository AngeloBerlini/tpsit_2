import socket
import threading
import time


def worker(thread_id, host="localhost", port=1024, message=None, timeout=5):
    """Worker che apre una connessione, invia un messaggio e riceve la risposta."""
    if message is None:
        message = f"Ciao dal worker {thread_id}"

    try:
        addr = socket.gethostbyname(host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((addr, port))
        print(f"[Worker {thread_id}] Connesso a {addr}:{port}")

        s.sendall(message.encode())

        # Attende risposta
        data = s.recv(4096)
        if data:
            print(f"[Worker {thread_id}] Risposta: {data.decode()}")
        else:
            print(f"[Worker {thread_id}] Nessuna risposta dal server")

    except Exception as e:
        print(f"[Worker {thread_id}] Errore: {e}")
    finally:
        try:
            s.close()
        except Exception:
            pass


def run_concurrent_clients(n=5, host="localhost", port=1024, delay_between=0.1):
    """Lancia n worker in thread separati che si connettono al server contemporaneamente."""
    threads = []
    for i in range(n):
        t = threading.Thread(target=worker, args=(i + 1, host, port, f"Messaggio dal client-thread {i+1}"), daemon=True)
        threads.append(t)
        t.start()
        time.sleep(delay_between)  # piccolo ritardo per variare l'ordine

    for t in threads:
        t.join()


if __name__ == "__main__":
    # Esempio: 5 client concorrenti
    run_concurrent_clients(n=5, host="localhost", port=1024)
