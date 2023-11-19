from scapy.all import sniff, IP, TCP, sr1, ICMP, Raw
from requests import get
import subprocess
import threading
import time
import socket
from datetime import datetime
from scapy.utils import hexdump

packet_counter = 0

# Resolve the IP address for www.google.com
def get_ip(domain):
    return socket.gethostbyname(domain)

# Send an HTTP GET request to www.google.com
def send_http_request(url):
    response = get(url)
    return response

# Generate Mermaid diagram from packets
def generate_mermaid_diagram(packets):
    mermaid_diagram = "sequenceDiagram\n"
    for line in packets:
        mermaid_diagram += f"    {line}\n"
    return mermaid_diagram

# Convert Mermaid diagram to image
def generate_diagram_image(input_file, output_file):
    subprocess.run(['mmdc', '-i', input_file, '-o', output_file], check=True)
    print(f"Diagram generated and saved to {output_file}.")


# Capture the packets
# Capture the packets with a specified protocol
def capture_packets(target_ip, targetProtocol, callback, timeout=5):
    global packet_counter
    packet_counter = 0
    # Define the packet processing function
    def process_packet(packet):
        # Check if the packet matches the given protocol
        print(f"Packet captured at {packet.time}")
        
        # If the packet matches our target IP and protocol, append it to the packets list
        if packet.haslayer(IP) and (packet[IP].src == target_ip or packet[IP].dst == target_ip):
            print(f"Packet captured at {packet.time}")
            global packet_counter
            packet_counter += 1
            no = packet_counter
            readable_time = datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S')  # Human-readable time
            source = packet[IP].src
            destination = packet[IP].dst
            packetProtocol = packet.sprintf("%IP.proto%")  # or however you are determining the protocol
            if packet.haslayer(TCP):
                payload = packet.lastlayer()
            else:
                payload = packet.lastlayer()
            
            # Create a tuple with the packet details
            packet_info = (no, str(readable_time), source, destination, packet.summary(), packet.show(dump=True), hexdump(payload, dump=True) )
            

            packets.append(f"{packet[IP].src}->>{packet[IP].dst}: len={len(packet)} / {packet.summary()}")
            print(packet.summary())
            # Now call the callback with the packet info
            callback(packet_info) 
    
    # Start the packet capture
    packets = []
    # Construct the filter string based on the protocol
    filter_str = f"host {target_ip}"
    if targetProtocol.upper() == 'ICMP':
        filter_str += " and icmp"
    elif targetProtocol.upper() == 'HTTP':
        filter_str += " and tcp port 80"
    elif targetProtocol.upper() == 'SSH':
        filter_str += " and tcp port 22"
    elif targetProtocol.upper() == 'TCP':
        filter_str += " and tcp"
    
    print(f"Starting packet capture with filter '{filter_str}'")
    sniff(filter=filter_str, prn=process_packet, timeout=timeout)

    # Generate Mermaid diagram
    mermaid_diagram = generate_mermaid_diagram(packets)
    mermaid_file = 'diagram.mmd'
    with open(mermaid_file, 'w') as file:
        file.write(mermaid_diagram)

    # Convert the Mermaid diagram into an image
    output_image_file = '{targetProtocol}->{targetIp}.png'.format(targetProtocol=targetProtocol, targetIp=target_ip)
    generate_diagram_image(mermaid_file, output_image_file)
    return packets

