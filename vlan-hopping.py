#!/usr/bin/python3

#Import scapy
from scapy.all import *

#Craft packet with 802.1Q headers
packet = Ether(dst="ff:ff:ff:ff:ff:ff")/\
         Dot1Q(vlan=1)/\
         Dot1Q(vlan=2)/\
         Dot1Q(vlan=2)/\
         IP(src="10.1.2.3",dst="10.1.2.254")/\
         ICMP()

#Show packet
packet.show()

#Sent packet
sendp(packet)
