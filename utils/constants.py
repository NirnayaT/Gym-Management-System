# Core app settings
APP_NAME = "Gym Management System"
APP_VERSION = "1.0.0"

# Database paths
DATABASE_DIR = "database"
DATABASE_FILE = "database/gym_database.xlsx"
BACKUP_DIR = "database/backup"
LOG_DIR = "logs"

# Sheet names
SHEET_NAMES = {
    "members": "Members",
    "payments": "Payments",
    "attendance": "Attendance"
}

# Theme colors
COLORS = {
    "primary": "#000000",    # Black
    "secondary": "#FFFFFF",  # White
    "text": "#000000",      # Black
    "button": "#000000",    # Black
    "button_text": "#FFFFFF" # White
}

# UI Settings
WINDOW_SIZE = "1024x768"
PADDING = 10
BUTTON_WIDTH = 20

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"

# File extensions
EXCEL_EXTENSION = ".xlsx"
LOG_EXTENSION = ".log"
