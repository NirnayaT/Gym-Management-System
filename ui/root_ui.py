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
        self.db = ExcelDatabase()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Create left navigation panel
        self.create_left_panel()
        
        # Create right content area
        self.create_content_frame()

        
        # Show default page
        self.show_home_page()

    def create_left_panel(self):
        left_panel = ttk.Frame(self.main_container, style='Navigation.TFrame')
        left_panel.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        # Add logo at top
        logo_img = tk.PhotoImage(file='assets/images/logo.png')
        logo_img = logo_img.subsample(4, 4)  
        self.logo_img = logo_img
        
        logo_label = ttk.Label(
            left_panel,
            image=logo_img,
            style='Clean.TLabel'
        )
        logo_label.pack(pady=20)
        
        # Navigation buttons
        nav_buttons = [
            ["Home", self.show_home_page],
            ["Members", self.show_members_page],
            ["Payments", self.show_payments_page],
            ["Attendance", self.show_attendance_page],
            ["Reports", self.show_reports_page]
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(
                left_panel,
                text=text,
                style='Navigation.TButton',
                command=command,
                width=15
            )
            btn.pack(pady=10)
        
        spacer = ttk.Frame(left_panel)
        spacer.pack(expand=True)
        
        # Exit button at bottom
        exit_btn = ttk.Button(
            left_panel,
            text="Exit",
            style='Navigation.TButton',
            command=self.root.quit,
            width=15
        )
        exit_btn.pack(pady=10)
            
        utility_frame = ttk.LabelFrame(left_panel, padding=15,text='QR Scan', style = 'Clean.TLabelframe')
        utility_frame.pack(side=tk.BOTTOM, padx=10)
        
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
                command=command,
            )
            btn.pack(side=tk.BOTTOM, padx=5, pady=15)
    
    def create_content_frame(self):
        self.content_frame = ttk.LabelFrame(
            self.main_container, 
            text="Gym Management System",
            padding=15
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1) 
              
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
        logo_img = logo_img.subsample(-10, -10)  
        self.logo_img = logo_img  
        
        logo_label = ttk.Label(
            header_container,
            image=logo_img,
            style='Clean.TLabel'
        )
        logo_label.pack(side=tk.LEFT, padx=(20, 10))
        
        # Title with black text
        title_label = ttk.Label(
            header_container, 
            text="Gym Management System",
            style='Header.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=(5, 10))

    def show_home_page(self):
        self.clear_content()
        dashboard_frame = ttk.Frame(self.content_frame)
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Center container
        center_frame = ttk.Frame(dashboard_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Welcome Message in bold
        welcome_label = ttk.Label(
            center_frame,
            text="Welcome to the Gym Management System",
            font=('Helvetica', 24, 'bold'),
            foreground='black'
        )
        welcome_label.pack()

        # Visible separator line
        separator = ttk.Separator(center_frame, orient='horizontal', style='Separator.TSeparator')
        separator.pack(fill='x', padx=100, pady=20)

        # Subtitle in italic
        subtitle_label = ttk.Label(
            center_frame,
            text="Your Complete Fitness Management Solution",
            font=('Helvetica', 16, 'italic'),
            foreground='black'
        )
        subtitle_label.pack()

        # Instructions
        instruction_label = ttk.Label(
            center_frame,
            text="Select an option from the menu to get started",
            font=('Helvetica', 12),
            foreground='black'
        )
        instruction_label.pack(pady=20)


         
    def show_members_page(self):
        self.clear_content()
        members_manager = MembersManager(self.content_frame, self.db)
        members_manager.pack(fill=tk.BOTH, expand=True) 

    def show_payments_page(self):
        self.clear_content()
        payment_manager = PaymentsManager(self.content_frame, self.db)
        payment_manager.pack(fill=tk.BOTH, expand=True)

    def show_attendance_page(self):
        self.clear_content()
        attendance_manager = AttendanceManager(self.content_frame, self.db)
        attendance_manager.pack(fill=tk.BOTH, expand=True)

    def show_reports_page(self):
        self.clear_content()
        report_manager = ReportsManager(self.content_frame, self.db)
        report_manager.pack(fill=tk.BOTH, expand=True)
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
        qr_img = qr_img.subsample(4,4)  # Adjust size as needed
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
