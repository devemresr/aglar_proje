import socket

def main():
    host = "127.0.0.1"
    port = 65535

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to the server.")

    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(message, end='')

        if "Enter a word" in message:
            guess = input()
            client_socket.send(guess.encode())

    client_socket.close()

if __name__ == "__main__":
    main()
