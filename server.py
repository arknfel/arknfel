# server.py

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from fib import fib
from threading import Thread

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("closed")

if __name__ == "__main__":
    fib_server(('', 25000))