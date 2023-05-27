
import socket
import sys 
import os
import threading

def setup_server():
    port = 1234
    # ip = socket.gethostbyname(socket.gethostname())
    ip = "0.0.0.0"
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip,port))
    serverSocket.listen()
    print(f"[LISTENING] Server is listening on {ip}:{port}")
    return serverSocket

def templating_html(html,status,msg):
    new_html = html.replace("{{status}}", status)
    new_html = new_html.replace("{{msg}}", msg)
    return new_html

def handler(server, addr):
    restricted_extension = ['.mp4', '.docx']
    allowable_extension = ['.css', '.jpg', '.txt', '.html', '.png', '.gif', '.pdf', '.xlsx']
    while True:
        req = server.recv(1024).decode('utf-8')
        path = req.split()[1].strip("/")
        print(f"[CONNECTION] {addr[0]}:{addr[1]} accessing: {req.split()[1]}")
        if path == "":
            server.send(b'HTTP/1.1 200 OK\n')
            server.send(b'Content-Type: text/html\n\n')
            server.sendfile(open('./index.html','rb'))
        else:
            isFile = os.path.isfile(path)
            if isFile:
                restricted_status = False
                allowable_status = False
                for i in range(0, len(restricted_extension)):
                    if restricted_extension[i] in path:
                        restricted_status = True
                        break
                for j in range(0, len(allowable_extension)):
                    if allowable_extension[i] in path:
                        allowable_status = True
                        break
                if restricted_status:
                    html = open("error.html", "r").read()
                    html = templating_html(html, "403 Forbidden", "The requested file is unable to access")
                    server.send(b'HTTP/1.1 403 Forbidden\n')
                    server.send(b'Content-Type: text/html\n\n')
                    server.send(html.encode())
                elif allowable_status:
                    server.send(b'HTTP/1.1 200 OK\n')
                    if '.css' in path:
                        server.send(b'Content-Type: text/css\n\n')
                    elif '.jpg' in path:
                        server.send(b'Content-Type: image/jpeg\n\n')
                    elif '.txt' in path:
                        server.send(b'Content-Type: text/plain\n\n')
                    elif '.html' in path:
                        server.send(b'Content-Type: text/html\n\n')
                    elif '.png' in path:
                        server.send(b'Content-Type: image/png\n\n')
                    elif '.gif' in path:
                        server.send(b'Content-Type: image/gif\n\n')
                    elif '.pdf' in path:
                        server.send(b'Content-Type: application/pdf\n\n')
                    elif '.xlsx' in path:
                        server.send(b'Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\n\n')
                    server.sendfile(open(path, 'rb'))
                else:
                    html = open("error.html", 'r').read()
                    html = templating_html(html, "400 Bad Request", "The server is not support the file you requested")
                    server.send(b'HTTP/1.1 400 Bad Request\n')
                    server.send(b'Content-Type: text/html\n\n')
                    server.send(html.encode())
            else:
                html = open("error.html", 'r').read()
                html = templating_html(html, "404 Not Found", "The requested file doesn't exist")
                server.send(b'HTTP/1.1 404 Not Found\n')
                server.send(b'Content-Type: text/html\n\n')
                server.send(html.encode())
        break
    server.close()
    print(f"[CLOSING CONNECTION] {addr[0]}:{addr[1]}")

def main():
    print("[STARTING] Server is starting...")
    serverSocket = setup_server()
    while True:
        server, addr = serverSocket.accept()
        thread = threading.Thread(target=handler, args=(server,addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1} from {addr[0]}:{addr[1]}")

if __name__ == "__main__":
    main()