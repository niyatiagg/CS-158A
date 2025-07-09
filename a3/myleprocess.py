import threading
import sys
from socket import *
import uuid
from message import Message
import time

client_socket = socket(AF_INET, SOCK_STREAM)
my_id = uuid.uuid4()
highest_id = my_id
flag = 0

def compare(a,b):
    if a > b:
        return 'greater'
    elif b > a:
        return 'less'
    return 'same'

def receive_msg(received_msg):
    global flag, highest_id, my_id
    with open(log_file, 'a') as file:
        file.write(f"Received: {received_msg.uuid}, flag={received_msg.flag}, {compare(received_msg.uuid, my_id)}, {flag}\n")

    if flag == 1 and my_id == highest_id:
        print(f"I am the Leader with id: {highest_id}")
    else:
        if received_msg.flag == 0 and received_msg.uuid == highest_id:
            with open(log_file, 'a') as file:
                file.write(f"Leader is decided to {highest_id}\n")
            flag = 1
            send_msg(Message(highest_id, flag))
        elif received_msg.flag == 0 and received_msg.uuid > highest_id:
            highest_id = received_msg.uuid
            send_msg(received_msg)
        elif received_msg.flag == 1:
            with open(log_file, 'a') as file:
                file.write(f"Leader is decided to {highest_id}\n")
            print(f"Leader is {highest_id}")
            flag = 1
            send_msg(Message(highest_id, flag))


def send_msg(msg):
    global client_socket, flag, highest_id
    while True:
        try:
            client_socket.send(msg.to_json().encode())
            break
        except (OSError, ConnectionResetError, BrokenPipeError):
            time.sleep(2)

    with open(log_file, 'a') as file:
        file.write(f"Sent: {msg.uuid}, flag={msg.flag}\n")


def le_server(saddress, sport):
    buffer_size = 1024
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((saddress, sport))
    server_socket.listen(2)
    conn_socket, addr = server_socket.accept()

    while True:
        buff = ""
        while not buff.endswith('\n'):
            buff += conn_socket.recv(buffer_size).decode()
        msg = Message.from_json(buff.strip())
        receive_msg(msg)

def le_client(caddress, cport):
    global client_socket

    while True:
        try:
            client_socket.connect((caddress, cport))
            print(f"Client connected:  {(caddress, cport)}")
            break
        except ConnectionRefusedError:
            print("Connection refused, retrying...")
            client_socket = socket(AF_INET, SOCK_STREAM)
            time.sleep(2)

    send_msg(Message(my_id, 0))


if __name__ == "__main__":
    file_suffix = ""
    if len(sys.argv) == 2:
        file_suffix = sys.argv[1]
    config_file = "config" + file_suffix + ".txt"
    log_file = "log" + file_suffix + ".txt"
    with open(config_file, 'r') as f:
        server = f.readline().strip().split(',')
        client = f.readline().strip().split(',')
    server_th = threading.Thread(target=le_server, args=(server[0], int(server[1])))
    client_th = threading.Thread(target=le_client, args=(client[0], int(client[1])))

    server_th.start()
    client_th.start()