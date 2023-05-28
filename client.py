import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.22', 1234))
    while True:
        client.send(b"GET /files/jarkom.html")
        msg = client.recv(1024).decode('utf-8')
        print(msg)

if __name__ == "__main__":
    main()