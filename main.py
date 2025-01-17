import tkinter as tk
from ui.root_ui import GymManagementApp
from utils.theme import GymTheme
import logging


def setup_logging():
    logging.basicConfig(
        filename="gym_management.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    root = tk.Tk()
    root.title("Gym Management System")
    root.geometry("1024x768")

    GymTheme.setup_styles()

    try:
        icon_path = "assets/images/logo.png"
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
    except Exception as e:
        logging.error(f"Failed to load window icon: {e}")

    app = GymManagementApp(root)
    app.run()


if __name__ == "__main__":
    main()
