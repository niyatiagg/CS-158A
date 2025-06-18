from socket import *

# Defining the port number the server will listen on
serverPort = 12000

# Defining the buffer size
bufferSize = 64

def receive_data():
    data_recvd = b""
    while len(data_recvd) < msgLen:
        packet = cnSocket.recv(min(bufferSize, msgLen - len(data_recvd)))
        if not packet:
            break
        data_recvd += packet
    return data_recvd

# Creating a TCP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Binding the socket to the local address and specified port
serverSocket.bind(('localhost', serverPort))

# Putting the socket into listening mode (max 1 queued connection at a time)
serverSocket.listen(1)

# Server runs indefinitely to accept incoming connections. Needs to be shut down manually
while True:
    # Accepting an incoming connection, returns a new socket and the client's address
    cnSocket, addr = serverSocket.accept()
    print("Connected from :", addr)

    # Since the first two bytes of the message represent the message length,
    # Receive the first 2 bytes to get message length
    msgLenBytes = cnSocket.recv(2)
    if not msgLenBytes:
        cnSocket.close()
        continue

    msgLen = int(msgLenBytes.decode())
    # Printing relevant information from the message like length of the message
    print("msg_len:", msgLen)

    # Receive the rest of the message based on msg_len
    data = receive_data()
    sentence = data.decode()

    # Printing relevant information from the message like decoded string and actual message length
    print("processed:", sentence)
    print("msg_len_sent:", msgLen)

    # Convert to uppercase and send back
    cnSocket.send(sentence.upper().encode())

    # Close the connection with the client
    cnSocket.close()
    print("Connection closed")