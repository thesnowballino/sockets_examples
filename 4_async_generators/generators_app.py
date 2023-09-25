import socket
from typing import TypeAlias, Generator

from select import select

# David Beazley
# PyCon 2015
# Concurrency from the Ground up Live

SocketGenerator: TypeAlias = Generator[tuple[str, socket.socket], None, None]
pending_tasks: list[SocketGenerator] = []

to_read: dict[socket.socket, SocketGenerator] = {}
to_write: dict[socket.socket, SocketGenerator] = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    while True:
        yield ("read", server_socket)
        # client_socket emulates the client socket on our end.
        client_socket, addr = server_socket.accept()  # read.

        print(f"Connection from: {addr}")
        pending_tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ("read", client_socket)
        request = client_socket.recv(4096)  # read.

        if not request:
            break
        else:
            response = "Hello, world\n".encode()
            yield ("write", client_socket)
            client_socket.send(response)  # write.

    client_socket.close()


def event_loop():
    while any([pending_tasks, to_read, to_write]):
        # here we add new pending tasks (i.e. ready sockets)...
        while not pending_tasks:
            # select blocks until there is a socket with a changed state.
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            print("Here!")
            for sock in ready_to_read:
                pending_tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                pending_tasks.append(to_write.pop(sock))

        # ... and here we drive our coros with actions.
        try:
            task: SocketGenerator = pending_tasks.pop(0)
            action, sock = next(task)

            if action == "read":
                to_read[sock] = task
            elif action == "write":
                to_write[sock] = task
        except StopIteration:
            print("Done!")


if __name__ == "__main__":
    pending_tasks.append(server())
    event_loop()
