import tkinter as tk
from services.dashboard_service import Members


def open_member_frame(right_panel):
    member_window = tk.Frame(right_panel, bg="white")
    member_window.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    button_style = {
        "font": ("Arial", 14),
        "bg": "#808080",
        "fg": "white",
        "activebackground": "#696969",
        "width": 15,
        "cursor": "hand2",
        "relief": "raised"
    }

    header_frame = tk.Frame(member_window, bg="white")
    header_frame.pack(fill="x", padx=20, pady=10)

    display_member_list_button = tk.Button(
        header_frame, 
        text="Display Member List",
        command=Members.display_member_list,
        **button_style
    )
    display_member_list_button.pack(side="left", padx=5)

    add_new_member_button = tk.Button(
        header_frame, 
        text="Add New Member",
        command=Members.add_new_member,
        **button_style
    )
    add_new_member_button.pack(side="left", padx=5)

    close_button = tk.Button(
        header_frame, 
        text="Go Back",
        command=member_window.destroy,
        font=("Arial", 12),
        bg="#808080",
        fg="white"
    )
    close_button.pack(side="right", padx=5)

    search_frame = tk.Frame(member_window, bg="white", bd=2, relief="solid")
    search_frame.pack(fill="x", padx=20, pady=10)

    search_label = tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 12),
        bg="white"
    )
    search_label.pack(side="left", padx=10, pady=10)

    search_box = tk.Entry(
        search_frame,
        font=("Arial", 12),
        width=30
    )
    search_box.pack(side="left", padx=10, pady=10)

