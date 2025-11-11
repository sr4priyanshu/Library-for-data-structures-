"""
Binary Search Tree (BST) Visualizer Module

This module provides a GUI interface for interacting with and visualizing
a Binary Search Tree. It uses ctypes to call C functions from dshelp.dll
and Tkinter Canvas to draw the tree structure.

To extend this for other tree structures:
1. Modify the ctypes structure definitions
2. Update the drawing algorithm in draw_tree()
3. Add/modify operation buttons as needed
"""

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os
import sys

# Try to load the DLL
dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dshelp.dll")
if not os.path.exists(dll_path):
    dll_path = "dshelp.dll"  # Fallback to current directory

try:
    dll = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"Warning: Could not load DLL: {e}")
    dll = None


class BSTNode:
    """
    Python representation of the C tree structure.
    This mirrors the C struct Binary_Search_Tree.
    """
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BSTVisualizer:
    """
    Main class for BST visualization and interaction.
    
    This class handles:
    - Loading C functions via ctypes
    - Managing the BST state
    - Drawing the tree on canvas
    - Handling user operations (insert, delete, search)
    """
    
    def __init__(self, parent):
        """
        Initialize the BST visualizer with UI components.
        
        Args:
            parent: Parent Tkinter widget (usually a Frame)
        """
        self.root = None  # Python-side BST root (for visualization)
        self.c_root = None  # C-side BST root pointer
        
        # Setup ctypes if DLL is available
        if dll:
            self.setup_ctypes()
        
        # Create UI
        self.create_ui(parent)
        
    def setup_ctypes(self):
        """
        Configure ctypes to interface with C BST functions.
        This sets up function signatures and return types.
        """
        # Define the tree structure in ctypes
        class Tree(ctypes.Structure):
            pass
        
        Tree._fields_ = [
            ("left", ctypes.POINTER(Tree)),
            ("data", ctypes.c_int),
            ("right", ctypes.POINTER(Tree))
        ]
        
        self.Tree = Tree
        
        # Setup bst_insert function
        dll.bst_insert.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_insert.restype = ctypes.POINTER(Tree)
        
        # Setup bst_Delete_Node function
        dll.bst_Delete_Node.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_Delete_Node.restype = ctypes.POINTER(Tree)
        
        # Setup traversal functions
        dll.bst_displayInorder.argtypes = [ctypes.POINTER(Tree)]
        dll.bst_displayInorder.restype = None
        
        dll.bst_displayPreorder.argtypes = [ctypes.POINTER(Tree)]
        dll.bst_displayPreorder.restype = None
        
        dll.bst_displayPostorder.argtypes = [ctypes.POINTER(Tree)]
        dll.bst_displayPostorder.restype = None
        
        # Setup statistics functions
        dll.bst_countNodes.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_countNodes.restype = ctypes.c_int
        
        dll.bst_One_child.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_One_child.restype = ctypes.c_int
        
        dll.bst_Two_child.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_Two_child.restype = ctypes.c_int
        
        dll.bst_Common_Parent.argtypes = [ctypes.POINTER(Tree), ctypes.c_int]
        dll.bst_Common_Parent.restype = ctypes.c_int
        
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
        self.value_entry.bind("<Return>", lambda e: self.insert_node())
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Insert", command=self.insert_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_tree).pack(side=tk.LEFT, padx=2)
        
        # Traversal buttons
        traversal_frame = ttk.LabelFrame(input_frame, text="Traversals", padding=5)
        traversal_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Button(traversal_frame, text="PreOrder", command=self.preorder_traversal).pack(side=tk.LEFT, padx=2)
        ttk.Button(traversal_frame, text="InOrder", command=self.inorder_traversal).pack(side=tk.LEFT, padx=2)
        ttk.Button(traversal_frame, text="PostOrder", command=self.postorder_traversal).pack(side=tk.LEFT, padx=2)
        
        # Statistics buttons
        stats_frame = ttk.LabelFrame(input_frame, text="Tree Statistics", padding=5)
        stats_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Button(stats_frame, text="Count Nodes", command=self.count_nodes).pack(side=tk.LEFT, padx=2)
        ttk.Button(stats_frame, text="One Child", command=self.count_one_child).pack(side=tk.LEFT, padx=2)
        ttk.Button(stats_frame, text="Two Children", command=self.count_two_children).pack(side=tk.LEFT, padx=2)
        ttk.Button(stats_frame, text="Common Parent", command=self.count_common_parent).pack(side=tk.LEFT, padx=2)
        
        # Info label
        self.info_label = ttk.Label(control_frame, text="Ready", foreground="blue")
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # Canvas for tree visualization
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=1000, height=600)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def insert_node(self):
        """
        Insert a node into the BST.
        Gets value from input field and updates both C and Python representations.
        """
        try:
            value = int(self.value_entry.get())
            self.value_entry.delete(0, tk.END)
            
            if dll and self.c_root:
                # Use C function
                self.c_root = dll.bst_insert(self.c_root, value)
            elif dll:
                # First node
                null_ptr = ctypes.POINTER(self.Tree)(None)
                self.c_root = dll.bst_insert(null_ptr, value)
            
            # Update Python representation for visualization
            self.root = self.insert_python(self.root, value)
            
            self.info_label.config(text=f"Inserted: {value}", foreground="green")
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        except Exception as e:
            messagebox.showerror("Error", f"Insert failed: {str(e)}")
            
    def insert_python(self, node, value):
        """
        Python-side BST insert for visualization purposes.
        
        Args:
            node: Current node (BSTNode or None)
            value: Value to insert
            
        Returns:
            Root node of the tree
        """
        if node is None:
            return BSTNode(value)
        
        if value < node.data:
            node.left = self.insert_python(node.left, value)
        elif value > node.data:
            node.right = self.insert_python(node.right, value)
        
        return node
        
    def delete_node(self):
        """
        Delete a node from the BST.
        """
        try:
            value = int(self.value_entry.get())
            self.value_entry.delete(0, tk.END)
            
            if dll and self.c_root:
                self.c_root = dll.bst_Delete_Node(self.c_root, value)
            
            # Update Python representation
            self.root = self.delete_python(self.root, value)
            
            self.info_label.config(text=f"Deleted: {value}", foreground="orange")
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")
            
    def delete_python(self, node, value):
        """
        Python-side BST delete for visualization.
        
        Args:
            node: Current node
            value: Value to delete
            
        Returns:
            Updated node (or None if deleted)
        """
        if node is None:
            return None
        
        if value < node.data:
            node.left = self.delete_python(node.left, value)
        elif value > node.data:
            node.right = self.delete_python(node.right, value)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children: get inorder successor
            min_node = self.find_min(node.right)
            node.data = min_node.data
            node.right = self.delete_python(node.right, min_node.data)
        
        return node
        
    def find_min(self, node):
        """Find minimum value node in subtree."""
        while node.left:
            node = node.left
        return node
        
    def search_node(self):
        """
        Search for a node in the BST.
        """
        try:
            value = int(self.value_entry.get())
            self.value_entry.delete(0, tk.END)
            
            found = self.search_python(self.root, value)
            
            if found:
                self.info_label.config(text=f"Found: {value}", foreground="green")
                messagebox.showinfo("Search Result", f"Value {value} found in the tree!")
            else:
                self.info_label.config(text=f"Not Found: {value}", foreground="red")
                messagebox.showinfo("Search Result", f"Value {value} not found in the tree.")
                
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            
    def search_python(self, node, value):
        """
        Python-side BST search.
        
        Args:
            node: Current node
            value: Value to search for
            
        Returns:
            True if found, False otherwise
        """
        if node is None:
            return False
        
        if value == node.data:
            return True
        elif value < node.data:
            return self.search_python(node.left, value)
        else:
            return self.search_python(node.right, value)
            
    def clear_tree(self):
        """
        Clear the entire BST.
        """
        self.root = None
        self.c_root = None
        self.info_label.config(text="Tree cleared", foreground="blue")
        self.refresh_view()
        
    def preorder_traversal(self):
        """
        Perform PreOrder traversal (Root, Left, Right) and display the result.
        """
        if self.root is None:
            messagebox.showinfo("PreOrder Traversal", "Tree is empty")
            self.info_label.config(text="PreOrder: Tree is empty", foreground="orange")
            return
        
        result = []
        self._preorder_python(self.root, result)
        traversal_str = " -> ".join(map(str, result))
        
        messagebox.showinfo("PreOrder Traversal", 
            f"PreOrder traversal (Root, Left, Right):\n\n{traversal_str}\n\nTotal nodes: {len(result)}")
        self.info_label.config(text=f"PreOrder: {traversal_str}", foreground="purple")
        
        # Also call C function if available (for console output)
        if dll and self.c_root:
            try:
                dll.bst_displayPreorder(self.c_root)
            except Exception as e:
                print(f"Warning: C PreOrder failed: {e}")
    
    def inorder_traversal(self):
        """
        Perform InOrder traversal (Left, Root, Right) and display the result.
        """
        if self.root is None:
            messagebox.showinfo("InOrder Traversal", "Tree is empty")
            self.info_label.config(text="InOrder: Tree is empty", foreground="orange")
            return
        
        result = []
        self._inorder_python(self.root, result)
        traversal_str = " -> ".join(map(str, result))
        
        messagebox.showinfo("InOrder Traversal", 
            f"InOrder traversal (Left, Root, Right):\n\n{traversal_str}\n\nTotal nodes: {len(result)}")
        self.info_label.config(text=f"InOrder: {traversal_str}", foreground="purple")
        
        # Also call C function if available (for console output)
        if dll and self.c_root:
            try:
                dll.bst_displayInorder(self.c_root)
            except Exception as e:
                print(f"Warning: C InOrder failed: {e}")
    
    def postorder_traversal(self):
        """
        Perform PostOrder traversal (Left, Right, Root) and display the result.
        """
        if self.root is None:
            messagebox.showinfo("PostOrder Traversal", "Tree is empty")
            self.info_label.config(text="PostOrder: Tree is empty", foreground="orange")
            return
        
        result = []
        self._postorder_python(self.root, result)
        traversal_str = " -> ".join(map(str, result))
        
        messagebox.showinfo("PostOrder Traversal", 
            f"PostOrder traversal (Left, Right, Root):\n\n{traversal_str}\n\nTotal nodes: {len(result)}")
        self.info_label.config(text=f"PostOrder: {traversal_str}", foreground="purple")
        
        # Also call C function if available (for console output)
        if dll and self.c_root:
            try:
                dll.bst_displayPostorder(self.c_root)
            except Exception as e:
                print(f"Warning: C PostOrder failed: {e}")
    
    def _preorder_python(self, node, result):
        """
        Helper function for PreOrder traversal (Root, Left, Right).
        
        Args:
            node: Current node
            result: List to store traversal result
        """
        if node is not None:
            result.append(node.data)  # Visit root
            self._preorder_python(node.left, result)  # Traverse left
            self._preorder_python(node.right, result)  # Traverse right
    
    def _inorder_python(self, node, result):
        """
        Helper function for InOrder traversal (Left, Root, Right).
        
        Args:
            node: Current node
            result: List to store traversal result
        """
        if node is not None:
            self._inorder_python(node.left, result)  # Traverse left
            result.append(node.data)  # Visit root
            self._inorder_python(node.right, result)  # Traverse right
    
    def _postorder_python(self, node, result):
        """
        Helper function for PostOrder traversal (Left, Right, Root).
        
        Args:
            node: Current node
            result: List to store traversal result
        """
        if node is not None:
            self._postorder_python(node.left, result)  # Traverse left
            self._postorder_python(node.right, result)  # Traverse right
            result.append(node.data)  # Visit root
    
    def count_nodes(self):
        """
        Count the total number of nodes in the BST.
        """
        if self.root is None:
            messagebox.showinfo("Count Nodes", "Tree is empty\nTotal nodes: 0")
            self.info_label.config(text="Count Nodes: 0", foreground="orange")
            return
        
        count = self._count_nodes_python(self.root)
        
        messagebox.showinfo("Count Nodes", 
            f"Total number of nodes in the BST: {count}")
        self.info_label.config(text=f"Count Nodes: {count}", foreground="purple")
        
        # Also call C function if available
        if dll and self.c_root:
            try:
                c_count = dll.bst_countNodes(self.c_root, 0)
                print(f"C function count: {c_count}")
            except Exception as e:
                print(f"Warning: C countNodes failed: {e}")
    
    def count_one_child(self):
        """
        Count the number of nodes with exactly one child.
        """
        if self.root is None:
            messagebox.showinfo("One Child Nodes", "Tree is empty\nNodes with one child: 0")
            self.info_label.config(text="One Child: 0", foreground="orange")
            return
        
        count = self._count_one_child_python(self.root)
        
        messagebox.showinfo("One Child Nodes", 
            f"Number of nodes with exactly one child: {count}")
        self.info_label.config(text=f"One Child Nodes: {count}", foreground="purple")
        
        # Also call C function if available
        if dll and self.c_root:
            try:
                c_count = dll.bst_One_child(self.c_root, 0)
                print(f"C function one child count: {c_count}")
            except Exception as e:
                print(f"Warning: C One_child failed: {e}")
    
    def count_two_children(self):
        """
        Count the number of nodes with exactly two children.
        """
        if self.root is None:
            messagebox.showinfo("Two Children Nodes", "Tree is empty\nNodes with two children: 0")
            self.info_label.config(text="Two Children: 0", foreground="orange")
            return
        
        count = self._count_two_children_python(self.root)
        
        messagebox.showinfo("Two Children Nodes", 
            f"Number of nodes with exactly two children: {count}")
        self.info_label.config(text=f"Two Children Nodes: {count}", foreground="purple")
        
        # Also call C function if available
        if dll and self.c_root:
            try:
                c_count = dll.bst_Two_child(self.c_root, 0)
                print(f"C function two child count: {c_count}")
            except Exception as e:
                print(f"Warning: C Two_child failed: {e}")
    
    def count_common_parent(self):
        """
        Count the number of nodes that are common parents (have two children).
        This is the same as count_two_children.
        """
        if self.root is None:
            messagebox.showinfo("Common Parent Nodes", "Tree is empty\nCommon parent nodes: 0")
            self.info_label.config(text="Common Parent: 0", foreground="orange")
            return
        
        count = self._count_common_parent_python(self.root)
        
        messagebox.showinfo("Common Parent Nodes", 
            f"Number of common parent nodes (nodes with two children): {count}")
        self.info_label.config(text=f"Common Parent Nodes: {count}", foreground="purple")
        
        # Also call C function if available
        if dll and self.c_root:
            try:
                c_count = dll.bst_Common_Parent(self.c_root, 0)
                print(f"C function common parent count: {c_count}")
            except Exception as e:
                print(f"Warning: C Common_Parent failed: {e}")
    
    def _count_nodes_python(self, node):
        """
        Helper function to count total nodes in the BST.
        
        Args:
            node: Current node
            
        Returns:
            Total count of nodes
        """
        if node is None:
            return 0
        return 1 + self._count_nodes_python(node.left) + self._count_nodes_python(node.right)
    
    def _count_one_child_python(self, node):
        """
        Helper function to count nodes with exactly one child.
        
        Args:
            node: Current node
            
        Returns:
            Count of nodes with one child
        """
        if node is None:
            return 0
        
        count = 0
        count += self._count_one_child_python(node.left)
        
        # Check if current node has exactly one child
        if (node.left is None and node.right is not None) or (node.right is None and node.left is not None):
            count += 1
        
        count += self._count_one_child_python(node.right)
        return count
    
    def _count_two_children_python(self, node):
        """
        Helper function to count nodes with exactly two children.
        
        Args:
            node: Current node
            
        Returns:
            Count of nodes with two children
        """
        if node is None:
            return 0
        
        count = 0
        count += self._count_two_children_python(node.left)
        
        # Check if current node has two children
        if node.left is not None and node.right is not None:
            count += 1
        
        count += self._count_two_children_python(node.right)
        return count
    
    def _count_common_parent_python(self, node):
        """
        Helper function to count common parent nodes (nodes with two children).
        This is the same as count_two_children.
        
        Args:
            node: Current node
            
        Returns:
            Count of common parent nodes
        """
        # Common parent is the same as nodes with two children
        return self._count_two_children_python(node)
        
    def refresh_view(self):
        """
        Redraw the tree visualization on the canvas.
        """
        self.canvas.delete("all")
        
        if self.root is None:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="Tree is empty",
                font=("Arial", 16),
                fill="gray"
            )
            return
        
        # Calculate tree dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            width, height = 1000, 600
        
        # Draw tree
        self.draw_tree(self.root, width // 2, 50, width // 4, 80, 0, width, 0, height)
        
        # Update scroll region
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def draw_tree(self, node, x, y, x_offset, y_offset, min_x, max_x, min_y, max_y):
        """
        Recursively draw the BST on the canvas.
        
        This function draws nodes as circles with values and connects them
        with lines to show parent-child relationships.
        
        Args:
            node: Current node to draw
            x, y: Current position for this node
            x_offset: Horizontal spacing between levels
            y_offset: Vertical spacing between levels
            min_x, max_x, min_y, max_y: Bounds for scroll region
        """
        if node is None:
            return
        
        # Draw left subtree
        if node.left:
            left_x = x - x_offset
            left_y = y + y_offset
            # Draw line to left child
            self.canvas.create_line(x, y + 20, left_x, left_y - 20, fill="black", width=2)
            self.draw_tree(node.left, left_x, left_y, x_offset // 2, y_offset,
                          min_x, max_x, min_y, max_y)
        
        # Draw right subtree
        if node.right:
            right_x = x + x_offset
            right_y = y + y_offset
            # Draw line to right child
            self.canvas.create_line(x, y + 20, right_x, right_y - 20, fill="black", width=2)
            self.draw_tree(node.right, right_x, right_y, x_offset // 2, y_offset,
                          min_x, max_x, min_y, max_y)
        
        # Draw current node (circle with value)
        radius = 25
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="lightblue", outline="black", width=2
        )
        self.canvas.create_text(
            x, y,
            text=str(node.data),
            font=("Arial", 12, "bold"),
            fill="black"
        )

