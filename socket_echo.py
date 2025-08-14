#!/usr/bin/env python3
import socket
import sys
import threading
from typing import Tuple

HOST = "127.0.0.1"
PORT = 53236
TIMEOUT = 10.0
BUF_SIZE = 4096
DELIM = b"\n"

def recv_line(conn: socket.socket) -> bytes:
    buf = bytearray()
    while True:
        chunk = conn.recv(BUF_SIZE)
        if not chunk:

            return bytes(buf)
        buf.extend(chunk)
        if DELIM in buf:
            line, _, rest = bytes(buf).partition(DELIM)

            return line

def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    conn.settimeout(TIMEOUT)
    try:
        print(f"[server] connected: {addr}")
        line = recv_line(conn)
        if not line:
            print(f"[server] no data received from {addr}")
            return
        msg = line.decode("utf-8", errors="replace")
        print(f"[server] received: {msg!r} from {addr}")
        response = (msg.upper() + "\n").encode("utf-8")
        conn.sendall(response)
        print(f"[server] responded to {addr}")
    except socket.timeout:
        print(f"[server] timeout: {addr}")
    except Exception as e:
        print(f"[server] error with {addr}: {e}")
    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        conn.close()
        print(f"[server] closed: {addr}")

def run_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[server] listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()

            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def run_client(message: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        s.connect((HOST, PORT))
        print(f"[client] Connected to: {s}.")
        payload = (message + "\n").encode("utf-8")
        s.sendall(payload)
        line = recv_line(s)
        if not line:
            print("[client] no response received")
            return
        print(f"[client] response: {line.decode('utf-8', errors='replace').rstrip()}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("server", "client"):
        print(f"Usage:\n  {sys.argv[0]} server\n  {sys.argv[0]} client 'your message'")
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "server":
        run_server()
    else:
        msg = sys.argv[2] if len(sys.argv) > 2 else "hello world"
        run_client(msg)