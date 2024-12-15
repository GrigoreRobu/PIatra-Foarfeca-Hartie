import socket
import random

host = '127.0.0.1'
port = 8888


def get_computer_choice():
    choices = ['P', 'F', 'H']
    return random.choice(choices)


def get_winner(player, computer):
    if player == computer:
        return "Remiza!"
    elif (player == 'P' and computer == 'F') or (player == 'H' and computer == 'P') or (
            player == 'F' and computer == 'H'):
        return "Ai castigat!"
    else:
        return "A castigat Computerul!"


def game_start(client_socket):
    player_score = 0
    computer_score = 0
    rounds = 3
    for _ in range(rounds):
        client_socket.send("Scrie alegerea ta(P/F/H): ".encode())
        player_choice = client_socket.recv(1024).decode().strip().upper()

        if player_choice not in ['P', 'H', 'F']:
            client_socket.send("Poti folosi doar P, F sau H.\n".encode())
            continue

        computer_choice = get_computer_choice()
        result = get_winner(player_choice, computer_choice)

        client_socket.send(f"Computer: {computer_choice}\n".encode())
        client_socket.send(f"{result}\n".encode())

        if result == "Ai castigat!":
            player_score += 1
        elif result == "A castigat Computerul!":
            computer_score += 1

        if player_score == 2 or computer_score == 2:
            break

    if player_score > computer_score:
        client_socket.send("Ai castigat!\n".encode())
    else:
        client_socket.send("A castigat computerul.\n".encode())


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print('Serverul TCP este pregatit de lucru si asculta pe adresa:', server_socket.getsockname())

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Adresa {addr} s-a conectat.")
        client_socket.send("Scrie START pentru a incepe jocul de Piatra Foarfeca Hartie.\n".encode())

        start_command = client_socket.recv(1024).decode().strip().upper()
        if start_command == "START":
            game_start(client_socket)

        client_socket.close()


if __name__ == "__main__":
    main()
