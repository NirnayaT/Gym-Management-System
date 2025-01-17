import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime


class AttendanceManager(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_widgets()
        self.load_attendance_data()

    def create_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel - Check-in/out Form
        form_frame = ttk.LabelFrame(self, text="Attendance Marking", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Member Selection
        ttk.Label(form_frame, text="Member:").grid(row=0, column=0, sticky="w")
        self.member_var = tk.StringVar()
        self.member_combo = ttk.Combobox(
            form_frame, textvariable=self.member_var, state="readonly"
        )
        self.member_combo.grid(row=0, column=1, padx=5, pady=5)
        self.load_members()

        # Control Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(
            btn_frame,
            text="Check In",
            style="Primary.TButton",
            command=self.mark_check_in,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame,
            text="Check Out",
            style="Primary.TButton",
            command=self.mark_check_out,
        ).pack(side=tk.LEFT, padx=5)

        # Right Panel - Attendance List
        list_frame = ttk.LabelFrame(self, text="Today's Attendance", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # Treeview Setup
        self.tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Member", "Check In", "Check Out", "Date", "Duration"),
            show="headings",
            height=20,
        )

        # Column Configuration
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Member", width=180, anchor="w")
        self.tree.column("Check In", width=120, anchor="center")
        self.tree.column("Check Out", width=120, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Duration", width=100, anchor="center")

        # Column Headers
        self.tree.heading("ID", text="ID")
        self.tree.heading("Member", text="Member Name")
        self.tree.heading("Check In", text="Check In Time")
        self.tree.heading("Check Out", text="Check Out Time")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Duration", text="Duration")

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

    def load_members(self):
        try:
            members_df = self.db.load_sheet_data("members")
            active_members = members_df[members_df["status"] == "Active"][
                "name"
            ].tolist()
            self.member_combo["values"] = active_members
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")

    def mark_check_in(self):
        member = self.member_var.get()
        if not member:
            messagebox.showwarning("Selection Required", "Please select a member!")
            return

        try:
            df = self.db.load_sheet_data("attendance")
            today = datetime.now().strftime("%Y-%m-%d")

            # Check for existing check-in
            already_checked_in = (
                df[
                    (df["member_id"] == member)
                    & (df["date"] == today)
                    & (df["check_out"].isnull())
                ].shape[0]
                > 0
            )

            if already_checked_in:
                messagebox.showwarning(
                    "Already Checked In",
                    "This member has already checked in today and hasn't checked out!",
                )
                return

            # Record check-in
            attendance_data = {
                "member_id": member,
                "check_in": datetime.now().strftime("%H:%M:%S"),
                "check_out": None,
                "date": today,
                "duration": None,
            }

            if self.db.mark_attendance(attendance_data):
                self.load_attendance_data()
                messagebox.showinfo("Success", "Check-in marked successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark check-in: {str(e)}")

    def mark_check_out(self):
        member = self.member_var.get()
        if not member:
            messagebox.showwarning("Selection Required", "Please select a member!")
            return

        try:
            df = self.db.load_sheet_data("attendance")
            today = datetime.now().strftime("%Y-%m-%d")

            # Process check-out
            mask = (
                (df["member_id"] == member)
                & (df["date"] == today)
                & (df["check_out"].isnull())
            )
            if not df[mask].empty:
                check_out_time = datetime.now()
                df.loc[mask, "check_out"] = check_out_time.strftime("%H:%M:%S")

                # Calculate duration
                check_in_time = datetime.strptime(
                    df.loc[mask, "check_in"].iloc[0], "%H:%M:%S"
                )
                duration = check_out_time - datetime.combine(
                    check_out_time.date(), check_in_time.time()
                )
                df.loc[mask, "duration"] = str(duration).split(".")[0]

                self.db.save_sheet_data("attendance", df)
                self.load_attendance_data()
                messagebox.showinfo("Success", "Check-out marked successfully!")
            else:
                messagebox.showwarning(
                    "Not Checked In", "Member has not checked in today!"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark check-out: {str(e)}")

    def load_attendance_data(self):
        # Refresh attendance display
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            attendance_df = self.db.load_sheet_data("attendance")
            if not attendance_df.empty:
                for _, row in attendance_df.iterrows():
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            row["id"],
                            row["member_id"],
                            row["check_in"],
                            row["check_out"],
                            row["date"],
                            row["duration"],
                        ),
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load attendance: {str(e)}")
