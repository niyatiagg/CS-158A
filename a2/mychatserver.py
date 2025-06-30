from socket import *
import threading

# Defining the port number the server will listen on
serverPort = 12000

# Defining the buffer size
bufferSize = 1024

# Create a dictionary to store each client's port number against their
# connection socket
clients = {}

# Function that handles messages from clients
def worker_bee(port_num, conn_socket):
    # Starting a sending thread for sending messages
    while True:
        data = conn_socket.recv(bufferSize)
        message = data.decode()
        if message == 'exit':
            conn_socket.send("exit".encode())
            conn_socket.close()
            clients.pop(port_num)
            print("Connection closed")
            break

        # Printing the message with their port number
        print(f"{port_num}:{message}")

        # Creating a message that runs on
        message_to_be_sent = f"{port_num}:{message}"
        for pt_num in clients.keys():
            if pt_num == port_num:
                continue
            else :
                clients[pt_num].send(message_to_be_sent.encode())

# Creating a TCP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Binding the socket to the local address and specified port
serverSocket.bind(('localhost', serverPort))

# Putting the socket into listening mode
serverSocket.listen(10)
print(f"Server listening on {serverSocket.getsockname()[0]}:{serverSocket.getsockname()[1]}")

# Server runs indefinitely to accept incoming connections. Needs to be shut down manually
while True:
    try:
    # Accepting an incoming connection, returns a new socket and the client's address
        cnSocket, addr = serverSocket.accept()
        ip_addr, port_number = addr
        print("New connection from :", addr)
        clients[port_number] = cnSocket

        # Assigning a new 'worker' thread to each incoming client to send and receive messages
        th = threading.Thread(target=worker_bee, args=(port_number, cnSocket))
        th.start()
    except KeyboardInterrupt:
        break

# Closing all the client sockets and then the server socket
for p_num in clients.keys():
    clients[p_num].close()
serverSocket.close()
