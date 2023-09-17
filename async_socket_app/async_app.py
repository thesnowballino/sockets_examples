import socket
from select import select

to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))
server_socket.listen()

# The most important change here is that we decoupled accept_connection and send_message (clearly,
# we don't have to send a message right after accepting a connection).
#
# After that -- all we did is created some kind of a "manager" that will run our functions.
# event_loop is this function.


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # client_socket emulates the client socket on our end.
    print(f"Connection from: {addr}")

    # add client socket obj to monitor.
    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)  # bytes.

    if request:
        response = "Hello, world\n".encode()
        client_socket.send(response)
    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # select chooses only those file-like object that are ready for read / write / errors.
        # it blocks event_loop until it returns something.
        ready_to_read, _, _ = select(to_monitor, [], [])
        print(f"to_monitor: {to_monitor}")
        print(f"ready_to_read: {ready_to_read}")
        print("\n\n")

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                # client socket:
                send_message(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
