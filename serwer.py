import socket
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Serwer UDP działa na porcie {UDP_PORT}")

# =============================
#  Tabela klientów:
#  { (ip,port): {"id": 0, "last_msg": "...", "last_seen": czas} }
# =============================
clients = {}
next_id = 1


def register_client(addr):
    global next_id

    clients[addr] = {
        "id": next_id,
        "last_msg": "",
        "last_seen": time.time()
    }

    print(f"[NOWY KLIENT] {addr} → ID={next_id}")
    next_id += 1


while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    # Rejestracja nowego klienta
    if addr not in clients:
        register_client(addr)

    # Aktualizacja danych klienta
    clients[addr]["last_msg"] = message
    clients[addr]["last_seen"] = time.time()

    print(f"[KLIENT {clients[addr]['id']}] {addr} → {message}")

    # Wysyłanie odpowiedzi tylko do nadawcy
    reply = f"OK, klient {clients[addr]['id']} — odebrano: {message}"
    sock.sendto(reply.encode(), addr)

    # DEBUG: lista klientów
    print("\n--- AKTYWNI KLIENCI ---")
    for c_addr, info in clients.items():
        print(f"ID {info['id']} | IP {c_addr[0]}:{c_addr[1]} | MSG: {info['last_msg']}")
    print("------------------------\n")
