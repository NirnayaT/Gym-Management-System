import pandas as pd
import os
from datetime import datetime


class ExcelDatabase:
    def __init__(self):
        # Database configuration
        self.database_file = "database/gym_database.xlsx"
        self.sheet_names = {
            "members": "Members",
            "payments": "Payments",
            "attendance": "Attendance",
        }

        os.makedirs("database", exist_ok=True)
        self.initialize_database()

    def initialize_database(self):
        # Create new database if not exists
        if not os.path.exists(self.database_file):
            with pd.ExcelWriter(
                self.database_file, engine="openpyxl", mode="w"
            ) as writer:
                # Initialize sheets with columns
                pd.DataFrame(
                    columns=[
                        "member_id",
                        "name",
                        "contact",
                        "email",
                        "membership_type",
                        "joining_date",
                        "status",
                    ]
                ).to_excel(writer, sheet_name=self.sheet_names["members"], index=False)

                pd.DataFrame(
                    columns=[
                        "payment_id",
                        "member_name",
                        "amount",
                        "payment_date",
                        "payment_type",
                        "status",
                    ]
                ).to_excel(writer, sheet_name=self.sheet_names["payments"], index=False)

                pd.DataFrame(
                    columns=[
                        "id",
                        "member_id",
                        "check_in",
                        "check_out",
                        "date",
                        "duration",
                    ]
                ).to_excel(
                    writer, sheet_name=self.sheet_names["attendance"], index=False
                )

    def load_sheet_data(self, sheet_name):
        # Load data from specified sheet
        if not os.path.exists(self.database_file):
            self.initialize_database()
            return pd.DataFrame()

        try:
            return pd.read_excel(
                self.database_file, sheet_name=self.sheet_names[sheet_name]
            )
        except Exception as e:
            print(f"Error loading {sheet_name} data: {e}")
            return pd.DataFrame()

    def save_sheet_data(self, sheet_name, df):
        # Save data to specified sheet
        try:
            excel_data = {}
            if os.path.exists(self.database_file):
                excel_data = pd.read_excel(self.database_file, sheet_name=None)

            excel_data[self.sheet_names[sheet_name]] = df

            with pd.ExcelWriter(
                self.database_file, engine="openpyxl", mode="w"
            ) as writer:
                for name, data in excel_data.items():
                    data.to_excel(writer, sheet_name=name, index=False)
            return True
        except Exception as e:
            print(f"Error saving {sheet_name} data: {e}")
            return False

    def add_member(self, member_data):
        # Add new member record
        df = self.load_sheet_data("members")
        member_data["member_id"] = len(df) + 1 if not df.empty else 1
        member_data["joining_date"] = datetime.now().strftime("%Y-%m-%d")
        member_data["status"] = "Active"
        df = pd.concat([df, pd.DataFrame([member_data])], ignore_index=True)
        return self.save_sheet_data("members", df)

    def add_payment(self, payment_data):
        # Add new payment record
        df = self.load_sheet_data("payments")
        payment_data["payment_id"] = len(df) + 1 if not df.empty else 1
        payment_data["payment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.concat([df, pd.DataFrame([payment_data])], ignore_index=True)
        return self.save_sheet_data("payments", df)

    def mark_attendance(self, attendance_data):
        # Record attendance entry
        df = self.load_sheet_data("attendance")
        attendance_data["id"] = len(df) + 1 if not df.empty else 1
        attendance_data["date"] = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat([df, pd.DataFrame([attendance_data])], ignore_index=True)
        return self.save_sheet_data("attendance", df)

    def update_member(self, member_id, updated_data):
        # Update existing member data
        df = self.load_sheet_data("members")
        df.loc[df["member_id"] == member_id] = updated_data
        return self.save_sheet_data("members", df)

    def delete_member(self, member_id):
        # Remove member record
        df = self.load_sheet_data("members")
        df = df[df["member_id"] != member_id]
        return self.save_sheet_data("members", df)

    def get_member_by_id(self, member_id):
        # Retrieve specific member data
        df = self.load_sheet_data("members")
        member_data = df[df["member_id"] == member_id]
        return member_data.iloc[0] if not member_data.empty else None

    def get_active_members(self):
        # Get list of active members
        df = self.load_sheet_data("members")
        return df[df["status"] == "Active"]

    def get_payment_history(self, member_id=None):
        # Get payment records
        df = self.load_sheet_data("payments")
        if member_id:
            return df[df["member_id"] == member_id]
        return df

    def get_attendance_history(self, member_id=None, date=None):
        # Get attendance records with optional filters
        df = self.load_sheet_data("attendance")
        if member_id and date:
            return df[(df["member_id"] == member_id) & (df["date"] == date)]
        elif member_id:
            return df[df["member_id"] == member_id]
        elif date:
            return df[df["date"] == date]
        return df
