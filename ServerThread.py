
import threading
import time
import signal
from socket import *
from fib import fib



class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    global intr
    
    while not intr.is_set():

        client, addr = sock.accept()
        print("Connection", addr)

        thread = threading.Thread(
            target=task,
            args=(client,),
            daemon=True
        )

        thread.start()

        pool[thread.ident] = thread
        thread = None
    
    client.close()
    sock.close()


def task(client):

    global intr

    while not intr.is_set():
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        print(resp)
        client.send(resp)

    print(f"{client.getsockname()} closed connection")
    client.close()


def main(address):

    global intr
    global pool

    serverThread = threading.Thread(
        target=server,
        args=(address,),
        daemon=True
    )

    serverThread.start()

    try:
        while not intr.is_set():
            time.sleep(0.3)

    except ServiceExit:
        intr.set()
        
        # serverThread.join()
        print("\nConnection pool:", pool)
        print("\nServer shutting down")
        time.sleep(0.7)


        


global intr
global pool

intr = threading.Event()
pool = {}

if __name__ == "__main__":

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    main(("", 25000))
