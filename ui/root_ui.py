import tkinter as tk
from tkinter import ttk
from database.excel_handler import ExcelDatabase
from utils.theme import GymTheme
from .members_ui import MembersManager
from .payments_ui import PaymentsManager
from .attendance_ui import AttendanceManager
from .reports_ui import ReportsManager

class GymManagementApp:
    def __init__(self, root):
        self.root = root
        
        
        # Initialize database
        self.db = ExcelDatabase()
        
        # Create main container with theme
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create navigation menu
        self.create_navigation()
        
        # Create main content area
        self.content_frame = ttk.Frame(self.main_container, style='Content.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show default page (Members)
        self.show_members_page()

    def create_header(self):
        header_frame = ttk.Frame(self.main_container, style='Clean.TFrame')
        header_frame.pack(fill=tk.X)
        
        # Create a container for logo and title
        header_container = ttk.Frame(header_frame, style='Clean.TFrame')
        header_container.pack(pady=10)
        
        # Create a blue background container
        title_container = ttk.Frame(header_frame, style='Title.TFrame')
        title_container.pack(pady=10, padx=20, fill=tk.X)
        
        # Add logo
        logo_img = tk.PhotoImage(file='assets/images/logo.png')
        logo_img = logo_img.subsample(8, 8)  
        self.logo_img = logo_img  
        
        logo_label = ttk.Label(
            header_container,
            image=logo_img,
            style='Clean.TLabel'
        )
        logo_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Title with black text
        title_label = ttk.Label(
            header_container, 
            text="Gym Management System",
            style='Header.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=(5, 10))


    def create_navigation(self):
        nav_frame = ttk.Frame(self.main_container, style='Navigation.TFrame')
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Navigation buttons
        nav_buttons_left = [
            ("Members", self.show_members_page),
            ("Payments", self.show_payments_page),
            ("Attendance", self.show_attendance_page),
            ("Reports", self.show_reports_page)
        ]
        
        for text, command in nav_buttons_left:
            btn = ttk.Button(
                nav_frame,
                text=text,
                style='Navigation.TButton',
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        utility_frame = ttk.LabelFrame(nav_frame, text="QR Scan Me", padding=15, style = 'Clean.TFrame')
        utility_frame.pack(side=tk.RIGHT, padx=10)
        
        nav_buttons_right = [
            ("Esewa", self.show_qr_code),
            ("Bank", self.show_bank_info),
            ("Wifi", self.show_wifi_info),
        ]
        
        for text, command in nav_buttons_right:
            btn = ttk.Button(
                utility_frame,
                text=text,
                style='Navigation.TButton',
                command=command
            )
            btn.pack(side=tk.RIGHT, padx=5)
            
    def show_members_page(self):
        self.clear_content()
        members_page = MembersManager(self.content_frame, self.db)
        members_page.pack(fill=tk.BOTH, expand=True)

    def show_payments_page(self):
        self.clear_content()
        payments_page = PaymentsManager(self.content_frame, self.db)
        payments_page.pack(fill=tk.BOTH, expand=True)

    def show_attendance_page(self):
        self.clear_content()
        attendance_page = AttendanceManager(self.content_frame, self.db)
        attendance_page.pack(fill=tk.BOTH, expand=True)

    def show_reports_page(self):
        self.clear_content()
        reports_page = ReportsManager(self.content_frame, self.db)
        reports_page.pack(fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_qr_code(self):
        # Create overlay frame with transparent background
        self.overlay_frame = ttk.Frame(self.main_container, style='Overlay.TFrame')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Set frame transparency
        self.overlay_frame.configure(style='Transparent.TFrame')
        
        # Create content frame for QR code with white background
        content_frame = ttk.Frame(self.overlay_frame, style='QRContent.TFrame')
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add title above QR code
        title_label = ttk.Label(
            content_frame,
            text="Scan QR Code for Payment (Esewa)",
            style='QRTitle.TLabel',
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=(20, 10))
        
        # Load and display QR image
        qr_img = tk.PhotoImage(file='assets/images/esewa_qr_code.png')
        qr_img = qr_img.subsample(2, 2)  # Adjust size as needed
        self.qr_img = qr_img  # Keep reference
        
        qr_label = ttk.Label(
            content_frame,
            image=qr_img,
            style='Clean.TLabel'
        )
        qr_label.pack(pady=20)
        
        # Bind click outside to close
        self.overlay_frame.bind('<Button-1>', lambda e: self.hide_qr_code())


    def hide_qr_code(self):
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()


    def show_bank_info(self):
        # Create overlay frame with transparent background
        self.overlay_frame = ttk.Frame(self.main_container, style='Overlay.TFrame')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Set frame transparency
        self.overlay_frame.configure(style='Transparent.TFrame')
        
        # Create content frame for QR code with white background
        content_frame = ttk.Frame(self.overlay_frame, style='QRContent.TFrame')
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add title above QR code
        title_label = ttk.Label(
            content_frame,
            text="Scan QR Code for Payment (Bank)",
            style='QRTitle.TLabel',
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=(20, 10))
        
        # Load and display QR image
        qr_img = tk.PhotoImage(file='assets/images/bank_qr_code.png')
        qr_img = qr_img.subsample(2, 2)  # Adjust size as needed
        self.qr_img = qr_img  # Keep reference
        
        qr_label = ttk.Label(
            content_frame,
            image=qr_img,
            style='Clean.TLabel'
        )
        qr_label.pack(pady=20)
        
        # Bind click outside to close
        self.overlay_frame.bind('<Button-1>', lambda e: self.hide_qr_code())


    def show_wifi_info(self):
        # Create overlay frame with transparent background
        self.overlay_frame = ttk.Frame(self.main_container, style='Overlay.TFrame')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Set frame transparency
        self.overlay_frame.configure(style='Transparent.TFrame')
        
        # Create content frame for QR code with white background
        content_frame = ttk.Frame(self.overlay_frame, style='QRContent.TFrame')
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add title above QR code
        title_label = ttk.Label(
            content_frame,
            text="Scan for Wifi",
            style='QRTitle.TLabel',
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=(20, 10))
        
        # Load and display QR image
        qr_img = tk.PhotoImage(file='assets/images/wifi_qr_code.png')
        qr_img = qr_img.subsample(2, 2)  # Adjust size as needed
        self.qr_img = qr_img  # Keep reference
        
        qr_label = ttk.Label(
            content_frame,
            image=qr_img,
            style='Clean.TLabel'
        )
        qr_label.pack(pady=20)
        
        # Bind click outside to close
        self.overlay_frame.bind('<Button-1>', lambda e: self.hide_qr_code())


    def run(self):
        self.root.mainloop()
