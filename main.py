# main.py
import tkinter as tk
from tkinter import ttk
from admin_page import AdminPage
from chefPage import ChefPage
from billing import BillingPage
from waiter import WaiterPage
from menupage import MenuPage  

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="THE MILL", font=("Arial", 28, "bold")).pack(pady=40)

        ttk.Button(self, text="Admin Page",
                   command=lambda: controller.show_frame("AdminPage")).pack(pady=10)
        ttk.Button(self, text="Waiter Page",
                   command=lambda: controller.show_frame("WaiterPage")).pack(pady=10)
        ttk.Button(self, text="Chef Page",
                   command=lambda: controller.show_frame("ChefPage")).pack(pady=10)
        ttk.Button(self, text="Billing Page",
                   command=lambda: controller.show_frame("BillingPage")).pack(pady=10)
        ttk.Button(self, text="Exit", command=controller.destroy).pack(pady=10)

class TheMillApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Mill Cafe Management")
        self.geometry("900x600")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Sab pages register karo
        for F in (HomePage, AdminPage, WaiterPage, ChefPage, BillingPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = TheMillApp()
    app.mainloop()
