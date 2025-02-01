import tkinter as tk
from tkinter import filedialog
import os


def open_file_selector():
    # Create a hidden Tkinter root window
    root = tk.Tk()
    # root.withdraw()  # Hide the root window
    # root.focus_force()
    # root.lift()
    
    # Open the file dialog
    file_path: str = filedialog.askopenfilename(parent=root, title="Select a file")
    root.withdraw()  # Hide the root window

    return file_path

def clear_console():
    pass
    # used to clear console
    # os.system('cls' if os.name=='nt' else 'clear')
    
class bcolor:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
    
def input_column_names() -> list[str]:    
    user_input = sanitized_input("Please provide a comma seperated list of column names (default=all)", "all") 
    return [] if user_input == "all" else [val.strip() for val in user_input.split(',')]

def sanitized_input(prompt, default=None):
    return str.strip(input(prompt + " >>  ")) or default
