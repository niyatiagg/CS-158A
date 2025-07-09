import threading
import sys
from socket import *
import uuid
from a3.message import Message
import time

client_socket = None
my_id = uuid.uuid4()
highest_id = my_id
flag = 0

def receive_msg(msg):
    global flag, highest_id, my_id
    received_msg = Message.from_json(msg)
    if flag == 1: # TODO: Is this to be added? is this correct
        with open(log_file, 'a') as file:
            file.write(f"Received: {received_msg.uuid}, flag=0, greater, 0\n")
    else:
        if received_msg.flag == 0:
            if received_msg.uuid > highest_id:
                highest_id = received_msg.uuid
                with open(log_file, 'a') as file:
                    file.write(f"Received: {received_msg.uuid}, flag=0, greater, 0\n")
                    send_msg(msg)
            elif received_msg.uuid < highest_id:
                with open(log_file, 'a') as file:
                    file.write(f"Received: {received_msg.uuid}, flag=0, less, 0\n") # No msg is sent
            else:
                flag = 1
                with open(log_file, 'a') as file:
                    file.write(f"Received: {highest_id}, flag=0, same, 0\n")
                    file.write(f"Leader is decided to {highest_id}, flag=0, greater, 0 \n")
                send_msg(Message(highest_id, flag))
        else:
            flag = 1
            with open(log_file, 'a') as file:
                file.write(f"Received: {highest_id}, flag=0, same, 0\n")
                file.write(f"Leader is decided to {highest_id}, flag=0, greater, 0 \n")
            print(f"Leader is {highest_id}")
            send_msg(Message(highest_id, flag))


def send_msg(msg):
    global client_socket, flag, highest_id
    while client_socket is None:
        time.sleep(2)
    client_socket.send(msg.encode())
    with open(log_file, 'a') as file:
        file.write(f"Sent: {highest_id}, flag={flag}")


def le_server(server_tup):
    buffer_size = 1024

    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(server_tup)

    server_socket.listen(2)

    while True:
        conn_socket, addr = server_socket.accept()
        buff = ""
        while not buff.endswith('\n'):
            buff += conn_socket.recv(buffer_size).decode()
        msg = Message.from_json(buff.strip())
        receive_msg(msg.decode())

def le_client(client_tup):
    global client_socket

    client_socket = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            client_socket.connect(client_tup)
            break
        except OSError:
            time.sleep(10)

    send_msg(Message(highest_id, flag).to_json())


if __name__ == "__main__":
    file_suffix = ""
    if len(sys.argv) == 2:
        file_suffix = sys.argv[1]
    config_file = "config" + file_suffix + ".txt"
    log_file = "log" + file_suffix + ".txt"
    with open(config_file, 'r') as f:
        server_tuple = tuple(f.readline().strip().split(','))
        client_tuple = tuple(f.readline().strip().split(','))
    server_th = threading.Thread(target=le_server(), args=server_tuple)
    client_th = threading.Thread(target=le_client(), args=client_tuple)

    server_th.start()
    client_th.start()


