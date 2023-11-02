import tkinter as tk
from tkinter import ttk

def update_text_areas(event):
    print("Updating text areas")
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item, "values")
        # Assuming you want to split the text based on a delimiter for left and right
        left_text = item_values[0]  # Assuming the left text is in the first column
        right_text = item_values[1] if len(item_values) > 1 else ''          
        text_area_left.config(state='normal')
        text_area_right.config(state='normal')
        text_area_left.delete('1.0', tk.END)
        text_area_right.delete('1.0', tk.END)
        text_area_left.insert(tk.END, left_text)
        text_area_right.insert(tk.END, right_text)
        text_area_left.config(state='disabled')
        text_area_right.config(state='disabled')

# Initialize the main window
root = tk.Tk()
root.title("Multi-section Window")
root.geometry("1200x500")  # Set the size of the window

# Disable resizing for simplicity
root.resizable(False, False)

# First section with buttons
top_frame = tk.Frame(root, height=50)
top_frame.pack(side=tk.TOP, fill=tk.X)

button1 = tk.Button(top_frame, text="Button 1")
button1.pack(side=tk.LEFT, padx=5, pady=5)

button2 = tk.Button(top_frame, text="Button 2")
button2.pack(side=tk.LEFT, padx=5, pady=5)

button3 = tk.Button(top_frame, text="Button 3")
button3.pack(side=tk.LEFT, padx=5, pady=5)

# Second section with Treeview
middle_frame = tk.Frame(root, height=250)
middle_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

treeview = ttk.Treeview(middle_frame)
treeview.pack(expand=True, fill=tk.BOTH)

treeview.bind('<<TreeviewSelect>>', update_text_areas)


# Adding some columns
treeview['columns'] = ("Column1", "Column2")

# Format our columns
treeview.column("#0", width=0, stretch=tk.NO)
treeview.column("Column1", anchor=tk.W, width=345)
treeview.column("Column2", anchor=tk.W, width=345)

# Create Headings
treeview.heading("#0", text="", anchor=tk.W)
treeview.heading("Column1", text="Column 1", anchor=tk.W)
treeview.heading("Column2", text="Column 2", anchor=tk.W)

# Adding some items to the treeview
for i in range(10):
    treeview.insert("", 'end', text="", values=(f"Item {i+1}", f"Value {i+1}"))


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

