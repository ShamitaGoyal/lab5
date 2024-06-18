# Name: Shamita Goyal, Wingyi Ng
# Lab 5
# Module: Network, Timing

import socket
import threading
import os
import sys


HOST = 'localhost'  # Server hostname
PORT = 5113
MIN_CLIENTS = 1     # Minimum number of clients
MAX_CLIENTS = 5     # Maximum number of clients
MIN_TIMEOUT = 3     # Minimum connection timeout in seconds
MAX_TIMEOUT = 120   # Maximum connection timeout in seconds

client_connections = {}

def change_directory(current_dir, new_directory):
    """
    Change directory; return "success" or "fail".
    """
    new_path = os.path.join(current_dir, new_directory)
    if os.path.isdir(new_path):
        return new_path, "success"
    else:
        return current_dir, "fail - No such directory"

def list_current_d(current_dir):
    """
    List the directories and files in the current directory.
    """
    try:
        files = os.listdir(current_dir)
        return "\n".join(files)
    except Exception as e:
        return str(e)

def recursive_d(current_dir):
    """
    Send the list of subdirectories from a recursive
    walk of the client's current directory.
    """
    sub_d = []
    for root, dirs, _ in os.walk(current_dir):
        for d in dirs:
            sub_d.append(os.path.relpath(os.path.join(root, d), current_dir))
    return "\n".join(sub_d)

def handle_client(conn, client_id):
    """
    Handle client requests.
    """
    current_dir = os.getcwd()  # Each client starts in the server's current directory
    commands_dict = {
        "cd": lambda args: change_directory(current_dir, args[0]) if len(args) == 1 else (current_dir, "Invalid cd command"),
        "ls": lambda _: (current_dir, list_current_d(current_dir)),
        "lsr": lambda _: (current_dir, recursive_d(current_dir))
    }

    while True:
        request = conn.recv(1024).decode().strip()
        if not request:
            break

        command_parts = request.split()
        command = command_parts[0]
        args = command_parts[1:]

        if command == "q":
            print(f'Connection to Client{client_id} closed')
            break
        elif command in commands_dict:
            current_dir, response = commands_dict[command](args)
        else:
            response = "Invalid command"

        conn.sendall(response.encode('utf-8'))

    conn.close()
    del client_connections[client_id]

def checkArgs(arg_list):
    """
    Validate arguments sent in on command line
    """
    invalid = ''
    try:
        if len(arg_list) > 3:
            raise RuntimeError
        num = int(arg_list[1])
        timeout = int(arg_list[2])
        if not MIN_CLIENTS <= num <= MAX_CLIENTS:
            invalid = f'Number of clients must be between {MIN_CLIENTS} and {MAX_CLIENTS}'
        elif not MIN_TIMEOUT <= timeout <= MAX_TIMEOUT:
            invalid = f'Timeout must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds'
    except RuntimeError:
        invalid = 'Received too many command line arguments'
    except IndexError:
        invalid = 'Received insufficient number of command line arguments'
    except ValueError:
        invalid = 'Unexpected argument in command line, expected integer'
    return invalid

def main():
    """
    Code driver to start server, manage connections, and handle requests
    """
    invalid = checkArgs(sys.argv)
    if invalid:
        print(f'\tUsage: {sys.argv[0]} number_of_clients timeout_in_seconds')
        print(f'\t{invalid}')
        raise SystemExit('\tPlease check command line arguments and try again')

    time_out = int(sys.argv[2])
    max_allowed = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print(f"Server started, hostname: {HOST}, port: {PORT}")
        print(f"Starting directory: {os.getcwd()}")
        s.listen(max_allowed)
        s.settimeout(time_out)

        threads = []
        try:
            for client_id in range(1, max_allowed + 1):
                try:
                    conn, addr = s.accept()
                    print(f"Client{client_id} established with {addr}")
                    client_connections[client_id] = conn
                    t = threading.Thread(target=handle_client, args=(conn, client_id))
                    threads.append(t)
                    t.start()
                except socket.timeout:
                    print(f'{time_out} seconds is up, closing {max_allowed - len(threads)} unused connections')
                    break

            for t in threads:
                t.join()

        finally:
            s.close()
            print("Server timeout: no connections")
            print("Server closed.")

if __name__ == '__main__':
    main()
