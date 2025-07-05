import socket
import uuid
from a3.client import client_sock
from a3.message import Message


class Node:

    def __init__(self, my_id: uuid.UUID, server_sock: socket.socket, client_sock: socket.socket, log_file: str ,leader_id : uuid.UUID = None, flag: int = 0):
        self.uuid = my_id
        self.server_sock = server_sock
        self.client_sock = client_sock
        self.log_file = log_file
        self.leader_id = leader_id
        self.flag = flag

    def receive_msg(self,msg):
        received_msg = Message.from_json(msg)
        if self.flag == 1: # TODO: Is this to be added??
            with open(self.log_file, 'a') as file:
                file.write(f"Leader is decided to {self.leader_id}, flag=0, greater, 0 \n")
                file.write(f"Received: {received_msg.uuid}, flag=0, greater, 0")
            return
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
                    self.leader_id = self.uuid
                    self.flag = 1
                    with open(self.log_file, 'a') as file:
                        file.write(f"Leader is decided to {self.leader_id}, flag=0, greater, 0 \n")
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




