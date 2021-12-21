import argparse
import re
import socket 
import subprocess
import sys

#TODO
#integrate functionality of adb for andriod specific tasks 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host_info", dest="host_info", action="store_true")
    parser.add_argument("scan_target", dest="scan_target", action="store_true")
    parser.add_argument("-n", "--name", dest="host_name", action="store_true")
    parser.add_argument("-a", "--haddr", dest="host_addr", action="store_true")
    parser.add_argument("-t", "--target", dest="target", action="store")
    group_args = parser.parse_args(["host_info", "scan_target"])
    if group_args.host_info:
        args = parser.parse_args(["-n", "--name", "-a", "--haddr"])
        if args.host_addr:
            print(socket.gethostbyname(socket.gethostname()))
        if args.host_name:
            print(socket.gethostname())
    elif group_args.scan_target:
        args = parser.parse_args(["-t", "--target"])
        target = args.target
        if re.match(r"[\d].[\d].[\d].[\d]/[\d]", target):
            run_subnet_scan()


def run_subnet_scan(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



main()
