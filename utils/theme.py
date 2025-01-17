import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

class GymTheme:
    COLORS = {
        'primary': '#000000',      # Pure Black
        'text': '#000000',         # Black Text
        'accent': '#ffffff',       # White
        'button': '#000000',       # Black Buttons
        'button_text': '#ffffff'   # White Button Text
    }

    FONTS = {
        'title': ('Helvetica', 24, 'bold'),
        'header': ('Helvetica', 16, 'bold'),
        'body': ('Helvetica', 12),
        'button': ('Helvetica', 12, 'bold')
    }

    @staticmethod
    def setup_styles():
        style = ttk.Style()
        style.theme_use('clam')

        # Button styles
        style.configure('Primary.TButton',
                       font=GymTheme.FONTS['button'],
                       background=GymTheme.COLORS['button'],
                       foreground=GymTheme.COLORS['button_text'],
                       padding=(15, 8))
        
        style.map('Primary.TButton',
                 background=[('active', '#333333')])

        style.configure('Secondary.TButton',
                       font=GymTheme.FONTS['button'],
                       background=GymTheme.COLORS['button'],
                       foreground=GymTheme.COLORS['button_text'],
                       padding=(15, 8))

        # Label styles
        style.configure('Title.TLabel',
                       font=GymTheme.FONTS['title'],
                       foreground=GymTheme.COLORS['text'])

        style.configure('Header.TLabel',
                       font=GymTheme.FONTS['header'],
                       foreground=GymTheme.COLORS['text'])

        style.configure('Body.TLabel',
                       font=GymTheme.FONTS['body'],
                       foreground=GymTheme.COLORS['text'])

        # Entry styles
        style.configure('TEntry',
                       font=GymTheme.FONTS['body'],
                       padding=5)

        # Combobox styles
        style.configure('TCombobox',
                       font=GymTheme.FONTS['body'],
                       padding=5)

        # Treeview styles
        style.configure('Treeview',
                       font=GymTheme.FONTS['body'],
                       rowheight=25)

        style.configure('Treeview.Heading',
                       font=GymTheme.FONTS['header'],
                       background=GymTheme.COLORS['primary'],
                       foreground=GymTheme.COLORS['accent'])

        # Frame styles
        style.configure('TFrame')

        # LabelFrame styles
        style.configure('TLabelframe',
                       font=GymTheme.FONTS['header'])

        style.configure('TLabelframe.Label',
                       font=GymTheme.FONTS['header'],
                       foreground=GymTheme.COLORS['text'])

        # Notebook styles
        style.configure('TNotebook',
                       font=GymTheme.FONTS['body'])

        style.configure('TNotebook.Tab',
                       font=GymTheme.FONTS['body'],
                       padding=(10, 5))
        
        # Style for the overlay frame
        style.configure('Transparent.TFrame', background='gray85', opacity=0.3)
        style.configure('QRContent.TFrame', background='white')
        style.configure('QRTitle.TLabel', background='white', font=('Helvetica', 14, 'bold'))
        # Add these lines to your existing styles
        style.configure('Utility.TLabelFrame', background='white')
        style.configure('Utility.TLabelFrame.Label', font=('Helvetica', 10))




    @staticmethod
    def apply_theme_to_matplotlib():
        import matplotlib.pyplot as plt
        
        plt.style.use('seaborn-white')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Helvetica']
        plt.rcParams['axes.labelcolor'] = GymTheme.COLORS['text']
        plt.rcParams['axes.titlecolor'] = GymTheme.COLORS['text']
        plt.rcParams['xtick.color'] = GymTheme.COLORS['text']
        plt.rcParams['ytick.color'] = GymTheme.COLORS['text']
