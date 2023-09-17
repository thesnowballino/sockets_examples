import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP protocol.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse the port immediately after killing the process.
server_socket.bind(("localhost", 5000))  # IP, port.
server_socket.listen()


def accept_connection(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from: {addr}")
        send_message(client_socket)


def send_message(client_socket):
    while True:
        request = client_socket.recv(4096)  # bytes.

        if not request:
            break
        else:
            response = "Hello, world\n".encode()
            client_socket.send(response)

    client_socket.close()  # emulates client socket on our end.


if __name__ == "__main__":
    accept_connection(server_socket)
