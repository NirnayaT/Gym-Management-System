import tkinter as tk
from PIL import Image, ImageTk
from decouple import config
from services.service import MainDashboard
from services.service import Members
    
logo_path = config("LOGO_PATH")
new_width = int(config("NEW_WIDTH"))
new_height = int(config("NEW_HEIGHT"))

root = tk.Tk()
root.title("Gym Management System")
root.geometry("800x600")

def open_member_window():
    member_window = tk.Toplevel(root)
    member_window.title("Members")
    member_window.geometry("800x600")
    
    member_frame = tk.Frame(member_window)
    member_frame.grid(row=0, column=0)
    
    display_member_list_button = tk.Button(member_frame, text="Display Member List", font=("Arial", 16), command=Members.display_member_list)
    display_member_list_button.grid(row=0, column=0, padx=20, pady=10, sticky="e")

    add_new_member_button = tk.Button(member_frame, text="Add New Member", font=("Arial", 16), command=Members.add_new_member)
    add_new_member_button.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    
    close_button = tk.Button(member_frame, text="Go Back", font=("Arial", 10), command=member_window.destroy)
    close_button.grid(row=0, column=2, padx=20, pady=10, sticky="w")
    
    inside_frame = tk.Frame(member_frame, width=200, height=100, bg="white", bd=1, relief="solid", )
    inside_frame.grid(row=1, column=0)

    search_label = tk.Label(inside_frame,text="Search:", font=("Arial", 12))
    search_label.grid(row=0, column=0)
    
    search_box = tk.Entry(inside_frame,textvariable="Search Box...")
    search_box.grid(row=0, column=1, padx=10, pady=10)
    
    

logo_frame = tk.Frame(root)
logo_frame.grid(row=0, column=0)


logo = Image.open(logo_path)
logo_resized = logo.resize((new_width, new_height))
logo_tk = ImageTk.PhotoImage(logo_resized)

logo_label = tk.Label(logo_frame, image=logo_tk)
logo_label.grid(row=0, column=0, padx=10, pady=10)

dashboard_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
dashboard_frame.grid(row=1, column=0, padx=20, pady=10)


dashboard_button = tk.Button(dashboard_frame, text="Dashboard", font=("Arial", 16), command=MainDashboard.dashboard_button)
dashboard_button.grid(row=1, column=0, padx=20, pady=10, sticky="news")

members_button = tk.Button(dashboard_frame, text="Members", font=("Arial", 16), command=open_member_window)
members_button.grid(row=2, column=0, padx=20, pady=10,  sticky="news")


# refrence
logo_label.image = logo_tk


root.mainloop()
