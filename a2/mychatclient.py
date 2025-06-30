from socket import *
import threading

# Defining the server name and port number to connect to
serverName = "localhost"
serverPort = 12000

# Defining the buffer size
bufferSize = 1024

# Defining the receiving function
def receiving_messages(c_socket):
    while True:
        response = c_socket.recv(bufferSize).decode()
        if response:
            if response == "exit":
                break
            else:
                print(f"\n{response}")

# Defining the sending function
def sending_messages(c_socket):
    while True:
        sentence = input()
        c_socket.send(sentence.encode())
        # Check if the client want to close the socket connection
        if sentence == "exit":
            receiving_thread.join()
            break

#Creating a TCP socket and establishing a connection to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print("Connected to chat server. Type 'exit' to leave.")

# Starting a sending thread for sending messages
sending_thread = threading.Thread(target=sending_messages, args=(clientSocket,))
sending_thread.start()

# Starting a receiving thread for receiving messages from other clients
receiving_thread = threading.Thread(target=receiving_messages, args=(clientSocket,))
receiving_thread.start()

sending_thread.join()

clientSocket.close()
#receiving_thread.join()
print("Disconnected from server")



