from scapy.all import sniff
import pyx
from scapy.libs.test_pyx import PYX

# Capture packets
packets = sniff(count=10)

if PYX == 0:
    print("No PYX")

# Check the type of the 'packets' variable
print(type(packets))  # Outputs: <class 'scapy.plist.PacketList'>
packets.pdfdump("capture.pdf")

# Iterate over the PacketList just like a regular list
for packet in packets:
    print(packet.summary())