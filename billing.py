import tkinter as tk
from tkinter import ttk
from db import get_connection

class BillingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Billing Dashboard", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Enter Table Number").pack()
        self.table_no = tk.Entry(self)
        self.table_no.pack()

        ttk.Button(self, text="Generate Bill", command=self.generate_bill).pack(pady=10)

        self.bill_text = tk.Text(self, height=20)
        self.bill_text.pack(fill="both", expand=True, pady=10)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("HomePage")  # ✅ String use kiya
        ).pack(pady=5)

    def generate_bill(self):
        table = self.table_no.get()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT o.token_no, m.food_name, oi.quantity, m.price "
            "FROM orders o "
            "JOIN order_items oi ON o.token_no=oi.token_no "
            "JOIN menu m ON oi.food_code=m.food_code "
            "WHERE o.table_no=%s AND o.status IN ('READY','SERVED')",
            (table,)
        )

        items = cur.fetchall()
        self.bill_text.delete(1.0, tk.END)

        if not items:
            self.bill_text.insert(tk.END, "No ready orders for this table.")
            conn.close()
            return

        total = 0
        self.bill_text.insert(
            tk.END,
            f"------ The Mill Restaurant ------\nTable No: {table}\n\n"
        )
        self.bill_text.insert(tk.END, "Item\tQty\tPrice\tAmount\n")
        self.bill_text.insert(tk.END, "-" * 40 + "\n")

        for token, name, qty, price in items:
            amount = qty * price
            total += amount
            self.bill_text.insert(
                tk.END,
                f"{name}\t{qty}\t{price}\t{amount}\n"
            )

        gst = total * 0.05
        grand_total = total + gst

        self.bill_text.insert(tk.END, "-" * 40 + "\n")
        self.bill_text.insert(
            tk.END,
            f"Subtotal: {total}\nGST 5%: {gst}\nTotal: {grand_total}\n"
        )
        self.bill_text.insert(tk.END, "-------------------------------\n")
        self.bill_text.insert(tk.END, "Thank you for visiting The Mill!\n")

        conn.close()
