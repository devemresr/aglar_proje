import socket
import random

# List of words for the game
WORDS = ["Kedi", "Abla", "Fare", "Acil", "Gram", "Kupa", "Jant", "Ordu", "Onay", "Oyun"]
# Function to choose a random word from the list
def choose_word():
    return random.choice(WORDS)

# Function to handle client connections
def handle_client(client_socket):
    word = choose_word()
    firstChar = word[0].upper()
    result = firstChar + "_" * (len(word) - 1)
    
    attempts = 5

    # Send initial message to client
    client_socket.send(f"You have {attempts} attempts to guess the word. Good luck!\n".encode())

    while attempts > 0:
        # Send current status of guessed word to client

        client_socket.send(f"Word: {result}\n".encode())

        # Prompt client for a guess
        client_socket.send("Enter a word: ".encode())
        guess = client_socket.recv(1024).decode().strip().lower()

        if len(guess) != len(word) or not guess.isalpha():
            client_socket.send("Invalid guess! Please enter a word with the same length as the target word.\n".encode())
            continue

        if guess == word.lower():
            client_socket.send("congrats.\n".encode())
            break
        else:
            for i in range(len(word)):
                if guess[i] in word and not guess[i] == word[i]:
                    result = result[:i] + guess[i].lower() + result[i+1:]
                elif guess[i] == word[i]:
                    result = result[:i] + guess[i].upper() + result[i+1:]
        client_socket.send(f"Word: {result}\n".encode())
        attempts -= 1
        client_socket.send(f"You have {attempts} guesses left.\n".encode())

    if attempts == 0:
        client_socket.send(f"Sorry, you ran out of attempts. The word was {word}\n".encode())

    client_socket.close()

# Main function to start the server
def main():
    host = "127.0.0.1"
    port = 65535

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()