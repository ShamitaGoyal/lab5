# Name: Shamita Goyal, Wingyi Ng
# Lab 5
# Module: Network, Timing

import socket
import os

HOST = 'localhost'
PORT = 5113

def handle_choice():
    """handles the choice picked by user --> returns the choice made"""
    print("=" * 50)
    print("\nCommands:")
    menu = "\n".join(f"{command:<15} {description}" for command, description in [
        ("ls", "list current directory"),
        ("lsr", "list subdirectories recursively"),
        ("cd dir_name", "go to dir_name"),
        ("q", "quit")
    ])

    print(menu, "\n")
    print("=" * 50)

    while True:
        choice = input('Enter choice: ').lower().strip()
        print("=" * 50)
        if choice in ['ls', 'lsr', 'q'] or (choice.startswith('cd') and len(choice.split()) == 2):
            return choice
        else:
            print('Invalid choice. Try again.')

def main():
    print("=" * 50)
    print(f"Client connected to: {HOST}, port: {PORT}")

    current_path = "."

    with socket.socket() as s:
        try:
            s.connect((HOST, PORT))
            while True:
                command = handle_choice()
                s.sendall(command.encode())

                if command == "q":
                    print("Quitting client")
                    break

                response = s.recv(1024).decode()
                print("Response from server:")

                # Print the new path if 'cd' command was successful
                if command.startswith("cd") and response == "success":
                    new_dir = command.split()[1]
                    current_path = os.path.join(current_path, new_dir)
                    current_path = os.path.realpath(current_path)
                    print(f"Path successfully changed to: {current_path}")
                else:
                    listing_path = current_path if command.startswith("cd") else os.path.realpath(current_path)
                    print(f"Listing of {listing_path}")
                    print(response)

        except ConnectionError as e:
            print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    main()
