import time
import uuid
from socket import *
from a3.message import Message

my_id = uuid.uuid4()
server_name = "localhost"
server_port = 12000

bufferSize = 1024

client_sock = socket(AF_INET, SOCK_STREAM)

while True:
    try:
        client_sock.connect((server_name, server_port))
        msg = Message(my_id).to_json()
        client_sock.send(msg.encode())
    except OSError:
        time.sleep(5)
