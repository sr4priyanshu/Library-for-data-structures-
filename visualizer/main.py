"""
Main entry point for the Data Structures Visualizer GUI
This application provides a graphical interface to interact with and visualize
data structures implemented in C (Linked List, BST, Graph).

Author: AI Assistant
Date: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path to import UI modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bst_ui import BSTVisualizer
from linkedlist_ui import LinkedListVisualizer
from graph_ui import GraphVisualizer


class MainWindow:
    """
    Main application window that provides navigation between different
    data structure visualizers.
    
    This class creates a tabbed interface where each tab represents
    a different data structure (BST, Linked List, Graph).
    """
    
    def __init__(self, root):
        """
        Initialize the main window with a notebook (tabbed interface).
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Data Structures Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for each data structure
        self.create_tabs()
        
        # Add menu bar
        self.create_menu()
        
    def create_tabs(self):
        """
        Create individual tabs for each data structure visualizer.
        Each tab contains a frame that will hold the specific visualizer.
        """
        # BST Tab
        bst_frame = ttk.Frame(self.notebook)
        self.notebook.add(bst_frame, text="Binary Search Tree")
        self.bst_visualizer = BSTVisualizer(bst_frame)
        
        # Linked List Tab
        ll_frame = ttk.Frame(self.notebook)
        self.notebook.add(ll_frame, text="Linked List")
        self.ll_visualizer = LinkedListVisualizer(ll_frame)
        
        # Graph Tab
        graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Graph")
        self.graph_visualizer = GraphVisualizer(graph_frame)
        
    def create_menu(self):
        """
        Create a menu bar with Help and About options.
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        
    def show_about(self):
        """
        Display about dialog with application information.
        """
        about_text = """
Data Structures Visualizer

A graphical interface for visualizing and interacting with
data structures implemented in C.

Features:
- Binary Search Tree operations and visualization
- Linked List operations and visualization
- Graph operations and visualization

Built with Python Tkinter and ctypes.
        """
        messagebox.showinfo("About", about_text)
        
    def show_instructions(self):
        """
        Display usage instructions for the application.
        """
        instructions = """
How to Use:

1. Select a tab for the data structure you want to work with
2. Use the input field and buttons to perform operations:
   - Insert: Add a new node/element
   - Delete: Remove a node/element
   - Search: Find a node/element
   - Clear: Reset the data structure
3. The visualization updates automatically after each operation

Note: Make sure dshelp.dll is in the project root directory.
        """
        messagebox.showinfo("Instructions", instructions)


def main():
    """
    Main function to launch the application.
    """
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

