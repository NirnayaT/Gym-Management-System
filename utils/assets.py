import tkinter as tk

class IconManager:
    def __init__(self):
        self.icons = {}
        self._load_icons()
    
    def _load_icons(self):
        # Define icon paths for different features
        icon_paths = {
            'member': 'assets/images/icons/member.png',
            'trainer': 'assets/images/icons/trainer.png',
            'equipment': 'assets/images/icons/equipment.png',
            'payment': 'assets/images/icons/payment.png'
        }
        
        # Load all icons into memory
        for name, path in icon_paths.items():
            self.icons[name] = tk.PhotoImage(file=path)
    
    # Retrieve icon by name
    def get_icon(self, name):
        return self.icons.get(name)
