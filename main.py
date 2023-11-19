import tkinter as tk
from tkinter import ttk
import time
import sendProtocols
from testMermaid import capture_packets, capture_all_packets, stop_capture
import threading
import ipaddress
import socket
import binascii

def update_text_areas(event):
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item, "values")
        # Assuming you want to split the text based on a delimiter for left and right
        left_text = item_values[-2]  # Assuming the left text is in the first column
        right_text = item_values[-1] if len(item_values) > 1 else ''          
        text_area_left.config(state='normal')
        text_area_right.config(state='normal')
        text_area_left.delete('1.0', tk.END)
        text_area_right.delete('1.0', tk.END)
        text_area_left.insert(tk.END, left_text)
        text_area_right.insert(tk.END, right_text)
        text_area_right.insert(tk.END, right_text)
        text_area_left.config(state='disabled')
        text_area_right.config(state='disabled')

def add_packet_to_treeview(packet_info):
    # This function will run in the main thread thanks to root.after
    treeview.insert("", 'end', text="", values=(packet_info))

def clear_view():
    for item in treeview.get_children():
        treeview.delete(item)
    text_area_left.config(state='normal')
    text_area_right.config(state='normal')
    text_area_left.delete('1.0', tk.END)
    text_area_right.delete('1.0', tk.END)
    text_area_left.config(state='disabled')
    text_area_right.config(state='disabled')

def get_ip_from_hostname(hostname):
    try:
        # Get the IP address list of the given hostname
        ip_list = socket.gethostbyname_ex(hostname)[2]
        # For simplicity, return the first IP address; in a real scenario, you might want to handle it differently
        return ip_list[0] if ip_list else None
    except socket.gaierror as e:
        # Handle errors in resolving the hostname
        print(f"Error resolving hostname {hostname}: {e}")
        return None
    
def show_error(message):
    # Update the text of the error_label to show the error message
    error_label.config(text=message)

def packet_callback(packet_info):
    # Since we're working with threads, we need to make sure updates to the GUI are thread-safe.
    # root.after is a thread-safe way to schedule updates to be run in the Tkinter main loop.
    root.after(0, add_packet_to_treeview, packet_info)

def capture_all():
    clear_view()
    threading.Thread(target=capture_all_packets, args=(packet_callback, ), daemon=True).start()
    print("Capture start")

def stop_capture_all():
    stop_capture()
    print("Capture stop")

def send_action():
    # Get the text from text_input Entry widget
    hostname_or_ip = text_input.get()
    if hostname_or_ip == "":
        hostname_or_ip = "computer.tukorea.ac.kr"

    # Check if the input is an IP address or a hostname
    try:
        # First, try to interpret the input as an IP address
        target_ip = ipaddress.ip_address(hostname_or_ip)
    except ValueError:
        # If it raises a ValueError, it's not an IP address, so try to resolve it as a hostname
        target_ip = get_ip_from_hostname(hostname_or_ip)
        if not target_ip:
            show_error("Invalid hostname or IP address entered")
            return
    
    clear_view()
    selected_protocol = protocol_cb.get()


    if (selected_protocol == 'ICMP'):
        threading.Thread(target=capture_packets, args=(str(target_ip), selected_protocol, packet_callback), daemon=True).start()
        time.sleep(1)
        print("Send ICMP")
        sendProtocols.ping(target_ip)
    elif (selected_protocol == 'DNS'):
        threading.Thread(target=capture_packets, args=("8.8.8.8", selected_protocol, packet_callback), daemon=True).start()
        time.sleep(1)
        print("Send DNS")
        sendProtocols.nslookup(hostname_or_ip)
    elif (selected_protocol == 'HTTP'):
        threading.Thread(target=capture_packets, args=(str(target_ip), selected_protocol, packet_callback), daemon=True).start()
        time.sleep(1)
        print("Send HTTP")
        sendProtocols.send_http_get(hostname_or_ip)
    elif (selected_protocol == 'SSH'):
        threading.Thread(target=capture_packets, args=(str(target_ip), selected_protocol, packet_callback), daemon=True).start()
        time.sleep(1)
        print("Send SSH")
        sendProtocols.send_ssh_command()
    print("Text to send:", hostname_or_ip)
    print("Selected protocol:", selected_protocol)
    # Add here the code to handle the sending action


# Initialize the main window
root = tk.Tk()
root.title("Multi-section Window")
root.geometry("1200x600")  # Set the size of the window

# Disable resizing for simplicity
root.resizable(False, False)

# First section with buttons
top_frame = tk.Frame(root, height=50)
top_frame.pack(side=tk.TOP, fill=tk.X)

button1 = tk.Button(top_frame, text="Start Capture", command=capture_all)
button1.pack(side=tk.LEFT, padx=5, pady=5)

button2 = tk.Button(top_frame, text="Stop Capture", command=stop_capture_all)
button2.pack(side=tk.LEFT, padx=5, pady=5)

combo_lbl = tk.Label(top_frame, text="Select Protocol:")
combo_lbl.pack(side=tk.LEFT, padx=5, pady=5)

protocols = ['HTTP', 'SSH', 'ICMP', 'DNS']
protocol_cb = ttk.Combobox(top_frame, values=protocols, state='readonly')  # state='readonly' to prevent user typing
protocol_cb.pack(side=tk.LEFT, padx=5, pady=5)

# Add a text input area
text_input = tk.Entry(top_frame)
text_input.pack(side=tk.LEFT, padx=5, pady=5)


send_button = tk.Button(top_frame, text="Send", command=send_action)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

clear_button = tk.Button(top_frame, text="Clear", command=clear_view)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

# Define the label in your top_frame or where it is appropriate in your layout
error_label = tk.Label(top_frame, text="", fg="red")  # fg="red" to make the error message stand out
error_label.pack(side=tk.LEFT, padx=5, pady=5)



# Second section with Treeview
middle_frame = tk.Frame(root, height=250)
middle_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

treeview = ttk.Treeview(middle_frame)
treeview.pack(expand=True, fill=tk.BOTH)

treeview.bind('<<TreeviewSelect>>', update_text_areas)


# Adding some columns
treeview['columns'] = ("Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7")

# Format our columns
treeview.column("#0", width=0, stretch=tk.NO)
treeview.column("Column1", anchor=tk.W, width=50)
treeview.column("Column2", anchor=tk.W, width=50)
treeview.column("Column3", anchor=tk.W, width=50)
treeview.column("Column4", anchor=tk.W, width=50)
treeview.column("Column5", anchor=tk.W, width=300)
treeview.column("Column6", anchor=tk.W, width=0, stretch=tk.NO)
treeview.column("Column7", anchor=tk.W, width=0, stretch=tk.NO)


# Create Headings
treeview.heading("#0", text="", anchor=tk.W)
treeview.heading("Column1", text="No.", anchor=tk.W)
treeview.heading("Column2", text="Time", anchor=tk.W)
treeview.heading("Column3", text="Source", anchor=tk.W)
treeview.heading("Column4", text="Destination", anchor=tk.W)
treeview.heading("Column5", text="summary", anchor=tk.W)



# Bottom section (third and fourth sections combined)
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Third section with TextArea on the Bottom Left
text_area_left = tk.Text(bottom_frame, state='disabled')
text_area_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Fourth section with TextArea on the Bottom Right
text_area_right = tk.Text(bottom_frame, state='disabled')
text_area_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Configure the columns to share the window width equally
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)

# Start the main loop
root.mainloop()


