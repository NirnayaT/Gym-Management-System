import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime


class PaymentsManager(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_widgets()
        self.load_payments_data()

    def create_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel - Payment Form
        form_frame = ttk.LabelFrame(self, text="Payment Details", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Member Selection
        ttk.Label(form_frame, text="Member:").grid(row=0, column=0, sticky="w")
        self.member_var = tk.StringVar()
        self.member_combo = ttk.Combobox(form_frame, textvariable=self.member_var)
        self.member_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.load_members()

        # Amount Entry
        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Payment Type Selection
        ttk.Label(form_frame, text="Payment Type:").grid(row=2, column=0, sticky="w")
        self.payment_type = ttk.Combobox(
            form_frame, values=["Cash", "Card", "Esewa", "Bank Transfer"]
        )
        self.payment_type.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Payment Status Selection
        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="w")
        self.payment_status = ttk.Combobox(
            form_frame, values=["Completed", "Pending", "Failed"]
        )
        self.payment_status.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Action Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Add Payment", command=self.add_payment).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(
            side=tk.LEFT, padx=5
        )

        # Right Panel - Payments List
        list_frame = ttk.LabelFrame(self, text="Payment History", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # Payment History TreeView
        self.tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Member", "Amount", "Date", "Type", "Status"),
            show="headings",
            height=20,
        )

        # Configure columns
        columns_config = {
            "ID": (80, "center"),
            "Member": (150, "w"),
            "Amount": (100, "e"),
            "Date": (150, "center"),
            "Type": (100, "center"),
            "Status": (100, "center"),
        }

        for col, (width, anchor) in columns_config.items():
            self.tree.column(col, width=width, anchor=anchor)
            self.tree.heading(col, text=col)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        x_scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set
        )

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

    # Data loading methods
    def load_members(self):
        try:
            members_df = self.db.load_sheet_data("members")
            active_members = members_df[members_df["status"] == "Active"][
                "name"
            ].tolist()
            self.member_combo["values"] = active_members
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")

    def load_payments_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            payments_df = self.db.load_sheet_data("payments")
            if not payments_df.empty:
                for _, row in payments_df.iterrows():
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            row["payment_id"],
                            row["member_name"],
                            f"Rs. {row['amount']:.2f}",
                            row["payment_date"],
                            row["payment_type"],
                            row["status"],
                        ),
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {str(e)}")

    # Payment operations
    def add_payment(self):
        if not self.validate_payment():
            return

        try:
            payment_data = {
                "member_name": self.member_var.get(),
                "amount": float(self.amount_entry.get()),
                "payment_type": self.payment_type.get(),
                "status": self.payment_status.get(),
            }

            if self.db.add_payment(payment_data):
                self.clear_form()
                self.load_payments_data()
                messagebox.showinfo("Success", "Payment recorded successfully!")
            else:
                messagebox.showerror("Error", "Failed to record payment")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def validate_payment(self):
        required_fields = {
            "member": self.member_var.get(),
            "amount": self.amount_entry.get(),
            "payment type": self.payment_type.get(),
            "status": self.payment_status.get(),
        }

        for field, value in required_fields.items():
            if not value:
                messagebox.showwarning(
                    "Validation Error", f"{field.title()} is required!"
                )
                return False
        return True

    def clear_form(self):
        self.member_var.set("")
        self.amount_entry.delete(0, tk.END)
        self.payment_type.set("")
        self.payment_status.set("")
