from tkinter import ttk

# Core app settings
APP_NAME = "Gym Management System"
APP_VERSION = "1.0.0"

# Database paths
MEMBERS_DB = "database/members.xlsx"
PAYMENTS_DB = "database/payments.xlsx"
ATTENDANCE_DB = "database/attendance.xlsx"

# Theme color palette
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#34495e"
ACCENT_COLOR = "#3498db"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f1c40f"
ERROR_COLOR = "#e74c3c"


# Theme configuration
def set_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Base widget styles
    style.configure("TLabel", padding=5)
    style.configure("TButton", padding=5)
    style.configure("TEntry", padding=5)
