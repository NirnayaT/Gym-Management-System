import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime


class MembersManager(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_members_data()

    def create_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel - Member Form
        form_frame = ttk.LabelFrame(self, text="Member Details", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Form Fields
        ttk.Label(form_frame, text="Name:",style="Body.TLabel").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact:",style="Body.TLabel").grid(row=1, column=0, sticky="w")
        self.contact_entry = ttk.Entry(form_frame)
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:",style="Body.TLabel").grid(row=2, column=0, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Membership Type:",style="Body.TLabel").grid(row=3, column=0, sticky="w")
        self.membership_type = ttk.Combobox(
            form_frame, values=["Monthly", "Quarterly", "Yearly"], 
        )
        self.membership_type.grid(row=3, column=1, padx=5, pady=5)

        # Action Buttons
        top_btn_frame = ttk.Frame(form_frame)
        top_btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        
        bottom_btn_frame = ttk.Frame(form_frame)
        bottom_btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(top_btn_frame, text="Add Member", command=self.add_member,style="Primary.TButton").pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(top_btn_frame, text="Update", command=self.update_member,style="Primary.TButton").pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(bottom_btn_frame, text="Delete", command=self.delete_member,style="Primary.TButton").pack(
            side=tk.TOP, padx=10
        )

        # Right Panel - Members List with Search
        list_frame = ttk.LabelFrame(self, text="Members List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        # Search Section
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(search_frame, text="Search", command=self.search_members).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(
            side=tk.LEFT, padx=5
        )

        # Members TreeView
        self.tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Name", "Contact", "Email", "Membership", "Join Date"),
            show="headings",
            height=20,
        )

        # Column Configuration
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Contact", width=120, anchor="w")
        self.tree.column("Email", width=200, anchor="w")
        self.tree.column("Membership", width=100, anchor="center")
        self.tree.column("Join Date", width=100, anchor="center")

        for col in self.tree["columns"]:
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

        self.tree.grid(row=1, column=0, sticky="nsew")
        y_scrollbar.grid(row=1, column=1, sticky="ns")
        x_scrollbar.grid(row=2, column=0, sticky="ew")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_member)

    # Data Operations
    def load_members_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            df = self.db.load_sheet_data("members")
            if not df.empty:
                for _, row in df.iterrows():
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            row["member_id"],
                            row["name"],
                            row["contact"],
                            row["email"],
                            row["membership_type"],
                            row["joining_date"],
                        ),
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")

    def validate_inputs(self):
        required_fields = {
            "Name": self.name_entry.get(),
            "Contact": self.contact_entry.get(),
            "Email": self.email_entry.get(),
            "Membership type": self.membership_type.get(),
        }

        for field, value in required_fields.items():
            if not value:
                messagebox.showwarning("Validation Error", f"{field} is required!")
                return False
        return True

    # CRUD Operations
    def add_member(self):
        if not self.validate_inputs():
            return

        member_data = {
            "name": self.name_entry.get(),
            "contact": self.contact_entry.get(),
            "email": self.email_entry.get(),
            "membership_type": self.membership_type.get(),
            "joining_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Active",
        }

        if self.db.add_member(member_data):
            self.clear_form()
            self.load_members_data()
            messagebox.showinfo("Success", "Member added successfully!")

    def update_member(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a member to update!"
            )
            return

        if not self.validate_inputs():
            return

        item = self.tree.item(selected[0])
        member_id = item["values"][0]

        try:
            df = pd.read_excel(
                self.db.database_file, sheet_name=self.db.sheet_names["members"]
            )

            df.loc[df["member_id"] == member_id, "name"] = self.name_entry.get()
            df.loc[df["member_id"] == member_id, "contact"] = self.contact_entry.get()
            df.loc[df["member_id"] == member_id, "email"] = self.email_entry.get()
            df.loc[df["member_id"] == member_id, "membership_type"] = (
                self.membership_type.get()
            )

            with pd.ExcelWriter(
                self.db.database_file, engine="openpyxl", mode="w"
            ) as writer:
                df.to_excel(
                    writer, sheet_name=self.db.sheet_names["members"], index=False
                )

            self.load_members_data()
            self.clear_form()
            messagebox.showinfo("Success", "Member updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update member: {str(e)}")

    def delete_member(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a member to delete!"
            )
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this member?"
        ):
            item = self.tree.item(selected[0])
            member_id = item["values"][0]

            if self.db.delete_member(member_id):
                self.load_members_data()
                self.clear_form()
                messagebox.showinfo("Success", "Member deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete member")

    # Utility Methods
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.membership_type.set("")

    def on_select_member(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]

            self.clear_form()
            self.name_entry.insert(0, values[1])
            self.contact_entry.insert(0, values[2])
            self.email_entry.insert(0, values[3])
            self.membership_type.set(values[4])

    def search_members(self):
        search_text = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())

        df = self.db.load_sheet_data("members")
        filtered_df = df[
            df["name"].str.lower().str.contains(search_text, na=False)
            | df["email"].str.lower().str.contains(search_text, na=False)
            | df["contact"].astype(str).str.lower().str.contains(search_text, na=False)
        ]

        for _, row in filtered_df.iterrows():
            self.tree.insert(
                "",
                "end",
                values=(
                    row["member_id"],
                    row["name"],
                    row["contact"],
                    row["email"],
                    row["membership_type"],
                    row["joining_date"],
                ),
            )

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_members_data()
