import socket
import random

# Configurarea adresei serverului
host = '127.0.0.1'
port = 8888

def get_computer_choice():
    # Generarea unei alegeri random pentru computer
    choices = ['P', 'H', 'F']
    return random.choice(choices)

def get_winner(player, computer):
    # Determinarea castigatorului in functie de alegerile facute
    if player == computer:
        return "Remiza!"
    elif (player == 'P' and computer == 'F') or (player == 'H' and computer == 'P') or (player == 'F' and computer == 'H'):
        return "Ai castigat!"
    else:
        return "A castigat Computerul!"

def game_start(client_socket):
    # Initializarea scorurilor
    player_score = 0
    computer_score = 0
    rounds = 3

    while player_score < 2 and computer_score < 2:
        # Serverul este pregatit pentru o noua runda
        client_socket.send("Serverul e pregatit!\n".encode())

        # Solicitarea alegerii jucatorului
        client_socket.send("Alege varianta (P pentru Piatra, H pentru Hartie, F pentru Foarfeca): ".encode())
        player_choice = client_socket.recv(1024).decode().strip().upper()

        # Validarea alegerii jucatorului
        if player_choice not in ['P', 'H', 'F']:
            client_socket.send("Nu exista o astfel de varianta. Verificati si introduceti din nou.\n".encode())
            continue

        # Generarea alegerii computerului si determinarea castigatorului
        computer_choice = get_computer_choice()
        result = get_winner(player_choice, computer_choice)

        # Trimiterea alegerii computerului si rezultatul rundei catre client
        client_socket.send(f"Computerul a ales: {computer_choice}\n".encode())
        client_socket.send(f"{result}\n".encode())

        # Actualizarea scorului in functie de rezultatul rundei
        if result == "Ai castigat!":
            player_score += 1
        elif result == "A castigat Computerul!":
            computer_score += 1

        # Trimiterea scorului curent catre client
        client_socket.send(f"Scor: Tu {player_score} - {computer_score} Computerul\n".encode())

    # Determinarea castigatorului final si trimiterea rezultatului catre client
    if player_score > computer_score:
        client_socket.send(f"Ai castigat din {player_score} incercari!\n".encode())
    elif player_score == computer_score:
        client_socket.send("Remiza!\n".encode())
    else:
        client_socket.send("A castigat computerul.\n".encode())

# Crearea socketului serverului si initializarea ascultarii
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)
print('Serverul TCP este pregatit de lucru si asculta pe adresa:', server_socket.getsockname())

while True:
    # Acceptarea conexiunii de la client
    client_socket, addr = server_socket.accept()
    print(f"Adresa {addr} s-a conectat.")

    while True:
        # Trimiterea mesajului de start catre client
        client_socket.send("Scrie START pentru a incepe jocul de Piatra-Foarfeca-Hartie sau Q pentru a iesi.\n".encode())
        start_command = client_socket.recv(1024).decode().strip().upper()
        if start_command == "START":
            # Inceperea jocului daca clientul trimite comanda START
            game_start(client_socket)
        elif start_command == "Q":
            # Deconectarea clientului daca trimite comanda Q
            client_socket.send("Deconectare...\n".encode())
            break
        else:
            # Mesaj pentru comanda necunoscuta
            client_socket.send("Comanda necunoscuta. Introdu START pentru a incepe jocul sau Q pentru a iesi.\n".encode())
    client_socket.close()
