# Client-server application — where the server can respond to a number of clients and send information about files and directories on the server

- two files: `server.py` and `client.py`

## The server:
- accepts 2 command line arguments: the number of clients it can serve, and the number of seconds before time out
- creates a thread to respond to each client
- lets the client look up files and directories of a (supposedly remote) directory tree that's on the server

## Upon connecting to the server, the client can request the following tasks from the server:
- show files and directories in the current directory
- show all subdirectories (recursively) in the current directory
- go to a new directory
- quit
