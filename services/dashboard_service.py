import tkinter as tk
class MainDashboard:
    def dashboard_button(right_panel):
        
        for widget in right_panel.winfo_children():
            widget.destroy()
            
        # dashboard_frame = tk.Frame(right_panel)
        # dashboard_frame.pack(expand=True)
        # # dashboard_frame.destroy()
        # print(right_panel)
        # print("smtghere")
        # right_panel.destroy()
        # print(dashboard_frame.winfo_children())
        # for widget in right_panel.winfo_children():
        #     widget.destroy()

    def members_button():
        pass

class Members:
    def display_member_list():
        pass
    
    def add_new_member():
        pass

class Payments:
    def display_payment_list():
        pass