from socket import *
from a3.node import Node

server_port = 12000

bufferSize = 1024

def le_server(node):
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(server_port)

    server_socket.listen(2)

    while True:
        conn_socket, addr = server_socket.accept()
        data = conn_socket.recv(1024)

