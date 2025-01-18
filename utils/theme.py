import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

class GymTheme:
    # Color definitions
    COLORS = {
        'primary': '#7f7f7c',      # Grey
        'secondary': '#FFFFFF',    # Pure White
        'text': 'black',         # Grey Text
        'button': '#7f7f7c',       # Grey Buttons
        'button_text': '#ffffff'   # White Button Text
    }
    # Font definitions
    FONTS = {
        'title': ('Helvetica', 24, 'bold'),
        'header': ('Helvetica', 18, 'bold'),
        'body': ('Helvetica', 12),
        'button': ('Helvetica', 14, 'bold'),
        'submit_button': ('Helvetica', 8, 'bold')
    }
    
    @staticmethod
    def setup_styles():
        style = ttk.Style()
        style.theme_use('clam')

        # Override all background colors to pure white
        style.configure('.', background='white')
        
        # Frame styles
        style.configure('Main.TFrame', background='white')
        style.configure('Navigation.TFrame', background='white')
        style.configure('Content.TFrame', background='white')
        
        # LabelFrame styles with black outline
        style.configure('TLabelframe', 
                       background='white',
                       bordercolor='black',
                       darkcolor='black',
                       lightcolor='black')
        
        style.configure('TLabelframe.Label', 
                       background='white',
                       foreground='black',
                       font=GymTheme.FONTS['header'])
        
        # Button styles with new color
        button_style = {
            'font': GymTheme.FONTS['button'],
            'background': '#777a79',
            'foreground': 'white',
            'padding': (15, 8),
            'bordercolor': 'black',
        }
        button_style_submit = {
            'font': GymTheme.FONTS['submit_button'],
            'background': '#777a79',
            'foreground': 'white',
            'padding': (10, 4),
            'bordercolor': 'black',
        }
        
        style.configure('Primary.TButton', **button_style)
        style.configure('Secondary.TButton', **button_style)
        style.configure('Navigation.TButton', **button_style)
        style.configure('Submit.TButton', **button_style_submit)
        
        # Add hover effects (inverted colors)
        style.map('Primary.TButton',
                 background=[('active', 'white')],
                 foreground=[('active', '#777a79')])
        
        style.map('Secondary.TButton',
                 background=[('active', 'white')],
                 foreground=[('active', '#777a79')])
        
        style.map('Navigation.TButton',
                 background=[('active', 'white')],
                 foreground=[('active', '#777a79')])
        
        style.map('Submit.TButton',
                 background=[('active', 'white')],
                 foreground=[('active', '#777a79')])
        
        # Label styles
        style.configure('Header.TLabel', 
                       font=GymTheme.FONTS['header'],
                       background='white', 
                       foreground='black')
        
        style.configure('Body.TLabel',
                       font=GymTheme.FONTS['body'],
                       background='white',
                       foreground='black')
        
        
        # Entry and Combobox styles with black outline
        style.configure('TEntry', 
                       fieldbackground='white',
                       foreground='black',
                       borderwidth=1,
                       
                    #    darkcolor='black',
                       lightcolor='black')
        
        style.configure('TCombobox', 
                       background='white',
                       fieldbackground='white',
                    #    foreground='black',
                    #    bordercolor='black',
                    #    darkcolor='black',
                       lightcolor='black')
        
        # Treeview styles with black outline
        style.configure('Treeview', 
                       background='white',
                       fieldbackground='white',
                       foreground='black',
                    #    bordercolor='black',
                       font=GymTheme.FONTS['body'])
        
        style.configure('Treeview.Heading', 
                       background='#777a79',
                       foreground='white',
                       font=GymTheme.FONTS['button'])
        
        style.map('Treeview',
                 background=[('selected', 'black')],
                 foreground=[('selected', 'white')])
        
        style.map('Treeview.Heading',
                 background=[('active', 'white')],
                 foreground=[('active', '#777a79')])        
        
        # Notebook styles
        style.configure('TNotebook', background='white')
        style.configure('TNotebook.Tab', 
                       background='white',
                       foreground='black')
        
        # Canvas styles for matplotlib
        style.configure('Canvas.TFrame', background='white')
        

        # Scrollbar styles with fixed grey color
        style.configure('Vertical.TScrollbar',
                       background='#808080',  # Medium grey
                       arrowcolor='black',
                       troughcolor='white',
                       bordercolor='black')
        
        style.configure('Horizontal.TScrollbar',
                       background='#808080',  # Medium grey
                       arrowcolor='black',
                       troughcolor='white',
                       bordercolor='black')
        
        style.map('Vertical.TScrollbar',
                 background=[('pressed', '#808080'),
                            ('active', '#808080')])
        
        style.map('Horizontal.TScrollbar',
                 background=[('pressed', '#808080'),
                            ('active', '#808080')])
        
        style.configure('Separator.TSeparator',
                    background='black',
                    thickness=2)


        # Configure matplotlib style
        plt.style.use('default')
        plt.rcParams.update({
            'axes.facecolor': 'white',
            'figure.facecolor': 'white',
            'text.color': 'black',
            'axes.labelcolor': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'axes.grid': True,
            'grid.color': '#000000',
            'grid.alpha': 0.1,
            'axes.spines.top': True,
            'axes.spines.right': True,
            'axes.spines.bottom': True,
            'axes.spines.left': True
        })
