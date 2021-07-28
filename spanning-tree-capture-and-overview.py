#Import scapy
from scapy.all import *

#Capture STP frame
pkt = sniff(filter="ether dst 01:80:c2:00:00:00",count=1)    

#View captured frame
pkt[0]

#View captured frame - show nicely
pkt[0].show()

#View 802.3 Ethernet
pkt[0][0].show()

#View Logical-Link Control
pkt[0][1].show()

#View STP
pkt[0][2].show()
