class Netroot:
    """Various network tools using raw sockets"""

    def __init__(self, iface='wlan0'):
        import os
        import sys
        if os.geteuid() != 0:
            print('Need to be root')
            sys.exit(255)
        self.iface = iface

    def arp(self, ip):
        """Get MAC by ip"""
        from scapy.layers.l2 import ARP, Ether
        from scapy.data import ETHER_BROADCAST
        from scapy.sendrecv import srp
        pkt = Ether(dst=ETHER_BROADCAST)/ARP(pdst=ip)
        ans, _ = srp(pkt, iface=self.iface, timeout=1)
        for p in ans:
            print(p[1][ARP].hwsrc)

    @staticmethod
    def _on_packet(pkt):
        from scapy.layers.inet import IP, TCP
        if pkt.haslayer(TCP):
            ip: IP = pkt[IP]
            tcp: TCP = pkt[TCP]
            print('{}:{} => {}:{}'.format(ip.src, tcp.sport, ip.dst, tcp.dport))

    def sniff(self):
        from scapy.sendrecv import sniff
        sniff(prn=self._on_packet, iface=self.iface)
