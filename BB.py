import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Prices for each item
prices = {
    "Regular Hot-Dog": 2.50,
    "Cheese Hot-Dog": 3.00,
    "Spicy Hot-Dog": 3.50,
    "Classic Burger": 5.00,
    "Cheese Burger": 5.50,
    "Bacon Burger": 6.00,
    "Regular Fries": 2.00,
    "Curly Fries": 2.50,
    "Sweet Potato Fries": 3.00,
    "Cola": 1.50,
    "Orange Juice": 2.00,
    "Water": 1.00
}

# Order data
order_data = {
    "hotdog": [],
    "burger": [],
    "fries": [],
    "drink": []
}

# Function to update total price
def update_total():
    total = 0.0
    for category in order_data.values():
        for item, qty in category:
            total += prices[item] * qty
    total_label.config(text=f"Total: ${total:.2f}")

# Function to update subtotal for a specific category
def update_subtotal(subtotal_label, category):
    subtotal = 0.0
    for item, qty in order_data[category]:
        subtotal += prices[item] * qty
    subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")

# Function to go back to main menu
def go_back_to_main():
    main_frame.tkraise()

# Function to submit the order
def submit_order():
    name = name_entry.get()
    order = []
    total = 0.0
    
    for category in order_data.values():
        for item, qty in category:
            order.append(f"{item} ({qty})")
            total += prices[item] * qty
    
    if not name:
        messagebox.showerror("Error", "Please enter your name.")
        return
    
    if not order:
        messagebox.showerror("Error", "Please select at least one item.")
        return
    
    order_details = f"Name: {name}\nOrder: {', '.join(order)}\nTotal: ${total:.2f}"
    messagebox.showinfo("Order Details", order_details)

# Function to add items to order
def add_item(category, item, qty_var, subtotal_label):
    qty = int(qty_var.get())
    order_data[category].append((item, qty))
    update_total()
    update_subtotal(subtotal_label, category)

# Function to increase quantity
def increase_qty(qty_var):
    qty = int(qty_var.get())
    qty += 1
    qty_var.set(qty)

# Function to decrease quantity
def decrease_qty(qty_var):
    qty = int(qty_var.get())
    if qty > 0:
        qty -= 1
        qty_var.set(qty)

# Function to clear subtotal for a category
def clear_subtotal(category, subtotal_label):
    order_data[category] = []
    update_total()
    update_subtotal(subtotal_label, category)

# Function to create category frame
def create_category_frame(category, items):
    frame = tk.Frame(root, bg='black')
    
    label = tk.Label(frame, text=f"Select {category.title()}:", fg='white', bg='black', font=("Arial", 24))
    label.pack(pady=20)
    
    subtotal_label = tk.Label(frame, text="Subtotal: $0.00", fg='white', bg='black', font=("Arial", 24))
    subtotal_label.pack(pady=10)
    
    for item in items:
        item_frame = tk.Frame(frame, bg='black')
        item_frame.pack(pady=5)
        
        item_label = tk.Label(item_frame, text=item, fg='white', bg='black', font=("Arial", 18))
        item_label.pack(side='left', padx=20)
        
        qty_var = tk.StringVar(value="0")
        
        decrease_button = tk.Button(item_frame, text="-", command=lambda q=qty_var: decrease_qty(q), bg='white', font=("Arial", 18))
        decrease_button.pack(side='left', padx=10)
        
        qty_entry = tk.Label(item_frame, textvariable=qty_var, fg='white', bg='black', font=("Arial", 18), width=3)
        qty_entry.pack(side='left', padx=10)
        
        increase_button = tk.Button(item_frame, text="+", command=lambda q=qty_var: increase_qty(q), bg='white', font=("Arial", 18))
        increase_button.pack(side='left', padx=10)
        
        add_button = tk.Button(item_frame, text="Add", command=lambda i=item, q=qty_var: add_item(category, i, q, subtotal_label), bg='white', font=("Arial", 18))
        add_button.pack(side='left', padx=10)
    
    clear_subtotal_button = tk.Button(frame, text="Clear Subtotal", command=lambda: clear_subtotal(category, subtotal_label), bg='red', font=("Arial", 18))
    clear_subtotal_button.pack(pady=20)
    
    back_button = tk.Button(frame, text="Back", command=go_back_to_main, bg='white', font=("Arial", 18))
    back_button.pack(pady=20)
    
    return frame

# Function to clear the order
def clear_order():
    global order_data
    order_data = {key: [] for key in order_data}
    update_total()
    main_frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("BIG Baguette Order System")
root.geometry("900x1100")
root.configure(bg='black')

# Create frames
main_frame = tk.Frame(root, bg='black')
main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
hotdog_frame = create_category_frame("hotdog", ["Regular Hot-Dog", "Cheese Hot-Dog", "Spicy Hot-Dog"])
burger_frame = create_category_frame("burger", ["Classic Burger", "Cheese Burger", "Bacon Burger"])
fries_frame = create_category_frame("fries", ["Regular Fries", "Curly Fries", "Sweet Potato Fries"])
drink_frame = create_category_frame("drink", ["Cola", "Orange Juice", "Water"])

# Add an image at the top of the window
try:
    image = Image.open("BB.png")  # Update the image path
    image = image.resize((500, 150))
    photo = ImageTk.PhotoImage(image)
    # Add image to the main_frame
    image_label = tk.Label(main_frame, image=photo, bg='black')
    image_label.image = photo  # Keep a reference to the image
    image_label.grid(row=0, columnspan=2, pady=10)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load image: {e}")

# User name entry
name_label = tk.Label(main_frame, text="Name:", fg='white', bg='black', font=("Arial", 24))
name_label.grid(row=1, column=0, pady=20, padx=10, sticky='e')
name_entry = tk.Entry(main_frame, font=("Arial", 24))
name_entry.grid(row=1, column=1, pady=20, padx=10, sticky='w')

# Main menu buttons
hotdog_button = tk.Button(main_frame, text="Hot-Dog", command=hotdog_frame.tkraise, bg='white', font=("Arial", 24))
hotdog_button.grid(row=2, columnspan=2, pady=20, padx=10)
burger_button = tk.Button(main_frame, text="Hamburger", command=burger_frame.tkraise, bg='white', font=("Arial", 24))
burger_button.grid(row=3, columnspan=2, pady=20, padx=10)
fries_button = tk.Button(main_frame, text="French Fries", command=fries_frame.tkraise, bg='white', font=("Arial", 24))
fries_button.grid(row=4, columnspan=2, pady=20, padx=10)
drinks_button = tk.Button(main_frame, text="Drinks", command=drink_frame.tkraise, bg='white', font=("Arial", 24))
drinks_button.grid(row=5, columnspan=2, pady=20, padx=10)

# Total label
total_label = tk.Label(main_frame, text="Total: $0.00", fg='white', bg='black', font=("Arial", 24))
total_label.grid(row=6, columnspan=2, pady=20)

# Submit button
submit_button = tk.Button(main_frame, text="Submit Order", command=submit_order, bg='white', font=("Arial", 24))
submit_button.grid(row=7, columnspan=2, pady=20)

# Clear order button
clear_button = tk.Button(main_frame, text="Clear Order", command=clear_order, bg='red', font=("Arial", 24))
clear_button.grid(row=8, columnspan=2, pady=20)

# Place frames in the same position
for frame in [main_frame, hotdog_frame, burger_frame, fries_frame, drink_frame]:
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Raise the main frame at the start
main_frame.tkraise()

# Run the application
root.mainloop()
