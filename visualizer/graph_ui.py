"""
Graph Visualizer Module

This module provides a GUI interface for interacting with and visualizing
a Graph data structure. It uses ctypes to call C functions from dshelp.dll
and Tkinter Canvas to draw the graph with nodes and edges.

To extend this for other graph types:
1. Modify the ctypes structure definitions
2. Update the drawing algorithm in draw_graph()
3. Add/modify operation buttons as needed
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ctypes
import os
import math

# Try to load the DLL
dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dshelp.dll")
if not os.path.exists(dll_path):
    dll_path = "dshelp.dll"

try:
    dll = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"Warning: Could not load DLL: {e}")
    dll = None


class GraphVisualizer:
    """
    Main class for Graph visualization and interaction.
    
    This class handles:
    - Loading C functions via ctypes
    - Managing the graph state
    - Drawing the graph on canvas
    - Handling user operations (add vertex, add edge, remove edge, traverse)
    """
    
    def __init__(self, parent):
        """
        Initialize the Graph visualizer with UI components.
        
        Args:
            parent: Parent Tkinter widget (usually a Frame)
        """
        self.graph = None  # C-side graph pointer
        self.num_vertices = 0
        self.edges = []  # Python-side edge list for visualization [(src, dest, weight)]
        self._redraw_pending = False  # Flag to prevent excessive redraws
        self.traversal_path = []  # Store current traversal path for highlighting
        
        # Setup ctypes if DLL is available
        if dll:
            self.setup_ctypes()
        
        # Create UI
        self.create_ui(parent)
        
    def setup_ctypes(self):
        """
        Configure ctypes to interface with C graph functions.
        """
        # Define Node structure
        class Node(ctypes.Structure):
            pass
        
        Node._fields_ = [
            ("vertex", ctypes.c_int),
            ("weight", ctypes.c_int),
            ("next", ctypes.POINTER(Node))
        ]
        
        # Define Graph structure
        class Graph(ctypes.Structure):
            _fields_ = [
                ("numVertices", ctypes.c_int),
                ("adjLists", ctypes.POINTER(ctypes.POINTER(Node))),
                ("visited", ctypes.POINTER(ctypes.c_bool))
            ]
        
        self.Graph = Graph
        self.Node = Node
        
        # Setup function signatures
        dll.createGraph.argtypes = [ctypes.c_int]
        dll.createGraph.restype = ctypes.POINTER(Graph)
        
        dll.addEdge.argtypes = [ctypes.POINTER(Graph), ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.addEdge.restype = None
        
        dll.removeEdge.argtypes = [ctypes.POINTER(Graph), ctypes.c_int, ctypes.c_int]
        dll.removeEdge.restype = None
        
        dll.freeGraph.argtypes = [ctypes.POINTER(Graph)]
        dll.freeGraph.restype = None
        
        dll.bfs.argtypes = [ctypes.POINTER(Graph), ctypes.c_int]
        dll.bfs.restype = None
        
        dll.dfs.argtypes = [ctypes.POINTER(Graph), ctypes.c_int]
        dll.dfs.restype = None
        
    def create_ui(self, parent):
        """
        Create the user interface with controls and canvas.
        
        Args:
            parent: Parent widget
        """
        # Control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Graph creation section
        create_frame = ttk.LabelFrame(control_frame, text="Graph Setup", padding=10)
        create_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(create_frame, text="Vertices:").grid(row=0, column=0, padx=5)
        self.vertices_entry = ttk.Entry(create_frame, width=10)
        self.vertices_entry.grid(row=0, column=1, padx=5)
        ttk.Button(create_frame, text="Create Graph", command=self.create_graph).grid(row=0, column=2, padx=5)
        
        # Edge operations section
        edge_frame = ttk.LabelFrame(control_frame, text="Edge Operations", padding=10)
        edge_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(edge_frame, text="From:").grid(row=0, column=0, padx=2)
        self.src_entry = ttk.Entry(edge_frame, width=8)
        self.src_entry.grid(row=0, column=1, padx=2)
        
        ttk.Label(edge_frame, text="To:").grid(row=0, column=2, padx=2)
        self.dest_entry = ttk.Entry(edge_frame, width=8)
        self.dest_entry.grid(row=0, column=3, padx=2)
        
        ttk.Label(edge_frame, text="Weight:").grid(row=0, column=4, padx=2)
        self.weight_entry = ttk.Entry(edge_frame, width=8)
        self.weight_entry.insert(0, "1")
        self.weight_entry.grid(row=0, column=5, padx=2)
        
        # Buttons
        btn_frame = ttk.Frame(edge_frame)
        btn_frame.grid(row=1, column=0, columnspan=6, pady=5)
        
        ttk.Button(btn_frame, text="Add Edge", command=self.add_edge).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Remove Edge", command=self.remove_edge).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="BFS", command=self.bfs_traversal).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="DFS", command=self.dfs_traversal).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_graph).pack(side=tk.LEFT, padx=2)
        
        # Info label
        self.info_label = ttk.Label(control_frame, text="Ready", foreground="blue")
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # Canvas for graph visualization
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
        
        # Bind canvas resize to redraw graph
        self.canvas.bind('<Configure>', lambda e: self.on_canvas_configure())
        
    def on_canvas_configure(self, event=None):
        """
        Handle canvas resize events to redraw the graph.
        Uses a flag to prevent excessive redraws.
        Only redraws if the canvas actually changed size significantly.
        """
        if self.num_vertices > 0 and not self._redraw_pending and event:
            # Only redraw if size actually changed
            new_width = event.width
            new_height = event.height
            if new_width > 10 and new_height > 10:  # Valid size
                self._redraw_pending = True
                self.canvas.after(150, self._delayed_redraw)
    
    def _delayed_redraw(self):
        """
        Perform delayed redraw after canvas resize.
        """
        self._redraw_pending = False
        if self.num_vertices > 0:
            self.refresh_view()
    
    def create_graph(self):
        """
        Create a new graph with specified number of vertices.
        """
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                messagebox.showerror("Error", "Number of vertices must be positive")
                return
            
            # Free existing graph if any
            if self.graph and dll:
                dll.freeGraph(self.graph)
            
            # Create new graph
            if dll:
                self.graph = dll.createGraph(num_vertices)
            
            self.num_vertices = num_vertices
            self.edges = []
            
            self.info_label.config(text=f"Graph created with {num_vertices} vertices", foreground="green")
            
            # Force canvas update and refresh to ensure graph is visible
            self.canvas.update_idletasks()
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        except Exception as e:
            messagebox.showerror("Error", f"Create graph failed: {str(e)}")
            
    def add_edge(self):
        """
        Add an edge to the graph.
        """
        # Check if graph has been created (using num_vertices instead of graph pointer)
        if self.num_vertices == 0:
            messagebox.showwarning("Warning", "Please create a graph first")
            return
        
        try:
            src = int(self.src_entry.get())
            dest = int(self.dest_entry.get())
            weight = int(self.weight_entry.get() or "1")
            
            if src < 0 or src >= self.num_vertices or dest < 0 or dest >= self.num_vertices:
                messagebox.showerror("Error", f"Vertices must be between 0 and {self.num_vertices - 1}")
                return
            
            # Add to C graph if DLL is available and graph pointer exists
            if dll and self.graph:
                try:
                    dll.addEdge(self.graph, src, dest, weight)
                except Exception as e:
                    print(f"Warning: Failed to add edge to C graph: {e}")
                    # Continue with Python-side tracking
            
            # Add to Python edge list (avoid duplicates)
            edge = (src, dest, weight)
            if edge not in self.edges:
                self.edges.append(edge)
                self.info_label.config(text=f"Edge added: {src} -> {dest} (weight: {weight}) | Total edges: {len(self.edges)}", foreground="green")
                print(f"DEBUG: Edge added: {edge}, Total edges: {len(self.edges)}")
            else:
                self.info_label.config(text=f"Edge already exists: {src} -> {dest}", foreground="orange")
            
            # Clear input fields
            self.src_entry.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, "1")
            
            # Force canvas update and refresh
            self.canvas.update_idletasks()
            self.refresh_view()
            print(f"DEBUG: After refresh, edges list: {self.edges}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
        except Exception as e:
            messagebox.showerror("Error", f"Add edge failed: {str(e)}")
            
    def remove_edge(self):
        """
        Remove an edge from the graph.
        """
        # Check if graph has been created (using num_vertices instead of graph pointer)
        if self.num_vertices == 0:
            messagebox.showwarning("Warning", "Please create a graph first")
            return
        
        try:
            src = int(self.src_entry.get())
            dest = int(self.dest_entry.get())
            
            if src < 0 or src >= self.num_vertices or dest < 0 or dest >= self.num_vertices:
                messagebox.showerror("Error", f"Vertices must be between 0 and {self.num_vertices - 1}")
                return
            
            # Remove from C graph if DLL is available and graph pointer exists
            if dll and self.graph:
                try:
                    dll.removeEdge(self.graph, src, dest)
                except Exception as e:
                    print(f"Warning: Failed to remove edge from C graph: {e}")
                    # Continue with Python-side tracking
            
            # Remove from Python edge list
            edge_to_remove = None
            for edge in self.edges:
                if edge[0] == src and edge[1] == dest:
                    edge_to_remove = edge
                    break
            
            if edge_to_remove:
                self.edges.remove(edge_to_remove)
            
            self.info_label.config(text=f"Edge removed: {src} -> {dest}", foreground="orange")
            self.refresh_view()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
        except Exception as e:
            messagebox.showerror("Error", f"Remove edge failed: {str(e)}")
            
    def bfs_traversal(self):
        """
        Perform BFS traversal starting from a vertex.
        Uses Python-side implementation to work with the edge list.
        """
        if self.num_vertices == 0:
            messagebox.showwarning("Warning", "Please create a graph first")
            return
        
        try:
            start = simpledialog.askinteger("BFS", "Enter starting vertex:", minvalue=0, maxvalue=self.num_vertices - 1)
            if start is not None:
                # Build adjacency list from edges
                adj_list = {i: [] for i in range(self.num_vertices)}
                for src, dest, weight in self.edges:
                    adj_list[src].append(dest)
                
                # Perform BFS
                visited = [False] * self.num_vertices
                queue = [start]
                visited[start] = True
                traversal_order = []
                
                while queue:
                    vertex = queue.pop(0)
                    traversal_order.append(vertex)
                    
                    # Add unvisited neighbors to queue
                    for neighbor in adj_list[vertex]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                
                # Store traversal path for visualization
                self.traversal_path = traversal_order
                
                # Display result
                result = " -> ".join(map(str, traversal_order))
                if not traversal_order:
                    result = "No vertices reachable"
                
                messagebox.showinfo("BFS Traversal", 
                    f"BFS starting from vertex {start}:\n\nVisit order: {result}\n\nTotal vertices visited: {len(traversal_order)}")
                
                self.info_label.config(text=f"BFS: {result}", foreground="purple")
                
                # Also call C function if available (for console output)
                if dll and self.graph:
                    try:
                        dll.bfs(self.graph, start)
                    except Exception as e:
                        print(f"Warning: C BFS failed: {e}")
                
                # Refresh to show traversal (could add highlighting later)
                self.refresh_view()
        except Exception as e:
            messagebox.showerror("Error", f"BFS failed: {str(e)}")
            
    def dfs_traversal(self):
        """
        Perform DFS traversal starting from a vertex.
        Uses Python-side implementation to work with the edge list.
        """
        if self.num_vertices == 0:
            messagebox.showwarning("Warning", "Please create a graph first")
            return
        
        try:
            start = simpledialog.askinteger("DFS", "Enter starting vertex:", minvalue=0, maxvalue=self.num_vertices - 1)
            if start is not None:
                # Build adjacency list from edges
                adj_list = {i: [] for i in range(self.num_vertices)}
                for src, dest, weight in self.edges:
                    adj_list[src].append(dest)
                
                # Perform DFS using recursion
                visited = [False] * self.num_vertices
                traversal_order = []
                
                def dfs_util(vertex):
                    visited[vertex] = True
                    traversal_order.append(vertex)
                    
                    # Visit all unvisited neighbors
                    for neighbor in adj_list[vertex]:
                        if not visited[neighbor]:
                            dfs_util(neighbor)
                
                dfs_util(start)
                
                # Store traversal path for visualization
                self.traversal_path = traversal_order
                
                # Display result
                result = " -> ".join(map(str, traversal_order))
                if not traversal_order:
                    result = "No vertices reachable"
                
                messagebox.showinfo("DFS Traversal", 
                    f"DFS starting from vertex {start}:\n\nVisit order: {result}\n\nTotal vertices visited: {len(traversal_order)}")
                
                self.info_label.config(text=f"DFS: {result}", foreground="purple")
                
                # Also call C function if available (for console output)
                if dll and self.graph:
                    try:
                        dll.dfs(self.graph, start)
                    except Exception as e:
                        print(f"Warning: C DFS failed: {e}")
                
                # Refresh to show traversal (could add highlighting later)
                self.refresh_view()
        except Exception as e:
            messagebox.showerror("Error", f"DFS failed: {str(e)}")
            
    def clear_graph(self):
        """
        Clear the graph.
        """
        if self.graph and dll:
            dll.freeGraph(self.graph)
        
        self.graph = None
        self.num_vertices = 0
        self.edges = []
        self.traversal_path = []
        self.info_label.config(text="Graph cleared", foreground="blue")
        self.refresh_view()
        
    def refresh_view(self):
        """
        Redraw the graph visualization on the canvas.
        """
        print(f"DEBUG: refresh_view called - vertices: {self.num_vertices}, edges: {len(self.edges)}")
        
        # Clear canvas
        self.canvas.delete("all")
        
        if self.num_vertices == 0:
            # Force canvas to have minimum size
            width = max(self.canvas.winfo_width(), 400)
            height = max(self.canvas.winfo_height(), 300)
            self.canvas.create_text(
                width // 2,
                height // 2,
                text="Graph is empty. Create a graph first.",
                font=("Arial", 16),
                fill="gray"
            )
            return
        
        # Force update to get proper canvas dimensions
        self.canvas.update_idletasks()
        
        # Draw the graph
        try:
            self.draw_graph()
        except Exception as e:
            print(f"DEBUG: Error in draw_graph: {e}")
            import traceback
            traceback.print_exc()
        
        # Update scroll region
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        
        # Schedule a final update to ensure everything is visible
        self.canvas.after(10, lambda: self.canvas.update_idletasks())
        
    def draw_graph(self):
        """
        Draw the graph with vertices in a circular layout and edges connecting them.
        """
        # Get canvas dimensions - use actual canvas size or fallback
        try:
            width = self.canvas.winfo_reqwidth()
            height = self.canvas.winfo_reqheight()
            # If requested size is 1, try actual width
            if width <= 1:
                width = self.canvas.winfo_width()
            if height <= 1:
                height = self.canvas.winfo_height()
        except:
            width, height = 1000, 600
        
        # If canvas hasn't been rendered yet, use default size
        if width <= 1 or height <= 1:
            width, height = 1000, 600
        
        # Ensure minimum size
        width = max(width, 400)
        height = max(height, 300)
        
        print(f"DEBUG: Drawing graph with {self.num_vertices} vertices, {len(self.edges)} edges, canvas size: {width}x{height}")
        
        center_x = width // 2
        center_y = height // 2
        
        # Calculate radius based on number of vertices to ensure they fit
        # Use a reasonable minimum and maximum radius
        min_radius = 100
        max_radius = min(width, height) // 3
        if self.num_vertices > 0:
            # Adjust radius based on number of vertices
            base_radius = min(width, height) // 3
            radius = max(min_radius, min(base_radius, max_radius))
        else:
            radius = max_radius
        
        # Calculate vertex positions in a circle
        vertex_positions = {}
        for i in range(self.num_vertices):
            if self.num_vertices == 1:
                # Single vertex at center
                x, y = center_x, center_y
            else:
                angle = 2 * math.pi * i / self.num_vertices - math.pi / 2  # Start from top
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            vertex_positions[i] = (x, y)
        
        print(f"DEBUG: Vertex positions: {vertex_positions}")
        print(f"DEBUG: Edges to draw: {self.edges}")
        
        # Draw edges first (so they appear behind vertices)
        edges_drawn = 0
        for edge in self.edges:
            try:
                if len(edge) >= 3:
                    src, dest, weight = edge[0], edge[1], edge[2]
                    # Validate vertex indices
                    if src in vertex_positions and dest in vertex_positions:
                        x1, y1 = vertex_positions[src]
                        x2, y2 = vertex_positions[dest]
                        # Draw arrow
                        self.draw_arrow(x1, y1, x2, y2, weight)
                        edges_drawn += 1
                        print(f"DEBUG: Drew edge {src} -> {dest} from ({x1}, {y1}) to ({x2}, {y2})")
                    else:
                        print(f"DEBUG: Skipping edge {edge} - invalid vertex indices")
                else:
                    print(f"DEBUG: Skipping invalid edge format: {edge}")
            except Exception as e:
                print(f"DEBUG: Error drawing edge {edge}: {e}")
        
        print(f"DEBUG: Total edges drawn: {edges_drawn}")
        
        # Draw vertices
        for i, (x, y) in vertex_positions.items():
            # Draw circle for vertex
            radius_circle = 30
            self.canvas.create_oval(
                x - radius_circle, y - radius_circle,
                x + radius_circle, y + radius_circle,
                fill="lightcoral", outline="black", width=2
            )
            
            # Draw vertex label
            self.canvas.create_text(
                x, y,
                text=str(i),
                font=("Arial", 14, "bold"),
                fill="black"
            )
            
    def draw_arrow(self, x1, y1, x2, y2, weight):
        """
        Draw an arrow from (x1, y1) to (x2, y2) with weight label.
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            weight: Edge weight to display
        """
        # Calculate angle
        angle = math.atan2(y2 - y1, x2 - x1)
        
        # Adjust start and end points to account for vertex radius
        vertex_radius = 30
        start_x = x1 + vertex_radius * math.cos(angle)
        start_y = y1 + vertex_radius * math.sin(angle)
        end_x = x2 - vertex_radius * math.cos(angle)
        end_y = y2 - vertex_radius * math.sin(angle)
        
        # Draw line
        self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="black", width=2, arrow=tk.LAST, arrowshape=(10, 12, 3)
        )
        
        # Draw weight label at midpoint
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Offset label slightly to avoid overlapping with line
        offset = 15
        label_x = mid_x + offset * math.cos(angle + math.pi / 2)
        label_y = mid_y + offset * math.sin(angle + math.pi / 2)
        
        self.canvas.create_text(
            label_x, label_y,
            text=str(weight),
            font=("Arial", 10),
            fill="blue",
            bg="white"
        )

