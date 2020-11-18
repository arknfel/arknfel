# client.py
import socket
  
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 25000)) 



if __name__ == "__main__":
    while True:
        msg = input(' >> ')
        sock.send(msg.encode('ascii'))
        resp = sock.recv(1024)
        print(resp.decode('ascii'))
    sock.close()
    print("Connection closed")
