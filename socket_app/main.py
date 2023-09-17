import socket
from views import blog, index

URLS = {
    "/": index,
    "/blog": blog,
}


def parse_request(request: str) -> tuple[str, str]:
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method: str, url: str) -> tuple[str, int]:
    if method != "GET":
        return "HTTP/1.1 405 Method not allowed\n\n", 405

    if url not in URLS:
        return "HTTP/1.1 404 Not found\n\n", 404

    return "HTTP/1.1 200 OK\n\n", 200


def generate_content(code: int, url: str) -> str:
    if code == 404:
        return "<h1>404</h1><p>Not found</p>"
    if code == 405:
        return "<h1>405</h1><p>Method not allowed</p>"
    return URLS[url]()


def generate_response(request: str) -> bytes:
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP protocol.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse the port immediately after killing the process.
    server_socket.bind(("localhost", 5000))  # IP, port.
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)  # bytes.
        print(request)
        print()
        print(addr)

        response = generate_response(request.decode("utf-8"))

        # answer
        client_socket.sendall(response)
        client_socket.close()


if __name__ == "__main__":
    run()
