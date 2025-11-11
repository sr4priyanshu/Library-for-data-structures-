"""
Linked List Visualizer Module

This module provides a GUI interface for interacting with and visualizing
a Linked List. It uses ctypes to call C functions from dshelp.dll where possible,
and Python-side implementations for operations that require input handling.

Note: Since llist_insert uses scanf, we maintain a Python-side linked list
for visualization while still using C functions for other operations when possible.

To extend this for other list structures:
1. Modify the node structure
2. Update the drawing algorithm in draw_list()
3. Add/modify operation buttons as needed
"""

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os

# Try to load the DLL
dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dshelp.dll")
if not os.path.exists(dll_path):
    dll_path = "dshelp.dll"

try:
    dll = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"Warning: Could not load DLL: {e}")
    dll = None


class ListNode:
    """
    Python representation of the C linked list structure.
    This mirrors the C struct Linked_List.
    """
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListVisualizer:
    """
    Main class for Linked List visualization and interaction.
    
    This class handles:
    - Managing the linked list state
    - Drawing the list on canvas
    - Handling user operations (insert, delete, search)
    """
    
    def __init__(self, parent):
        """
        Initialize the Linked List visualizer with UI components.
        
        Args:
            parent: Parent Tkinter widget (usually a Frame)
        """
        self.head = None  # Python-side linked list head
        
        # Setup ctypes if DLL is available
        if dll:
            self.setup_ctypes()
        
        # Create UI
        self.create_ui(parent)
        
    def setup_ctypes(self):
        """
        Configure ctypes to interface with C linked list functions.
        Note: llist_insert uses scanf, so we'll use Python-side implementation.
        """
        # Define the list structure in ctypes
        class List(ctypes.Structure):
            pass
        
        List._fields_ = [
            ("data", ctypes.c_int),
            ("next", ctypes.POINTER(List))
        ]
        
        self.List = List
        
        # Setup other functions for future use
        # Note: llist_insert uses scanf, so we implement it in Python
        dll.llist_count.argtypes = [ctypes.POINTER(List)]
        dll.llist_count.restype = ctypes.c_int
        
    def create_ui(self, parent):
        """
        Create the user interface with controls and canvas.
        
        Args:
            parent: Parent widget
        """
        # Control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input section
        input_frame = ttk.LabelFrame(control_frame, text="Operations", padding=10)
        input_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="Value:").grid(row=0, column=0, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=10)
        self.value_entry.grid(row=0, column=1, padx=5)
        self.value_entry.bind("<Return>", lambda e: self.insert_at_head())
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Insert at Head", command=self.insert_at_head).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete from Head", command=self.delete_from_head).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete from Tail", command=self.delete_from_tail).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Search", command=self.search_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Count Nodes", command=self.count_nodes).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Reverse Display", command=self.reverse_display).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_list).pack(side=tk.LEFT, padx=2)
        
        # Info label
        self.info_label = ttk.Label(control_frame, text="Ready", foreground="blue")
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # Count label
        self.count_label = ttk.Label(control_frame, text="Count: 0", foreground="purple")
        self.count_label.pack(side=tk.LEFT, padx=10)
        
        # Canvas for list visualization
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=1000, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def insert_at_head(self):
        """
        Insert a node at the head of the linked list.
        """
        try:
            value = int(self.value_entry.get())
            self.value_entry.delete(0, tk.END)
            
            # Create new node
            new_node = ListNode(value)
            new_node.next = self.head
            self.head = new_node
            
            self.info_label.config(text=f"Inserted at head: {value}", foreground="green")
            self.update_count()
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        except Exception as e:
            messagebox.showerror("Error", f"Insert failed: {str(e)}")
            
    def delete_from_head(self):
        """
        Delete a node from the head of the linked list.
        """
        if self.head is None:
            messagebox.showwarning("Warning", "Linked list is empty")
            self.info_label.config(text="List is empty", foreground="red")
            return
        
        deleted_value = self.head.data
        self.head = self.head.next
        
        self.info_label.config(text=f"Deleted from head: {deleted_value}", foreground="orange")
        self.update_count()
        self.refresh_view()
        
    def delete_from_tail(self):
        """
        Delete a node from the tail of the linked list.
        """
        if self.head is None:
            messagebox.showwarning("Warning", "Linked list is empty")
            self.info_label.config(text="List is empty", foreground="red")
            return
        
        if self.head.next is None:
            # Only one node
            deleted_value = self.head.data
            self.head = None
        else:
            # Find second-to-last node
            current = self.head
            while current.next.next is not None:
                current = current.next
            deleted_value = current.next.data
            current.next = None
        
        self.info_label.config(text=f"Deleted from tail: {deleted_value}", foreground="orange")
        self.update_count()
        self.refresh_view()
        
    def search_node(self):
        """
        Search for a node in the linked list.
        """
        try:
            value = int(self.value_entry.get())
            self.value_entry.delete(0, tk.END)
            
            current = self.head
            position = 0
            found = False
            
            while current:
                if current.data == value:
                    found = True
                    break
                current = current.next
                position += 1
            
            if found:
                self.info_label.config(text=f"Found: {value} at position {position}", foreground="green")
                messagebox.showinfo("Search Result", f"Value {value} found at position {position}!")
            else:
                self.info_label.config(text=f"Not Found: {value}", foreground="red")
                messagebox.showinfo("Search Result", f"Value {value} not found in the list.")
                
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            
    def count_nodes(self):
        """
        Count the number of nodes in the linked list and display the result.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        
        # Update the count label
        self.update_count()
        
        # Show message box with count
        if count == 0:
            messagebox.showinfo("Count Nodes", "The linked list is empty.\nNumber of nodes: 0")
            self.info_label.config(text="Count: 0 (List is empty)", foreground="purple")
        else:
            messagebox.showinfo("Count Nodes", f"Number of nodes in the linked list: {count}")
            self.info_label.config(text=f"Count: {count} nodes", foreground="purple")
    
    def reverse_display(self):
        """
        Display the linked list in reverse order.
        """
        if self.head is None:
            messagebox.showinfo("Reverse Display", "The linked list is empty.")
            self.info_label.config(text="Reverse: List is empty", foreground="orange")
            return
        
        # Collect all values in reverse order
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        
        # Reverse the list
        reversed_values = values[::-1]
        reversed_str = " -> ".join(map(str, reversed_values))
        
        # Display result
        messagebox.showinfo("Reverse Display", 
            f"Linked list in reverse order:\n\n{reversed_str}\n\n"
            f"Original order: {' -> '.join(map(str, values))}")
        self.info_label.config(text=f"Reverse: {reversed_str}", foreground="purple")
        
        # Also call C function if available (for console output)
        if dll:
            try:
                # Note: llist_Rdisplay uses printf, so output goes to console
                # We can't easily capture it, but we'll call it anyway
                print("C function reverse display (console output):")
                # The C function would need the list pointer, which we don't maintain
                # So we'll just use Python implementation
            except Exception as e:
                print(f"Warning: C reverse display failed: {e}")
        
    def clear_list(self):
        """
        Clear the entire linked list.
        """
        self.head = None
        self.info_label.config(text="List cleared", foreground="blue")
        self.update_count()
        self.refresh_view()
        
    def update_count(self):
        """
        Update the count label with current list size.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        self.count_label.config(text=f"Count: {count}")
        
    def refresh_view(self):
        """
        Redraw the linked list visualization on the canvas.
        """
        self.canvas.delete("all")
        
        if self.head is None:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="Linked List is empty",
                font=("Arial", 16),
                fill="gray"
            )
            return
        
        # Draw the linked list horizontally
        self.draw_list()
        
        # Update scroll region
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def draw_list(self):
        """
        Draw the linked list as horizontal nodes connected by arrows.
        """
        current = self.head
        x = 100
        y = self.canvas.winfo_height() // 2
        if y <= 1:
            y = 200
        
        node_width = 80
        node_height = 60
        spacing = 120
        
        while current:
            # Draw node rectangle
            x1 = x
            y1 = y - node_height // 2
            x2 = x + node_width
            y2 = y + node_height // 2
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="lightgreen", outline="black", width=2
            )
            
            # Draw data value
            self.canvas.create_text(
                x + node_width // 2, y,
                text=str(current.data),
                font=("Arial", 14, "bold"),
                fill="black"
            )
            
            # Draw arrow to next node
            if current.next:
                arrow_x1 = x2
                arrow_y1 = y
                arrow_x2 = x + spacing - 20
                arrow_y2 = y
                
                # Draw arrow line
                self.canvas.create_line(
                    arrow_x1, arrow_y1, arrow_x2, arrow_y2,
                    fill="black", width=3, arrow=tk.LAST, arrowshape=(10, 12, 3)
                )
            
            x += spacing
            current = current.next
        
        # Draw NULL indicator at the end
        if self.head:
            self.canvas.create_text(
                x, y,
                text="NULL",
                font=("Arial", 12, "italic"),
                fill="gray"
            )

