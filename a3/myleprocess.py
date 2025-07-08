import threading
from socket import *
import uuid
from a3.message import Message
import time

class Node:
    highest_uuid = None
    flag = 0
    def __init__(self, my_id: uuid.UUID, server_sock: socket.socket, client_sock: socket.socket, log_file: str ,leader_id : uuid.UUID = None, flag: int = 0):
        self.uuid = my_id
        self.server_sock = server_sock
        self.client_sock = client_sock
        self.log_file = log_file
        self.leader_id = leader_id
        self.flag = flag
        self.highest_uuid = my_id

    def receive_msg(self,msg):
        received_msg = Message.from_json(msg)
        if self.flag == 1: # TODO: Is this to be added??
            with open(self.log_file, 'a') as file:
                file.write(f"Leader is decided to {self.leader_id}, flag=0, greater, 0 \n")
                file.write(f"Received: {received_msg.uuid}, flag=0, greater, 0")
            self.send_msg(Message(self.leader_id, self.flag))
        else:
            if received_msg.flag == 0:
                if received_msg.uuid > self.uuid:
                    with open(self.log_file, 'a') as file:
                        file.write(f"Received: {received_msg.uuid}, flag=0, greater, 0")
                        self.send_msg(msg)
                elif received_msg.uuid < self.uuid:
                    with open(self.log_file, 'a') as file:
                        file.write(f"Received: {received_msg.uuid}, flag=0, less, 0") # No msg is sent
                else:
                    self.highest_uuid = self.uuid
                    self.leader_id = self.uuid
                    self.flag = 1
                    with open(self.log_file, 'a') as file:
                        file.write(f"Received: {received_msg.uuid}, flag=0, same, 0")
                        file.write(f"Leader is decided to {self.leader_id}, flag=0, greater, 0 \n")
                    self.send_msg(Message(self.leader_id, self.flag))
            else:
                self.leader_id = received_msg.uuid


    def send_msg(self, msg) -> None:
        if self.flag == 1:
            self.client_sock.send(msg.encode())
            with open(self.log_file, 'a') as file:
                file.write(f"Sent: {self.leader_id}, flag=1")
        else:
            self.client_sock.send(msg.encode())
            with open(self.log_file, 'a') as file:
                file.write(f"Sent: {msg.uuid}, flag=0")

def le_server(node):
    server_port = 12000

    buffer_size = 1024

    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(('localhost', server_port))

    server_socket.listen(2)

    while True:
        conn_socket, addr = server_socket.accept()
        data = conn_socket.recv(buffer_size)
        Node.receive_msg(data.decode())

def le_client(node):
    my_id = uuid.uuid4()
    server_name = "localhost"
    server_port = 12000

    client_sock = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            client_sock.connect((server_name, server_port))
            break
            # TODO: how to break out of this loop
        except OSError:
            time.sleep(5)

    msg = Message(my_id, 0).to_json()
    Node.send_msg(msg)


if __name__ == "__main__":
    my_id = uuid.uuid4()
    node = Node(my_id, )
    server_th = threading.Thread(target=le_server())
    client_th = threading.Thread(target=le_client())

    server_th.start()
    client_th.start()


