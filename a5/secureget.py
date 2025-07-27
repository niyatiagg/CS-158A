import socket, ssl

host_name = "www.google.com"
port_number = 443

c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_sock.connect((host_name, port_number))

context = ssl.create_default_context()
ssl_sock = context.wrap_socket(c_sock, server_hostname=host_name)

request = f"GET / HTTP/1.1\r\nHost: {host_name}\r\nConnection: close\r\n\r\n"
ssl_sock.sendall(request.encode())

with open('response.html', 'a') as file:
    while True:
        data = ssl_sock.recv(1024)
        if not data:
            break
        file.write(data.decode())

ssl_sock.close()