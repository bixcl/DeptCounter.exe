import tkinter as tk
from tkinter import messagebox

def calculate_remaining_debt():
    try:
        total_debt = float(entry_total_debt.get())
        interest_rate = float(entry_interest_rate.get()) / 100
        monthly_payment = float(entry_monthly_payment.get())
        
        months = 0
        while total_debt > 0:
            interest = total_debt * (interest_rate / 12)
            total_debt += interest
            total_debt -= monthly_payment
            months += 1
            
            if total_debt <= 0:
                total_debt = 0
                break

        label_result.config(text=f"Debt will be paid off in {months} months.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Creating the main window
root = tk.Tk()
root.title("Debt Return Counter")

# Labels and entries
tk.Label(root, text="Total Debt:").grid(row=0, column=0)
entry_total_debt = tk.Entry(root)
entry_total_debt.grid(row=0, column=1)

tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0)
entry_interest_rate = tk.Entry(root)
entry_interest_rate.grid(row=1, column=1)

tk.Label(root, text="Monthly Payment:").grid(row=2, column=0)
entry_monthly_payment = tk.Entry(root)
entry_monthly_payment.grid(row=2, column=1)

# Calculate button
btn_calculate = tk.Button(root, text="Calculate", command=calculate_remaining_debt)
btn_calculate.grid(row=3, columnspan=2)

# Result label
label_result = tk.Label(root, text="Debt will be paid off in: ")
label_result.grid(row=4, columnspan=2)

# Run the application
root.mainloop()