import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class OrderManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Order Management System")

        # Customer Info
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky=tk.E)
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=0, column=1)

        self.label_shipping = tk.Label(master, text="Shipping:")
        self.label_shipping.grid(row=1, column=0, sticky=tk.E)
        self.entry_shipping = tk.Entry(master)
        self.entry_shipping.grid(row=1, column=1)

        self.label_phone = tk.Label(master, text="Phone:")
        self.label_phone.grid(row=2, column=0, sticky=tk.E)
        self.entry_phone = tk.Entry(master)
        self.entry_phone.grid(row=2, column=1)

        # Order Details
        self.label_order = tk.Label(master, text="Order:")
        self.label_order.grid(row=3, column=0, sticky=tk.E)
        self.entry_order = tk.Entry(master)
        self.entry_order.grid(row=3, column=1)

        # Buttons
        self.button_submit = tk.Button(master, text="Submit Order", command=self.submit_order)
        self.button_submit.grid(row=4, columnspan=2)

        # Orders Treeview
        self.orders_tree = ttk.Treeview(master, columns=("Name", "Shipping", "Phone", "Order"))
        self.orders_tree.heading("#0", text="ID")
        self.orders_tree.heading("Name", text="Name")
        self.orders_tree.heading("Shipping", text="Shipping")
        self.orders_tree.heading("Phone", text="Phone")
        self.orders_tree.heading("Order", text="Order")
        self.orders_tree.grid(row=5, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        # Load orders from JSON file
        self.load_orders()

    def submit_order(self):
        name = self.entry_name.get()
        shipping = self.entry_shipping.get()
        phone = self.entry_phone.get()
        order = self.entry_order.get()

        if name or shipping or phone or order:
            order_data = {
                "Name": name,
                "Shipping": shipping,
                "Phone": phone,
                "Order": order
            }
            self.save_order(order_data)
            messagebox.showinfo("Success", "Order placed successfully!")
            self.clear_fields()
            self.load_orders()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def save_order(self, order_data):
        file_path = os.path.join(os.path.dirname(__file__), "orders.json")
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump([], file)
        
        with open(file_path, "r+") as file:
            try:
                orders = json.load(file)
            except json.decoder.JSONDecodeError:
                orders = []

            orders.append(order_data)
            file.seek(0)
            json.dump(orders, file, indent=4)

    def load_orders(self):
        file_path = os.path.join(os.path.dirname(__file__), "orders.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    orders = json.load(file)
                except json.decoder.JSONDecodeError:
                    orders = []
            self.display_orders(orders)


    def display_orders(self, orders):
        # Clear existing items in the Treeview
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Insert new orders into the Treeview
        for idx, order in enumerate(orders, start=1):
            self.orders_tree.insert("", tk.END, text=str(idx), values=(order["Name"], order["Shipping"], order["Phone"], order["Order"]))

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_shipping.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_order.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()