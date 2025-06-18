from socket import *

# Defining the server name and port number to connect to
serverName = "localhost"
serverPort = 12000

# Defining the buffer size
bufferSize = 64

#Creating a TCP socket and establishing a connection to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Encoding the user-input lowercase sentence and sending it to the server
sentence = input("Input lowercase sentence:")
clientSocket.send(sentence.encode())

# Receiving the response from the server and printing the decoded message
response = b""
while True:
    part = clientSocket.recv(bufferSize)
    if not part:
        break
    response += part
print("From Server:", response.decode())

# Closing the socket connection
clientSocket.close()