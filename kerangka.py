#import modul socket
from socket import *
import sys # Import modul sys untuk terminasi program

#Inisiasi Server Socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8888
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
while True:
    #Membuat koneksi
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        #Membaca data request dari client
        message = connectionSocket.recv(1024)
        #Mengambil data filenama dari url
        filename = message.split()[1].decode("utf-8").strip("/")
        #Membuka file berdasarkan variable filename sebelumnya
        f = open(filename)
        #membaca konten file
        outputdata = f.read()
        #menutup program dibelakang layar yang membuka file tersebut
        f.close()
        #Set header dengan kode status 200 
        response_line = "HTTP/1.0 200 OK\r\n"
        connectionSocket.send(response_line.encode())
        #Set tipe konten agar konten responsenya selalu menampilkan html bukan text
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        #Memberikan seluruh konten yang sebelumnya telah dibaca ke client melalui response
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        #Menutup koneksi soket client
        connectionSocket.close()

    except IOError:
    #Send pesan error apabila terdapat error dengan atribut 'IOError'
        connectionSocket.send('HTTP/1.0 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>')
    #Menutup koneksi soket
    connectionSocket.close()
    #Fill in end
    #Menutup server soket
    serverSocket.close()
    #Terminasi program
    sys.exit()