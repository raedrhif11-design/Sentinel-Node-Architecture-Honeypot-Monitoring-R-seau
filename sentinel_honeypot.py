import datetime
import json
import logging
import socket
import threading

LOG_FILE = "sentinel_attacks.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def log_incident(src_ip, src_port, banner_req, raw_data):
    """Enregistre l'intrusion détectée au format JSON dans le fichier de logs."""
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "src_ip": src_ip,
        "src_port": src_port,
        "service_targeted": banner_req,
        "payload_length": len(raw_data),
        "raw_payload": raw_data[:200].decode('latin1', errors='replace')
    }
    logging.info(json.dumps(event))
    print(f"[🚨 ALERTE INTRUSION] Attaque interceptée depuis {src_ip}:{src_port} sur {banner_req}")

def handle_client(client_socket, client_address, port_service):
    src_ip, src_port = client_address
    try:
        # Fausse bannière de service (leurre)
        if port_service == 2222:
            client_socket.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
        elif port_service == 8080:
            client_socket.send(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\n\r\n<h1>It works!</h1>")

        data = client_socket.recv(1024)
        if data:
            service_name = "SSH_SIMULATED" if port_service == 2222 else "HTTP_SIMULATED"
            log_incident(src_ip, src_port, service_name, data)
    except Exception as e:
        pass
    finally:
        client_socket.close()

def start_listener(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"[*] Sonde Honeypot active sur le port {port}...")
        while True:
            client_socket, client_address = server.accept()
            t = threading.Thread(target=handle_client, args=(client_socket, client_address, port))
            t.daemon = True
            t.start()
    except Exception as err:
        print(f"[!] Erreur sur port {port}: {err}")

def main():
    print("=" * 60)
    print(" 🛡️ SENTINEL-NODE : HONEYPOT & MONITORING D'INTRUSIONS")
    print("=" * 60)
    # Simulation de surveillance sur port 2222 (faux SSH) et 8080 (faux HTTP)
    ports = [2222, 8080]
    threads = []
    for p in ports:
        th = threading.Thread(target=start_listener, args=(p,))
        th.daemon = True
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Arrêt des sondes Sentinel-Node.")
