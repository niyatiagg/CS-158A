import socket, ssl

def main():
    # Defining the host (in our case: google.com) and port number (in our case: 443)
    host_name = "www.google.com"
    port_number = 443

    # Creating a plain TCP socket and connect
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect((host_name, port_number))

    # Wrapping socket with SSL context
    context = ssl.create_default_context()
    ssl_sock = context.wrap_socket(c_sock, server_hostname=host_name)

    # Preparing and sending HTTP GET request
    request = f"GET / HTTP/1.1\r\nHost: {host_name}\r\nConnection: close\r\n\r\n"
    ssl_sock.sendall(request.encode())

    # Receiving full HTTP response
    response = ''
    #with open('response.html', 'a') as file:
    while True:
        data = ssl_sock.recv(1024)
        if not data:
            break
        response += data.decode()
        #file.write(data.decode())

    # Closing the socket after receiving and saving all the data
    ssl_sock.close()

    # Saving the HTML response with the header in response.html
    with open('response.html', 'w') as file:
        file.write(response)

    # Separating HTTP headers and body
    header_end = response.find("\r\n\r\n")
    if header_end != 1:
        html_body = response[header_end + 4:]
    else:
        html_body = response

    # Saving just the HTML content (without the header) in response2.html
    with open('response2.html', 'w') as file:
        file.write(html_body)

    print("Response with header saved to response.html\n")
    print("Response without header saved to response2.html")

if __name__ == "__main__":
    main()