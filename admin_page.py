import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from db import get_connection
import datetime

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Admin Dashboard",
                 font=("Arial", 22, "bold")).pack(pady=20)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        ttk.Button(btns, text="Add Employee",
                   command=self.add_employee).grid(row=0, column=0, padx=10)

        ttk.Button(btns, text="View Employees",
                   command=self.view_employees).grid(row=0, column=1, padx=10)

        ttk.Button(btns, text="Daily Orders Report",
                   command=self.view_orders_report).grid(row=0, column=2, padx=10)

        ttk.Button(self, text="Back",
                   command=lambda: controller.show_frame("HomePage")
                   ).pack(pady=10)

        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

    def clear(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

    def add_employee(self):
        name = simpledialog.askstring("Name", "Employee name")
        role = simpledialog.askstring("Role", "Employee role")
        if not name or not role:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, role) VALUES (%s,%s)",
            (name, role)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Employee Added")

    def view_employees(self):
        self.clear()
        tree = ttk.Treeview(self.table_frame,
                            columns=("ID", "Name", "Role"),
                            show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Role", text="Role")
        tree.pack(fill="both", expand=True)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, role FROM employees")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    def view_orders_report(self):
        self.clear()
        tree = ttk.Treeview(self.table_frame,
                            columns=("Waiter", "Orders", "Revenue"),
                            show="headings")
        tree.heading("Waiter", text="Waiter")
        tree.heading("Orders", text="Orders")
        tree.heading("Revenue", text="Revenue")
        tree.pack(fill="both", expand=True)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.waiter_name,
                   COUNT(DISTINCT o.token_no),
                   SUM(oi.quantity * m.price)
            FROM orders o
            JOIN order_items oi ON o.token_no=oi.token_no
            JOIN menu m ON oi.food_code=m.food_code
            GROUP BY o.waiter_name
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
