import socket
import os
import sys


HOST = "0.0.0.0"
PORT = 2222

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print("listening for client...")
client_sock, client_addr = sock.accept()
head = client_sock.recv(1024).decode()
print("connecting to: ", head)

while True:
    try:
        cmd = input(f"enter command: ").encode()
        if cmd.decode().split(" ")[0] == "download":
            client_sock.send(cmd)
            path = cmd.decode().split(" ")[1]
            print(f"downloading {path}...")
            with open("copy" + path, "w") as fh:
                rdata = client_sock.recv(1024).decode()
                while True:
                    if rdata == "DONE":
                        break
                    fh.write(rdata)
                    rdata = client_sock.recv(1024).decode()
            print("...finished downloading")
        else:
            client_sock.send(cmd)
            data = client_sock.recv(1024).decode()
            if data in {"q", "quit", "Q", "Quit"}:
                print("terminating...")
                break
            while True:
                print(data)
                if len(data) < 1024:
                    break
                data = client_sock.recv(1024).decode()
    except socket.error as err:
        print(f"error: {err}, terminating...")
        client_sock.shutdown(socket.SHUT_RDWR)
        break
    except KeyboardInterrupt:
        client_sock.send(str("quit").encode())
        client_sock.close()
        sock.close()
        break
    except Exception as err:
        print(f"exerr: {err}")
        continue
client_sock.close()
sock.close()
