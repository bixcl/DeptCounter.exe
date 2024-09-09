import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class DebtReturnCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Debt Return Counter")

        self.data_file = "debt_data.json"
        self.profiles = {}
        self.current_profile = "one"

        # Set dark theme
        self.root.configure(bg='black')

        # Initialize UI components
        self.initialize_ui()

        self.load_data()

    def initialize_ui(self):
        # Profile selection
        tk.Label(self.root, text="Select Profile:", bg='black', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.profile_var = tk.StringVar(self.root)
        self.profile_menu = ttk.Combobox(self.root, textvariable=self.profile_var)
        self.profile_menu.grid(row=0, column=1, padx=10, pady=10)
        self.profile_menu.bind("<<ComboboxSelected>>", self.switch_profile)
        
        # Labels and entries
        tk.Label(self.root, text="Total Debt:", bg='black', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.entry_total_debt = tk.Entry(self.root, bg='gray20', fg='white')
        self.entry_total_debt.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Payment Amount:", bg='black', fg='white').grid(row=2, column=0, padx=10, pady=10)
        self.entry_payment = tk.Entry(self.root, bg='gray20', fg='white')
        self.entry_payment.grid(row=2, column=1, padx=10, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=3, columnspan=2, pady=10)
        self.progress.configure(style='black.Horizontal.TProgressbar')
        style = ttk.Style()
        style.configure('black.Horizontal.TProgressbar', background='white')

        # Buttons
        self.btn_set_debt = tk.Button(self.root, text="Set Total Debt", command=self.set_total_debt, bg='gray30', fg='white')
        self.btn_set_debt.grid(row=4, column=0, padx=10, pady=10)

        self.btn_add_payment = tk.Button(self.root, text="Add Payment", command=self.add_payment, bg='gray30', fg='white')
        self.btn_add_payment.grid(row=4, column=1, padx=10, pady=10)

        self.btn_reset = tk.Button(self.root, text="Reset Profile", command=self.reset_profile, bg='gray30', fg='white')
        self.btn_reset.grid(row=5, columnspan=2, pady=10)

        # Result labels
        self.label_remaining_debt = tk.Label(self.root, text="Remaining Debt: $0.00", bg='black', fg='white')
        self.label_remaining_debt.grid(row=6, columnspan=2, pady=10)

        self.label_percentage = tk.Label(self.root, text="Debt Repaid: 0%", bg='black', fg='white')
        self.label_percentage.grid(row=7, columnspan=2, pady=10)

    def switch_profile(self, event=None):
        self.current_profile = self.profile_var.get()
        self.update_display()

    def set_total_debt(self):
        try:
            total_debt = float(self.entry_total_debt.get())
            if self.current_profile not in self.profiles:
                self.profiles[self.current_profile] = {"total_debt": 0, "paid_amount": 0}
            self.profiles[self.current_profile]['total_debt'] = total_debt
            self.profiles[self.current_profile]['paid_amount'] = 0
            self.save_data()
            self.update_display()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the total debt.")

    def add_payment(self):
        try:
            payment = float(self.entry_payment.get())
            if payment <= 0:
                raise ValueError("Payment should be a positive number.")
            if self.current_profile not in self.profiles:
                self.profiles[self.current_profile] = {"total_debt": 0, "paid_amount": 0}
            self.profiles[self.current_profile]['paid_amount'] += payment
            if self.profiles[self.current_profile]['paid_amount'] > self.profiles[self.current_profile]['total_debt']:
                self.profiles[self.current_profile]['paid_amount'] = self.profiles[self.current_profile]['total_debt']
            self.save_data()
            self.update_display()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the payment.")

    def reset_profile(self):
        if self.current_profile in self.profiles:
            self.profiles[self.current_profile] = {"total_debt": 0, "paid_amount": 0}
            self.save_data()
            self.update_display()
        else:
            messagebox.showwarning("Profile Error", "The selected profile does not exist.")

    def get_repaid_percentage(self):
        profile_data = self.profiles.get(self.current_profile, {"total_debt": 0, "paid_amount": 0})
        total_debt = profile_data['total_debt']
        if total_debt == 0:
            return 0
        return (profile_data['paid_amount'] / total_debt) * 100

    def update_display(self):
        profile_data = self.profiles.get(self.current_profile, {"total_debt": 0, "paid_amount": 0})
        if isinstance(profile_data, dict):
            remaining_debt = profile_data['total_debt'] - profile_data['paid_amount']
            if hasattr(self, 'label_remaining_debt'):
                self.label_remaining_debt.config(text=f"Remaining Debt: ${remaining_debt:.2f}")
            if hasattr(self, 'label_percentage'):
                percentage = self.get_repaid_percentage()
                self.label_percentage.config(text=f"Debt Repaid: {percentage:.2f}%")
                self.progress['value'] = percentage
        self.profile_var.set(self.current_profile)

    def update_profile_menu(self):
        if hasattr(self, 'profile_menu'):
            self.profile_menu['values'] = list(self.profiles.keys())
            if self.current_profile not in self.profiles:
                self.current_profile = list(self.profiles.keys())[0] if self.profiles else "one"
            self.profile_var.set(self.current_profile)
            self.update_display()

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.profiles, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                try:
                    self.profiles = json.load(f)
                except json.JSONDecodeError:
                    self.profiles = {}
        if not self.profiles:
            self.profiles = {
                "one": {"total_debt": 0, "paid_amount": 0},
                "two": {"total_debt": 0, "paid_amount": 0},
                "three": {"total_debt": 0, "paid_amount": 0},
                "four": {"total_debt": 0, "paid_amount": 0},
                "five": {"total_debt": 0, "paid_amount": 0}
            }
        # Update the profile menu after initialization
        self.update_profile_menu()

# Running the app
root = tk.Tk()
app = DebtReturnCounter(root)
root.mainloop()
