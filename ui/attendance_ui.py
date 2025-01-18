import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pandas as pd
from datetime import datetime

class AttendanceManager(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        self.create_widgets()
        self.load_attendance_data()

    def create_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel with Calendar and Check-in Form
        left_frame = ttk.LabelFrame(self, text="Attendance Management", padding=15)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Calendar
        self.cal = Calendar(left_frame, selectmode='day', date_pattern='y-mm-dd')
        self.cal.grid(row=0, column=0, padx=5, pady=5)
        self.cal.bind('<<CalendarSelected>>', self.on_date_select)

        # Member Selection
        form_frame = ttk.Frame(left_frame)
        form_frame.grid(row=1, column=0, pady=10)

        ttk.Label(form_frame, text="Member:",style="Body.TLabel").grid(row=0, column=0, sticky="w")
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
        list_frame = ttk.LabelFrame(self, text="Attendance Records", padding=15)
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

    def on_date_select(self, event):
        self.selected_date = self.cal.get_date()
        self.load_attendance_data(self.selected_date)

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
            today = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")

            attendance_data = {
                "member_id": member,
                "check_in": current_time,
                "check_out": None,
                "date": today,
                "duration": None
            }

            if self.db.mark_attendance(attendance_data):
                # Refresh to show today's attendance
                self.load_attendance_data(today)
                self.cal.selection_set(today)  # Highlight today in calendar
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

            # Get member's actual ID from members sheet
            members_df = self.db.load_sheet_data("members")
            member_row = members_df[members_df["name"] == member]
            if not member_row.empty:
                actual_member_id = member_row.iloc[0]["member_id"]
                
                # Find member's active check-in using actual ID
                mask = (
                    (df["member_id"] == actual_member_id) & 
                    (df["date"] == today) & 
                    (df["check_out"].isnull())
                )

                if not df[mask].empty:
                    check_out_time = datetime.now()
                    df.loc[mask, "check_out"] = check_out_time.strftime("%H:%M:%S")

                    check_in_time = datetime.strptime(df.loc[mask, "check_in"].iloc[0], "%H:%M:%S")
                    duration = check_out_time - datetime.combine(check_out_time.date(), check_in_time.time())
                    df.loc[mask, "duration"] = str(duration).split(".")[0]

                    if self.db.save_sheet_data("attendance", df):
                        self.load_attendance_data(today)
                        messagebox.showinfo("Success", "Check-out marked successfully!")
                else:
                    messagebox.showwarning("Not Checked In", "Member has not checked in today!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark check-out: {str(e)}")

 # In attendance_ui.py
    def load_attendance_data(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:       
            # Get attendance records
            attendance_df = self.db.get_attendance_history(date=date)
            
            if not attendance_df.empty:
                # Get member names from members sheet
                members_df = self.db.load_sheet_data("members")
                
                # Map member_id to member names for display
                for _, row in attendance_df.iterrows():
                    member_name = members_df[members_df["member_id"] == row["member_id"]]["name"].iloc[0]
                    self.tree.insert("", "end", values=(
                        row["member_id"],
                        member_name,  # Display actual member_id
                        row["check_in"],
                        row["check_out"],
                        row["date"],
                        row["duration"]
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load attendance: {str(e)}")
