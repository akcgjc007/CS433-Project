import time
import socket
from utils import *
from getpass import getpass

HOST = "localhost"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to Server")

while True:
    conn, addr = client_socket.recvfrom(1024*64)

    conn = conn.decode('utf-8')

    if (conn == "Thanks for using Mini Tweet!"):
        print(conn)
        break
    elif(conn == "Enter your username and password:"):
        print(conn)
        username = bytes(str(input()), 'utf-8')
        password = encrypt(getpass(), 4)
        client_socket.send(username)
        client_socket.send(bytes(password, 'utf-8'))
    else:
        print(conn)

        response = bytes(str(input()), 'utf-8')

        client_socket.send(response)

client_socket.close()
print('Connection closed!')
