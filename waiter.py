import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from db import get_connection
import datetime
from menupage import MenuPage


class WaiterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Waiter Panel", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Waiter ID").pack()
        self.wid = tk.Entry(self)
        self.wid.pack()

        tk.Label(self, text="Table Number").pack()
        self.table = tk.Entry(self)
        self.table.pack()

        # Selected items list
        tk.Label(self, text="Selected Items").pack(pady=5)
        self.order_listbox = tk.Listbox(self, height=8)
        self.order_listbox.pack(fill="x", padx=20)

        ttk.Button(self, text="Open Menu", command=self.open_menu).pack(pady=5)
        ttk.Button(self, text="Submit Order", command=self.submit_order).pack(pady=5)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("HomePage")
        ).pack(pady=10)

        # Temporary order storage
        self.selected_items = []

    # ---------------- Open Menu ----------------
    def open_menu(self):
        MenuPage(self, self.add_item)

    # ---------------- Add Item from Menu ----------------
    def add_item(self, item_str):
        self.selected_items.append(item_str)
        self.order_listbox.insert(tk.END, item_str)

    # ---------------- Submit Order ----------------
    def submit_order(self):
        if not self.selected_items:
            messagebox.showwarning("Warning", "No items selected!")
            return

        conn = get_connection()
        cur = conn.cursor()

        # Check existing pending order
        cur.execute(
            "SELECT token_no FROM orders "
            "WHERE waiter_id=%s AND table_no=%s AND order_date=%s AND status='PENDING'",
            (self.wid.get(), self.table.get(), datetime.date.today())
        )
        row = cur.fetchone()

        if row:
            token_no = row[0]
        else:
            # Create new order (NO waiter_name)
            cur.execute(
                "INSERT INTO orders (waiter_id, table_no, order_date, status) "
                "VALUES (%s,%s,%s,%s)",
                (self.wid.get(), self.table.get(), datetime.date.today(), "PENDING")
            )
            conn.commit()
            token_no = cur.lastrowid

        # Insert items
        for item in self.selected_items:
            food_code = int(item.split("|")[0].strip())
            food_name = item.split("|")[1].strip()

            qty = simpledialog.askinteger(
                "Quantity",
                f"Enter quantity for {food_name}:",
                minvalue=1
            )

            if qty:
                cur.execute(
                    "INSERT INTO order_items (token_no, food_code, quantity) "
                    "VALUES (%s,%s,%s)",
                    (token_no, food_code, qty)
                )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            f"Order Submitted!\nToken No: {token_no}"
        )

        self.selected_items.clear()
        self.order_listbox.delete(0, tk.END)
