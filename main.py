import tkinter as tk
from ui.root_ui import GymManagementApp
from utils.theme import GymTheme
import logging
import sys
from datetime import datetime

def setup_logging():
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler for important logs
    file_handler = logging.FileHandler(
        f"logs/gym_management_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)  # Only log INFO and above
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Set overall level to INFO
    root_logger.addHandler(file_handler)

def main():
    setup_logging()
    logging.info("Application started")
    
    root = tk.Tk()
    root.title("Gym Management System")
    root.geometry("1024x768")
    logging.debug("Main window initialized")

    GymTheme.setup_styles()

    try:
        icon_path = "assets/images/logo.png"
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
        logging.debug("Application icon loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load window icon: {e}", exc_info=True)

    app = GymManagementApp(root)
    logging.info("Application GUI initialized successfully")
    app.run()

if __name__ == "__main__":
    main()
