import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


class ChefPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(
            self,
            text="Chef Panel",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Treeview for pending orders
        columns = ("Token", "Table", "Items")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Mark as READY",
                   command=self.mark_ready).grid(row=0, column=0, padx=10)

        ttk.Button(btn_frame, text="Refresh",
                   command=self.load_orders).grid(row=0, column=1, padx=10)

        # ✅ Use string "HomePage" instead of importing HomePage
        ttk.Button(btn_frame, text="Back",
                   command=lambda: controller.show_frame("HomePage")
                   ).grid(row=0, column=2, padx=10)

        self.load_orders()

    # ---------------- Load pending orders ----------------
    def load_orders(self):
        conn = get_connection()
        cur = conn.cursor()

        # Clear treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        cur.execute(
            "SELECT token_no, table_no FROM orders "
            "WHERE status='PENDING' ORDER BY token_no"
        )
        orders = cur.fetchall()

        for token_no, table_no in orders:
            cur.execute(
                "SELECT m.food_name, oi.quantity "
                "FROM order_items oi "
                "JOIN menu m ON oi.food_code = m.food_code "
                "WHERE oi.token_no=%s",
                (token_no,)
            )
            items = cur.fetchall()
            items_str = ", ".join([f"{name} x{qty}" for name, qty in items])

            self.tree.insert(
                "",
                tk.END,
                values=(token_no, table_no, items_str)
            )

        conn.close()

    # ---------------- Mark order READY ----------------
    def mark_ready(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order")
            return

        token_no = self.tree.item(selected[0])["values"][0]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE orders SET status='READY' WHERE token_no=%s",
            (token_no,)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Order Ready",
            f"Token {token_no} marked as READY"
        )

        self.load_orders()
