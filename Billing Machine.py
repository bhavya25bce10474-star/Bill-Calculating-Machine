import tkinter as tk
from tkinter import messagebox, simpledialog
import math

# --- Data Setup ---
items = {
    "101": {"name": "Soap", "mrp": 30, "qty": 20},
    "102": {"name": "Shampoo", "mrp": 120, "qty": 20},
    "103": {"name": "Chips", "mrp": 20, "qty": 20},
    "104": {"name": "Biscuits", "mrp": 15, "qty": 20},
    "105": {"name": "ToothPaste", "mrp": 60, "qty": 20},
    "106": {"name": "ToothBrush", "mrp": 30, "qty": 20},
    "107": {"name": "Deodrant", "mrp": 150, "qty": 20},
    "108": {"name": "Detergant", "mrp": 50, "qty": 20},
    "109": {"name": "FloorCleaner", "mrp": 110, "qty": 20},
    "110": {"name": "Mosquito Repellant", "mrp": 120, "qty": 20},
}

admin_username = "bhavya"
admin_password = "bhavya204"


def get_discount(total):
    if total >= 500:
        return 0.20
    elif total >= 200:
        return 0.10
    elif total >= 100:
        return 0.05
    else:
        return 0.0


def check_membership_code(code):
    # Membership code: one or more letters (name) + exactly 10 digits (phone)
    import re
    return bool(re.fullmatch(r"[A-Za-z]+\d{10}", code))


class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shop Bill Calculator")
        self.bill = []
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Shop Bill Calculator", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Billing", command=self.billing_page, width=20).pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_login, width=20).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def billing_page(self):
        self.clear_window()
        tk.Label(self.root, text="Billing Page", font=("Arial", 14)).pack(pady=10)

        self.code_var = tk.StringVar()
        self.qty_var = tk.StringVar()

        tk.Label(self.root, text="Item Code:").pack()
        tk.Entry(self.root, textvariable=self.code_var).pack()

        tk.Label(self.root, text="Quantity:").pack()
        tk.Entry(self.root, textvariable=self.qty_var).pack()

        tk.Button(self.root, text="Add Item", command=self.add_to_bill).pack(pady=5)
        tk.Button(self.root, text="Generate Bill", command=self.show_bill_summary).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)
        self.bill_box = tk.Listbox(self.root, width=40)
        self.bill_box.pack(pady=5)

    def add_to_bill(self):
        code = self.code_var.get()
        qty = self.qty_var.get()
        if code not in items:
            messagebox.showerror("Error", "Invalid item code.")
            return
        try:
            qty = int(qty)
        except:
            messagebox.showerror("Error", "Enter a numeric quantity.")
            return
        if qty <= 0 or qty > items[code]['qty']:
            messagebox.showerror("Error", "Not enough stock or invalid quantity.")
            return
        self.bill.append((code, items[code]['name'], items[code]['mrp'], qty))
        items[code]['qty'] -= qty
        self.bill_box.insert(tk.END, f"{items[code]['name']} ({qty}) - ₹{items[code]['mrp']} x {qty}")
        self.code_var.set("")
        self.qty_var.set("")

    def show_bill_summary(self):
        bill_text = ""
        total = 0
        for entry in self.bill:
            code, name, mrp, qty = entry
            line_total = mrp * qty
            total += line_total
            bill_text += f"{name} (Code: {code}) - {qty} x ₹{mrp} = ₹{line_total}\n"
        discount_rate = get_discount(total)
        discount_amount = total * discount_rate
        grand_total = total - discount_amount

        # Membership Dialogue
        is_member = messagebox.askyesno("Membership", "Are you a member?")
        member_discount_applied = False
        if is_member:
            customer_name = simpledialog.askstring("Membership", "Enter customer name (letters only):")
            customer_phone = simpledialog.askstring("Membership", "Enter phone number (10 digits):")
            if customer_name and customer_phone and check_membership_code(customer_name + customer_phone):
                membership_code = customer_name + customer_phone
                membership_discount = 0.10
                additional_discount_amount = grand_total * membership_discount
                grand_total -= additional_discount_amount
                bill_text += f"\nMembership Discount (10%): ₹{round(additional_discount_amount, 2)}"
                member_discount_applied = True
            else:
                messagebox.showinfo("Membership", "Invalid customer name or phone. No extra discount applied.")
        bill_text += f"\nSubtotal: ₹{total}\nDiscount ({int(discount_rate * 100)}%): ₹{round(discount_amount, 2)}\n"
        if not member_discount_applied and is_member:
            bill_text += f"Membership Discount: INVALID\n"
        bill_text += f"Total Bill: ₹{round(grand_total, 2)}"
        messagebox.showinfo("Bill Summary", bill_text)
        self.bill.clear()
        self.bill_box.delete(0, tk.END)

    def admin_login(self):
        uname = simpledialog.askstring("Admin Login", "Username:")
        pwd = simpledialog.askstring("Admin Login", "Password:", show='*')
        if uname == admin_username and pwd == admin_password:
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials.")

    def admin_panel(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Panel", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Add New Item", command=self.add_item_page, width=25).pack(pady=3)
        tk.Button(self.root, text="Update Inventory", command=self.update_inventory_page, width=25).pack(pady=3)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory, width=25).pack(pady=3)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=25).pack(pady=3)

    def add_item_page(self):
        code = simpledialog.askstring("Add Item", "Enter Item Code:")
        name = simpledialog.askstring("Add Item", "Enter Item Name:")
        mrp = simpledialog.askinteger("Add Item", "Enter Item MRP:")
        qty = simpledialog.askinteger("Add Item", "Starting Quantity:")
        if code in items:
            messagebox.showerror("Error", "Item code exists!")
        else:
            items[code] = {"name": name, "mrp": mrp, "qty": qty}
            messagebox.showinfo("Success", f"Item {name} added.")

    def update_inventory_page(self):
        code = simpledialog.askstring("Update Inventory", "Item Code to Update:")
        if code in items:
            more = simpledialog.askinteger("Update Inventory",
                                           f"Quantity to add to {items[code]['name']} (Current: {items[code]['qty']}):")
            items[code]['qty'] += more
            messagebox.showinfo("Success", f"Inventory updated. New quantity: {items[code]['qty']}")
        else:
            messagebox.showerror("Error", "Code not found.")

    def view_inventory(self):
        inv_text = ""
        for code, info in items.items():
            inv_text += f"{code}: {info['name']} | MRP: ₹{info['mrp']} | Qty: {info['qty']}\n"
        messagebox.showinfo("Inventory", inv_text)


# --- Launch App ---
root = tk.Tk()
app = ShopApp(root)
root.mainloop()
