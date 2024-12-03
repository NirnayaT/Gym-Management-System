from abc import ABC, abstractmethod
import tkinter as tk
from typing import Any

class BaseView(ABC):
    """Base interface for all UI views"""
    
    @abstractmethod
    def setup_ui(self) -> None:
        """Initialize and setup UI components"""
        pass
    
    @abstractmethod
    def update_view(self) -> None:
        """Update the view with current data"""
        pass
    
    @abstractmethod
    def clear_view(self) -> None:
        """Clear all input fields and reset view"""
        pass

class BaseFrame(ABC):
    """Base interface for frame components"""
    
    @abstractmethod
    def create_frame(self, parent: tk.Widget) -> tk.Frame:
        """Create and return a new frame"""
        pass
    
    @abstractmethod
    def configure_frame(self) -> None:
        """Configure frame settings"""
        pass

class BaseDialog(ABC):
    """Base interface for dialog windows"""
    
    @abstractmethod
    def show_dialog(self) -> Any:
        """Display dialog and return result"""
        pass
    
    @abstractmethod
    def validate_input(self) -> bool:
        """Validate dialog input"""
        pass

# Example implementation
# class GymBaseView(BaseView):
#     def __init__(self, master: tk.Widget):
#         self.master = master
#         self.frame = tk.Frame(self.master)
        
#     def setup_ui(self) -> None:
#         self.frame.grid(padx=10, pady=10)
        
#     def update_view(self) -> None:
#         self.frame.update()
        
#     def clear_view(self) -> None:
#         for widget in self.frame.winfo_children():
#             widget.destroy()
