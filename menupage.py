import tkinter as tk
from tkinter import ttk

class MenuPage(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)

        self.title("The Mill - Menu")
        self.geometry("500x400")
        self.callback = callback

        tk.Label(self, text="Search Food (Name / Code)").pack(pady=5)

        self.search = tk.Entry(self)  
        self.search.pack(fill="x", padx=10)
        self.search.bind("<KeyRelease>", self.search_food)

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(frame)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Select", command=self.select_item).pack(pady=10)

        self.load_menu()

    # ---------------- Methods ----------------
    def load_menu(self):
        from db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT food_code, food_name, price FROM menu")
        self.menu_data = cur.fetchall()
        self.show_list(self.menu_data)
        conn.close()

    def show_list(self, data):
        self.listbox.delete(0, tk.END)
        for item in data:
            self.listbox.insert(tk.END, f"{item[0]} | {item[1]} | ₹{item[2]}")

    def search_food(self, event):
        key = self.search.get().lower()
        filtered = [
            item for item in self.menu_data
            if key in str(item[0]).lower() or key in item[1].lower()
        ]
        self.show_list(filtered)

    def select_item(self):
        selected = self.listbox.get(tk.ACTIVE)
        if selected:
            self.callback(selected)
            self.destroy()
