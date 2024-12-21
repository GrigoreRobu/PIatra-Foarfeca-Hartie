import socket

host = '127.0.0.1'
port = 8888


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    server_message = client_socket.recv(1024).decode()
    print(server_message, end='')

    if "Alege varianta" in server_message or "Scrie START" in server_message:
        user_input = input().strip().upper()
        client_socket.send(user_input.encode())

        if user_input == 'Q':
            break

client_socket.close()
