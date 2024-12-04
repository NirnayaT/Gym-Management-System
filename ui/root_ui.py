import tkinter as tk
from PIL import Image, ImageTk
from decouple import config
from services.dashboard_service import MainDashboard
from ui import dashboard_view, member_view

class GymManagementApp:
    def create_root(self):
        root = tk.Tk()
        root.title("Gym Management System")
        root.geometry("1200x800")
        root.configure(bg="#f0f0f0")
        return root

    def create_main_container(self, root):
        main_container = tk.Frame(root, bg="#f0f0f0")
        main_container.pack(expand=True, fill="both")
        return main_container

    def create_panels(self, main_container):
        left_panel = tk.Frame(main_container, bg="#f0f0f0", width=400)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        right_panel = tk.Frame(main_container, bg="white", width=800)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        right_panel.configure(height=400, width=500, relief="solid", bd=2)
        
        return left_panel, right_panel

    def create_logo(self, left_panel):
        logo_frame = tk.Frame(left_panel, bg="#f0f0f0")
        logo_frame.pack(pady=20)

        logo_path = config("LOGO_PATH")
        new_width = int(config("NEW_WIDTH"))
        new_height = int(config("NEW_HEIGHT"))

        logo = Image.open(logo_path)
        logo_resized = logo.resize((new_width, new_height))
        logo_tk = ImageTk.PhotoImage(logo_resized)
        logo_label = tk.Label(logo_frame, image=logo_tk, bg="#f0f0f0")
        logo_label.pack()
        
        return logo_tk  # Return to prevent garbage collection

    def create_buttons(self,root, left_panel, right_panel):
        dashboard_frame = tk.Frame(left_panel)
        dashboard_frame.pack(pady=20, fill="x")

        button_style = {
            "font": ("Arial", 16),
            "width": 15,
            "bg": "#808080",
            "fg": "white",
            "activebackground": "#696969",
            "relief": "raised",
            "cursor": "hand2"
        }

        
        dashboard_button = tk.Button(
            dashboard_frame, 
            text="Dashboard",
            command=lambda:dashboard_view.open_dashboard_frame(right_panel),
            **button_style
        )
        dashboard_button.pack(pady=10)
        
        members_button = tk.Button(
            dashboard_frame,
            text="Members",
            command=lambda:member_view.open_member_frame(right_panel),
            **button_style
        )
        members_button.pack(pady=10)
        
        exit_button = tk.Button(
            dashboard_frame,
            text="Exit",
            command=root.destroy,
            **button_style
        )
        exit_button.pack(pady=10)
    # def dashboard_view_click(self):
    #     self.reset_panel(right_panel)
    #     MainDashboard.dashboard_button(right_panel)
        
    def reset_panel(self,right_panel):
        # print(right_panel)
        for widget in right_panel.winfo_children():
            widget.destroy()

            
    def run(self):
        root = self.create_root()
        main_container = self.create_main_container(root)
        left_panel, right_panel = self.create_panels(main_container)
        self.logo_tk = self.create_logo(left_panel)  # Store as instance attribute
        self.create_buttons(root, left_panel,right_panel)
        # self.reset_panel(right_panel)
        root.mainloop()


