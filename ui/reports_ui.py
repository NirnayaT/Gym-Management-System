import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


class ReportsManager(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left control panel setup
        control_frame = ttk.LabelFrame(self, text="Report Controls", padding=15)
        control_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Report type selection
        ttk.Label(control_frame, text="Report Type:", style="Body.TLabel").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.report_type = ttk.Combobox(
            control_frame,
            values=[
                "Attendance Trends",
                "Member Plans",
                "Payment Analysis",
                "Payment History",
            ],
        )
        self.report_type.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.report_type.bind("<<ComboboxSelected>>", self.on_report_type_change)

        # Date range selection
        ttk.Label(control_frame, text="Date Range:", style="Body.TLabel").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.date_range = ttk.Combobox(
            control_frame,
            values=[
                "Last 7 Days",
                "Last 30 Days",
                "This Month",
                "This Year",
                "All Time",
            ],
        )
        self.date_range.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.date_range.bind("<<ComboboxSelected>>", self.generate_report)

        # Control buttons
        ttk.Button(
            control_frame,
            text="Generate Report",
            style="Primary.TButton",
            command=self.generate_report,
        ).grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(
            control_frame,
            text="Export Report",
            style="Secondary.TButton",
            command=self.export_report,
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Right display area setup
        report_frame = ttk.LabelFrame(self, text="Report View", padding=15)
        report_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        report_frame.grid_columnconfigure(0, weight=1)
        report_frame.grid_rowconfigure(1, weight=1)

        # Report title and content area
        self.report_title = ttk.Label(
            report_frame, text="Select a Report Type", style="Header.TLabel"
        )
        self.report_title.grid(row=0, column=0, pady=10)

        self.content_frame = ttk.Frame(report_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    # Report generation methods
    def generate_attendance_trends(self):
        df = self.db.load_sheet_data("attendance")
        df["date"] = pd.to_datetime(df["date"])

        # Date range filtering
        date_range = self.date_range.get()
        end_date = datetime.now()

        if date_range == "Last 7 Days":
            start_date = end_date - timedelta(days=7)
            df = df[df["date"] >= start_date]
        elif date_range == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
            df = df[df["date"] >= start_date]
        elif date_range == "This Month":
            start_date = end_date.replace(day=1)
            df = df[df["date"] >= start_date]
        elif date_range == "This Year":
            start_date = end_date.replace(month=1, day=1)
            df = df[df["date"] >= start_date]

        # Plot creation
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_attendance = df.groupby("date")["member_id"].count()

        line = ax.plot(daily_attendance.index, daily_attendance.values, marker="o")[0]

        for x, y in zip(daily_attendance.index, daily_attendance.values):
            ax.text(x, y, f"{int(y)}", ha="center", va="bottom")

        ax.set_title(f"Daily Attendance Trends - {date_range}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Members")

        max_attendance = (
            daily_attendance.values.max() if not daily_attendance.empty else 10
        )
        y_limit = max(10, int(max_attendance * 1.2))
        ax.set_ylim(0, y_limit)
        ax.set_yticks(range(0, y_limit + 1, max(1, y_limit // 10)))

        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_member_plans(self):
        df = self.db.load_sheet_data("members")

        fig, ax = plt.subplots(figsize=(10, 6))
        plan_counts = df["membership_type"].value_counts()

        bars = ax.bar(plan_counts.index, plan_counts.values)
        ax.set_title("Membership Plans Distribution")
        ax.set_xlabel("Plan Type")
        ax.set_ylabel("Number of Members")

        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 10))

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_payment_chart(self):
        df = self.db.load_sheet_data("payments")

        fig, ax = plt.subplots(figsize=(10, 6))
        payment_types = df["payment_type"].value_counts()

        ax.pie(payment_types.values, labels=payment_types.index, autopct="%1.1f%%")
        ax.set_title("Payment Methods Distribution")

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_payment_history(self):
        df = self.db.load_sheet_data("payments")

        tree = ttk.Treeview(
            self.content_frame,
            columns=("Date", "Member", "Amount", "Type"),
            show="headings",
        )

        tree.heading("Date", text="Payment Date")
        tree.heading("Member", text="Member Name")
        tree.heading("Amount", text="Amount")
        tree.heading("Type", text="Payment Type")

        tree.column("Date", width=150)
        tree.column("Member", width=200)
        tree.column("Amount", width=100)
        tree.column("Type", width=100)

        scrollbar = ttk.Scrollbar(
            self.content_frame, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        for _, row in df.iterrows():
            tree.insert(
                "",
                "end",
                values=(
                    row["payment_date"],
                    row["member_name"],
                    f"Rs. {row['amount']:.2f}",
                    row["payment_type"],
                ),
            )

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Event handlers and utility methods
    def on_report_type_change(self, event=None):
        report_type = self.report_type.get()
        self.report_title.config(text=report_type)
        self.generate_report()

    def generate_report(self, event=None):
        report_type = self.report_type.get()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if report_type == "Attendance Trends":
            self.generate_attendance_trends()
        elif report_type == "Member Plans":
            self.generate_member_plans()
        elif report_type == "Payment Analysis":
            self.generate_payment_chart()
        elif report_type == "Payment History":
            self.generate_payment_history()

    def export_report(self):
        report_type = self.report_type.get()
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf")],
            )
            if filename:
                if filename.endswith(".xlsx"):
                    self.export_to_excel(filename)
                elif filename.endswith(".pdf"):
                    self.export_to_pdf(filename)
                messagebox.showinfo("Success", "Report exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")

    def export_to_excel(self, filename):
        report_type = self.report_type.get()
        df = self.db.load_sheet_data(report_type.lower().replace(" ", "_"))
        df.to_excel(filename, index=False)

    def export_to_pdf(self, filename):
        fig = plt.gcf()
        fig.savefig(filename, format="pdf", bbox_inches="tight")
