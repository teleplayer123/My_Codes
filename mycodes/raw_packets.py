from collections import defaultdict
import os
import socket
import struct
import sys
from time import time, sleep
from datetime import date

from hex_dump import xdump


class EthHeader:
    def __init__(self, frame):
        eth = frame[0:14]
        ehdr = struct.unpack("!6B6BH", eth)
        self.size = struct.calcsize("!6B6BH")
        self.dst = ehdr[0:6]
        self.src = ehdr[6:12] 
        self.etype = ehdr[12]

    def fmt_mac(self, data):
        bs = ["%02x" % data[i] for i in range(len(data))]
        return ":".join(bs)

    def get_type(self, data):
        etype = "Unknown"
        set_of_pairs = {
        "IPv4": 0x0800,
        "ARP": 0x0806,
        "RARP": 0x8035,
        "SNMP": 0x814c,
        "IPv6": 0x86dd
        }
        for k, v in set_of_pairs.items():
            if data == v:
                etype = k
                break
        return etype

    def dump(self):
        print("Ethernet Header")
        print("------------------------")
        print("Destination: ", self.fmt_mac(self.dst))
        print("Source: ", self.fmt_mac(self.src))
        print("Ether Type: ", "0x{:04x} {}".format(self.etype, self.get_type(self.etype)))

    def __str__(self):
        return """
        Ethernet Header
        ---------------------
        Destination: {}
        Source: {}
        Type: 0x{:04x} {}
        """.format(self.fmt_mac(self.dst), self.fmt_mac(self.src),
            self.etype, self.get_type(self.etype))

class IPHeader:
    def __init__(self, frame):
        hstr = frame[14:34]
        iph = struct.unpack("!BBHHHBBH4s4s", hstr)
        self.size = struct.calcsize("!BBHHHBBH4s4s")
        self.version = iph[0] >> 4
        self.internet_header_len = (iph[0] & 0b1111) * 4
        self.type_service = iph[1] >> 6
        self.explicit_congestion = iph[1] & 0b11
        self.total_len = iph[2]
        self.id = iph[3]
        self.flags = self.get_flag((iph[4] >> 3))
        self.fragment_offset = iph[4] & 0b1111111111111
        self.time_to_live = iph[5]
        self.protocol = iph[6]
        self.checksum = iph[7]
        self.src_addr = socket.inet_ntoa(iph[8])
        self.dst_addr = socket.inet_ntoa(iph[9])

    def get_flag(self, fbits):
        flags = []
        if fbits & 0b11 >> 1:
            flags.append("DF")
        if fbits & 0b1:
            flags.append("MF")
        if flags != []:
            return ",".join(flags)
        else:
            return "--"

    def dump(self):
        print("IP Header")
        print("------------------")
        print(f"Version: {self.version}")
        print(f"Header Length: {self.internet_header_len}")
        print(f"Type of Service: {self.type_service}")
        print(f"Explicit Congestion Notification: {self.explicit_congestion}")
        print(f"Total Length: {self.total_len}")
        print(f"Identification: {self.id}")
        print(f"Flags: {self.flags}")
        print(f"Fragment Offset: {self.fragment_offset}")
        print(f"Time to Live: {self.time_to_live}")
        print(f"Protocol: {self.protocol}")
        print(f"Checksum: {self.checksum}")
        print(f"Source Address: {self.src_addr}")
        print(f"Destination Address: {self.dst_addr}")

    def __str__(self):
        return f"""
        IP Header
        ------------------
        Version: {self.version}
        Header Length: {self.internet_header_len}
        Type of Service: {self.type_service}
        Explicit Congestion Notification: {self.explicit_congestion}
        Total Length: {self.total_len}
        Identification: {self.id}
        Flags: {self.flags}
        Fragment Offset: {self.fragment_offset}
        Time to Live: {self.time_to_live}
        Protocol: {self.protocol}
        Checksum: {self.checksum}
        Source Address: {self.src_addr}
        Destination Address: {self.dst_addr}
        """

class TCPHeader:
    def __init__(self, frame, ipheader):
        header_size = 14 + ipheader.internet_header_len
        tcphead = frame[header_size: header_size + 20]
        tcpbits = struct.unpack("!HHLLHHHH", tcphead)
        self.raw_bits = "".join(tcpbits)
        self.size = struct.calcsize("!HHLLHHHH")
        self.src_port = tcpbits[0]
        self.dst_port = tcpbits[1]
        self.seq_num = tcpbits[2]
        self.ack_num = tcpbits[3]
        self.offset = (tcpbits[4] >> 12) * 4
        self.flags = self.get_flags(tcpbits[4] & 0b111111111)
        self.window_size = tcpbits[5]
        self.checksum = tcpbits[6]
        self.urg_pointer = tcpbits[7]

    def get_flags(self, flagbits):
        flag_dict = {
            "NS": 0b100000000 & flagbits,
            "CWR": 0b010000000 & flagbits,
            "ECE": 0b001000000 & flagbits,
            "URG": 0b000100000 & flagbits,
            "ACK": 0b000010000 & flagbits,
            "PSH": 0b000001000 & flagbits,
            "RST": 0b000000100 & flagbits,
            "SYN": 0b000000010 & flagbits,
            "FIN": 0b000000001 & flagbits,
            }
        flags = []
        for flag, bits in flag_dict.items():
            if bits:
                flags.append(flag)
        if flags != []:
            return ",".join(flags)
        else:
            return "--"

    def dump(self):
        print("TCP Header")
        print("-------------------")
        print(f"Source Port: {self.src_port}")
        print(f"Destination Port: {self.dst_port}")
        print(f"Sequence Number: {self.seq_num}")
        print(f"Aknowledgment Number: {self.ack_num}")
        print(f"Data Offset: {self.offset}")
        print(f"Flags: {self.flags}")
        print(f"Window Size: {self.window_size}")
        print(f"Checksum: {self.checksum}")
        print(f"Urgent Pointer: {self.urg_pointer}")

    def __str__(self):
        return f"""
        TCP Header
        -------------------
        Source Port: {self.src_port}
        Destination Port: {self.dst_port}
        Sequence Number: {self.seq_num}
        Aknowledgment Number: {self.ack_num}
        Data Offset: {self.offset}
        Flags: {self.flags}
        Window Size: {self.window_size}
        Checksum: {self.checksum}
        Urgent Pointer: {self.urg_pointer}
        """

class TCP_Packet(object):
    def __init__(self, frame):
        self.eth = EthHeader(frame)
        self.ip = IPHeader(frame)
        self.tcp = TCPHeader(frame, self.ip)
        self.bytes = frame.__sizeof__() - (self.tcp.offset-1)
        total_header_size = self.eth.size + self.ip.size + self.tcp.size
        self.data = frame[total_header_size: total_header_size + self.tcp.offset-1]

    def dump(self):
        print(f"\nTCP Packet\nbytes {self.bytes}")
        print("----------------------------------------\n")
        self.eth.dump()
        print("\n")
        self.ip.dump()
        print("\n")
        self.tcp.dump()
        print("\n")

    def __repr__(self):
        return f"""
        {str(self.eth)}
        {str(self.ip)}
        {str(self.tcp)}
        """



arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]
s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

current_date = date.fromtimestamp(time())
dumpdir = "/path/to/captures/{}".format(current_date)
packet_by_id = defaultdict(list)
packet_by_src_dest = defaultdict(list)

try:
    while True:
        try:
            frame = s.recv(4096)
            tcp = TCP_Packet(frame)
            packet_by_id[tcp.ip.id].append(repr(tcp))
            packet_by_src_dest[(tcp.ip.src_addr, tcp.ip.dst_addr)].append(repr(tcp))
            tcp.dump()
            xdump(tcp.tcp.raw_bits)
        except KeyboardInterrupt:
            break
except KeyboardInterrupt:
    s.close()
finally:
    if arg in {"-s"}:
        if not os.path.exists(dumpdir):
            os.mkdir(dumpdir)
        for i, ps in packet_by_src_dest.items():
            fn = dumpdir + "/{}".format(i)
            with open(fn, "w") as fh:
                for p in ps:
                    fh.write(p)
                    fh.write("\n")
    sys.exit()
