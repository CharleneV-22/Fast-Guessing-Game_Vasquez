"""
Simple guessing game client using only the socket library.

Connects to the guessing game server, prints its messages, and
lets the user enter guesses.
"""

import socket
import sys


def parse_args():
    if len(sys.argv) != 3:
        print("Usage: python guess_client.py <192.168.56.1> <12345>")
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be an integer.")
        sys.exit(1)

    return host, port


def run_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    print(f"Connected to {host}:{port}")
    print("Press Ctrl+C to quit.\n")

    try:
        # Simple loop: receive from server, display, send user input when prompted.
        # We keep reading small chunks and print them as they come.
        buffer = b""
        while True:
            data = sock.recv(4096)
            if not data:
                print("\nServer closed the connection.")
                break

            buffer += data
            text = buffer.decode("utf-8", errors="replace")

            # Print all text received so far
            print(text, end="", flush=True)

            # If the server is asking for input (we detect by "Enter your guess")
            if "Enter your guess" in text:
                user_input = input()  # read from stdin
                # Send with newline
                sock.sendall((user_input + "\n").encode("utf-8"))
                buffer = b""
            else:
                # Reset buffer after printing; keep it simple
                buffer = b""

    except KeyboardInterrupt:
        print("\nClient interrupted by user.")
    finally:
        sock.close()


if __name__ == "__main__":
    host_arg, port_arg = parse_args()
    run_client(host_arg, port_arg)

