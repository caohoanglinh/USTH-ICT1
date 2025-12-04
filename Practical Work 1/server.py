import socket
import logging

BUFFER = 4096
PORT = 5001

logging.basicConfig(level=logging.INFO)


def start_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(1)
    logging.info(f"Server listening on port {port}")
    return s


def receive_file(conn):
    name_len = int.from_bytes(conn.recv(4), "big")

    filename = conn.recv(name_len).decode()

    file_size = int.from_bytes(conn.recv(8), "big")

    logging.info(f"Receiving file '{filename}' ({file_size} bytes)")

    with open(filename, "wb") as f:
        received = 0
        while received < file_size:
            chunk = conn.recv(BUFFER)
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)

    logging.info("File successfully received")

    conn.send(b"File received OK")


if __name__ == "__main__":
    server_socket = start_server(PORT)
    conn, addr = server_socket.accept()
    logging.info(f"Client connected: {addr}")

    receive_file(conn)

    conn.close()
    server_socket.close()
