
import socket
import os
import threading

#function untuk inisiasi server
def setup_server():
    port = 1234 #set port ke 1234
    # ip = socket.gethostbyname(socket.gethostname())
    ip = "0.0.0.0" #set ip address ke 0.0.0.0 (ipv4 wifi)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket servernya
    serverSocket.bind((ip,port)) #hubungkan server dengan address yang telah ditentukan
    serverSocket.listen() #server listening ke address
    print(f"[LISTENING] Server is listening on {ip}:{port}") #Informasi tentang listening servernya
    return serverSocket #mengembalikan data serversoccketnya

#function untuk templating html yang berguna untuk customize file html sesuai dengan status
def templating_html(html,status,msg):
    new_html = html.replace("{{status}}", status) #setiap ada {{status}} diganti dengan isi dari parameter status
    new_html = new_html.replace("{{msg}}", msg) #setiap ada {{msg}} diganti dengan isi atau value dari parameter msg
    return new_html #mengembalikan string html yang telah dimodifikasi

#function untuk menghandle setiap koneksi
def handler(server, addr):
    restricted_extension = ['.mp4', '.docx'] #menentukan ekstensi mana saja yang dilarang
    allowable_extension = ['.css', '.jpg', '.txt', '.html', '.png', '.gif', '.pdf', '.xlsx'] #menentukan ekstensi manasaja yang diperbolehkan
    while True: #looping untuk koneksi yang diminta
        req = server.recv(1024).decode('utf-8') #parsing request dari client
        path = req.split()[1].strip("/") #mendapatkan url yang diakses oleh client
        print(f"[CONNECTION] {addr[0]}:{addr[1]} accessing: {req.split()[1]}") #memberikan informasi tentang client
        if path == "": #membuat statement kalau urlnya adalah /
            server.send(b'HTTP/1.1 200 OK\n') #set status 200 OK
            server.send(b'Content-Type: text/html\n\n') #set tipe konten text/html
            server.sendfile(open('./index.html','rb')) #memberikan file index.html dengan tehnik read dan kontennya diubah ke bytes
        else: #selain urlnya "/" maka
            isFile = os.path.isfile(path) #mengecek apakah file terdapat pada server
            if isFile: #kalau file ada pada server maka
                restricted_status = False #inisiasi status restricted
                allowable_status = False #inisiasi status allowable
                for i in range(0, len(restricted_extension)): #melakukan loop seluruh array restricted_extension
                    if restricted_extension[i] in path: #apakah elemen dari array restricted_extension tersebut terdapat pada url
                        restricted_status = True #set status restricted menjadi true
                        break #berhentikan looping jika file yang diminta client dilarang oleh server
                for j in range(0, len(allowable_extension)): #lakukan loop seluruh array allowable_extension
                    if allowable_extension[j] in path: #apakah file yang diminta oleh klien merupakan file yang diizinkan oleh server
                        allowable_status = True #set status allowable menjadi true
                        break #berhentikan looping jika file tersebut merupakan file yang diizinkan oleh server
                if restricted_status:#kalau restricted_status true
                    html = open("error.html", "r").read() #membuka file error.html dan membacanya
                    html = templating_html(html, "403 Forbidden", "The requested file is unable to access") #panggil function templating_html dengan argumen status kode dan penjelasan dari status kode tersebut
                    server.send(b'HTTP/1.1 403 Forbidden\n') #set status header menjadi 403 forbidden
                    server.send(b'Content-Type: text/html\n\n') #set content type text/html
                    server.send(html.encode()) #encode string html dan berikan ke client
                elif allowable_status: #kalau file tersebut diizinkan oleh server
                    server.send(b'HTTP/1.1 200 OK\n') #set status menjadi 200 OK
                    if '.css' in path: #kalau ekstensi file client adalah css
                        server.send(b'Content-Type: text/css\n\n') #set content type menjadi text/css
                    elif '.jpg' in path:#kalau ekstensi file client adalah jpg
                        server.send(b'Content-Type: image/jpeg\n\n') #set content type menjadi image/jpeg
                    elif '.txt' in path:#kalau ekstensi file client adalah txt
                        server.send(b'Content-Type: text/plain\n\n')#set content type text/plain
                    elif '.html' in path: #kalau ekstensi file client adalah html
                        server.send(b'Content-Type: text/html\n\n') #set content type text/html
                    elif '.png' in path: #kalau ekstensi file client adalah png
                        server.send(b'Content-Type: image/png\n\n') #set content type image/png
                    elif '.gif' in path: #kalau ekstensi file client adalah gif
                        server.send(b'Content-Type: image/gif\n\n') #set content type image/gif
                    elif '.pdf' in path:#kalau ekstensi file client adalah pdf
                        server.send(b'Content-Type: application/pdf\n\n') #set content type application/pdf
                    elif '.xlsx' in path:#kalau ekstensi file client adalah xlsx
                        server.send(b'Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\n\n') #set content type sesuai dengan mime type dari microsoft excel 
                    server.sendfile(open(path, 'rb')) #membuka file yang diminta oleh client di server dengan tehnik membaca dan konten dari filenya diubah ke bytes dan dikiriman ke client
                else:#kalau file tersebut tidak disupport oleh server
                    html = open("error.html", 'r').read() #membuka file error.html dan membacanya
                    html = templating_html(html, "400 Bad Request", "The server is not support the file you requested") #memanggil function templating_html dengan argumennya 400 Bad Reqeust dan penjelasan dari status tersebut
                    server.send(b'HTTP/1.1 400 Bad Request\n') #set status menjadi 400 Bad Request
                    server.send(b'Content-Type: text/html\n\n') #set content type menjadi text/html
                    server.send(html.encode()) #server mengirim string html yang telah diencode
            else: #jika file tidak terdapat pada server
                html = open("error.html", 'r').read() #membuka file error.html dan membacanya
                html = templating_html(html, "404 Not Found", "The requested file doesn't exist") #memanggil function templating_html dengan status kode 404 Not Found dengan deskripsinya
                server.send(b'HTTP/1.1 404 Not Found\n') #set status menjadi 404 Not Found
                server.send(b'Content-Type: text/html\n\n') #set content type menjadi text/html
                server.send(html.encode()) #server memberikan string html dengan diencode
        break #stop looping apabila file yang diminta oleh client telah terpenuhi
    server.close() #tutup koneksi
    print(f"[CLOSING CONNECTION] {addr[0]}:{addr[1]}") #memberikan informasi kalau koneksi tersebut telah ditutup

#function ini dijalankan ketika file main.py (file ini) dirun
def main():
    print("[STARTING] Server is starting...") #memberikan informasi kalau servernya sedang dijalankan
    serverSocket = setup_server() #memanggil function setup_server untuk inisiasi server
    while True: #looping untuk server listening ke address
        server, addr = serverSocket.accept() #menerima koneksi dari client
        thread = threading.Thread(target=handler, args=(server,addr)) #membuat threading dan melempar ke function handler dengan argumen server dan addr
        thread.start() #thread yang tadi telah dibuat dijalankan
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1} from {addr[0]}:{addr[1]}") #memberikan informasi tentang koneksi yang aktif berapa dan dari address mana

if __name__ == "__main__": #jika isi dari variable __name__ (bawaan python)
    main() #maka function main dijalankan