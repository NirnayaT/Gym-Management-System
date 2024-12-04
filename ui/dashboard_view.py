import tkinter as tk

def open_dashboard_frame(right_panel):
    for widget in right_panel.winfo_children():
        widget.destroy()
    tk.Label(right_panel,text="ABC").pack()