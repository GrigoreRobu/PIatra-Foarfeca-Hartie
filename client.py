import socket

# Configurarea adresei serverului
host = '127.0.0.1'
port = 8888

# Crearea socketului clientului si conectarea la server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    # Primirea mesajelor de la server
    server_message = client_socket.recv(1024).decode()
    print(server_message, end='')

    # Verificarea mesajului de la server si trimiterea raspunsului
    if "Alege varianta" in server_message or "Scrie START" in server_message:
        user_input = input().strip().upper()
        client_socket.send(user_input.encode())

        # Incheierea conexiunii daca utilizatorul alege 'Q'
        if user_input == 'Q':
            break

# Inchiderea conexiunii cu serverul
client_socket.close()
