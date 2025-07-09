import threading
import sys
from socket import *
import uuid
from message import Message
import time

# Maintaining global state of the node
client_socket = socket(AF_INET, SOCK_STREAM)
my_id = uuid.uuid4()
highest_id = my_id
flag = 0

# Comparing UUIDs and returning their status
def compare(a,b):
    if a > b:
        return 'greater'
    elif b > a:
        return 'less'
    return 'same'

# Receiving and processing messages
def receive_msg(received_msg):
    global flag, highest_id, my_id
    with open(log_file, 'a') as file:
        file.write(f"Received: {received_msg.uuid}, flag={received_msg.flag}, {compare(received_msg.uuid, my_id)}, {flag}\n")

    # This is the final state of the leader
    if flag == 1 and my_id == highest_id:
        print(f"I am the Leader with id: {highest_id}")
    else:
        # When node with the highest UUID receives its own UUID and declares itself leader
        if received_msg.flag == 0 and received_msg.uuid == highest_id:
            with open(log_file, 'a') as file:
                file.write(f"Leader is decided to {highest_id}\n")
            flag = 1
            send_msg(Message(highest_id, flag))

        # When sending node has a higher UUID
        elif received_msg.flag == 0 and received_msg.uuid > highest_id:
            highest_id = received_msg.uuid
            send_msg(received_msg)

        # When sending node has a lower UUID
        elif received_msg.flag == 1:
            with open(log_file, 'a') as file:
                file.write(f"Leader is decided to {highest_id}\n")
            print(f"Leader is {highest_id}")
            flag = 1
            send_msg(Message(highest_id, flag))

# Sending messages to respective servers
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

# The server function for the node
def le_server(saddress, sport):
    buffer_size = 1024

    # Creating a TCP server socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((saddress, sport))
    server_socket.listen(2)
    conn_socket, addr = server_socket.accept()

    while True:
        # Checking for end of message descriptor
        buff = ""
        while not buff.endswith('\n'):
            buff += conn_socket.recv(buffer_size).decode()
        msg = Message.from_json(buff.strip())
        receive_msg(msg)

# The client function for the node
def le_client(caddress, cport):
    global client_socket

    # Creating a TCP client socket
    while True:
        try:
            client_socket.connect((caddress, cport))
            print(f"Client connected:  {(caddress, cport)}")
            break
        except ConnectionRefusedError:
            # Retrying if the corresponding server is still not up
            print("Connection refused, retrying...")
            client_socket = socket(AF_INET, SOCK_STREAM)
            time.sleep(2)

    send_msg(Message(my_id, 0))


if __name__ == "__main__":
    # Reading the server and client IP address and port number from different config files each with the number provided on console
    file_suffix = ""
    if len(sys.argv) == 2:
        file_suffix = sys.argv[1]
    config_file = "config" + file_suffix + ".txt"

    # Log file for each node
    log_file = "log" + file_suffix + ".txt"
    with open(config_file, 'r') as f:
        server = f.readline().strip().split(',')
        client = f.readline().strip().split(',')

    # Assigning a server to a new thread
    server_th = threading.Thread(target=le_server, args=(server[0], int(server[1])))

    # Assigning a client to a new thread
    client_th = threading.Thread(target=le_client, args=(client[0], int(client[1])))

    # Starting server thread
    server_th.start()

    # Starting client thread
    client_th.start()