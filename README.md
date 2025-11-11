# Data Structures Visualizer

A graphical user interface (GUI) application for visualizing and interacting with data structures implemented in C. This project provides an intuitive way to see how Linked Lists, Binary Search Trees, and Graphs work through real-time visualizations.

## 📋 Features

- **Binary Search Tree (BST)**: Insert, delete, search nodes with hierarchical tree visualization
- **Linked List**: Insert at head, delete from head/tail, search with horizontal node visualization
- **Graph**: Create graphs, add/remove edges, perform BFS/DFS traversals with circular node layout
- **Real-time Visualization**: See data structure changes immediately after each operation
- **Cross-language Integration**: Python GUI using ctypes to call C library functions

## 🏗️ Project Structure

```
Library-for-data-structures/
│
├── src/                    # C source files (if you have them)
│   ├── linkedlist.c
│   ├── bst.c
│   ├── graph.c
│   └── dshelp.h
│
├── build/                  # Compiled DLL location
│   └── libds.dll          # Or dshelp.dll in root
│
├── visualizer/            # Python GUI application
│   ├── main.py           # Main entry point
│   ├── bst_ui.py         # BST visualizer module
│   ├── linkedlist_ui.py  # Linked List visualizer module
│   └── graph_ui.py       # Graph visualizer module
│
├── dshelp.dll            # Compiled C shared library
├── dshelp.h              # Header file with function declarations
└── README.md             # This file
```

## 🔧 Prerequisites

### Required Software

1. **Python 3.7+** 
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to add Python to PATH during installation

2. **GCC Compiler** (for building the DLL)
   - **Windows**: Install [MinGW-w64](https://www.mingw-w64.org/downloads/) or use [MSYS2](https://www.msys2.org/)
   - **Alternative**: Use Visual Studio Build Tools

3. **Tkinter** (usually included with Python)
   - If not available, install via: `pip install tk`

## 📦 Building the DLL

### Step 1: Compile the C Source Files

Open a terminal/command prompt in the project root directory and run:

```bash
# If you have a build directory
gcc -shared -o build/libds.dll src/*.c -I.

# Or compile directly to root directory
gcc -shared -o dshelp.dll bst.c llist.c graph.c -I.
```

**For Windows with MinGW:**
```bash
gcc -shared -o dshelp.dll bst.c llist.c graph.c -I. -Wl,--out-implib,dshelp.lib
```

**For Visual Studio (Developer Command Prompt):**
```cmd
cl /LD bst.c llist.c graph.c /Fe:dshelp.dll /I.
```

### Step 2: Verify DLL Creation

Check that `dshelp.dll` (or `build/libds.dll`) exists in your project directory.

**Note**: If you place the DLL in a `build/` directory, update the DLL path in the Python files:
- In `bst_ui.py`, `linkedlist_ui.py`, and `graph_ui.py`, modify:
  ```python
  dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build", "libds.dll")
  ```

## 🚀 Running the Application

### Method 1: Direct Python Execution

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd path/to/Library-for-data-structures
   ```
3. Run the main application:
   ```bash
   python visualizer/main.py
   ```

### Method 2: From Visualizer Directory

```bash
cd visualizer
python main.py
```

## 💻 Usage Guide

### Binary Search Tree

1. Select the **"Binary Search Tree"** tab
2. Enter a value in the input field
3. Click **"Insert"** to add a node
4. Click **"Delete"** to remove a node
5. Click **"Search"** to find a value
6. Click **"Clear"** to reset the tree
7. The tree visualization updates automatically

### Linked List

1. Select the **"Linked List"** tab
2. Enter a value in the input field
3. Click **"Insert at Head"** to add at the beginning
4. Click **"Delete from Head"** to remove the first node
5. Click **"Delete from Tail"** to remove the last node
6. Click **"Search"** to find a value
7. The list visualization shows nodes connected horizontally

### Graph

1. Select the **"Graph"** tab
2. Enter the number of vertices and click **"Create Graph"**
3. Enter source, destination, and weight (optional, default: 1)
4. Click **"Add Edge"** to connect vertices
5. Click **"Remove Edge"** to disconnect vertices
6. Click **"BFS"** or **"DFS"** to perform traversals
7. The graph displays vertices in a circular layout with labeled edges

## 🎨 Visual Features

- **BST**: Hierarchical tree view with parent-child relationships
- **Linked List**: Horizontal flow with arrows showing connections
- **Graph**: Circular node layout with directed edges and weight labels
- **Color Coding**: Different colors for different data structures
- **Scrollable Canvas**: Handle large data structures with scrollbars

## 🔨 Building an Executable (.exe)

To create a standalone Windows executable, use **PyInstaller**:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Create Executable

```bash
# From project root
pyinstaller --onefile --windowed --name "DataStructuresVisualizer" --add-data "dshelp.dll;." visualizer/main.py
```

Or create a spec file for more control:

```bash
pyinstaller --name "DataStructuresVisualizer" visualizer/main.py
```

Then edit the generated `.spec` file to include the DLL:

```python
# In the spec file, add to datas:
datas=[('dshelp.dll', '.')],
```

### Step 3: Run PyInstaller

```bash
pyinstaller DataStructuresVisualizer.spec
```

The executable will be in the `dist/` directory.

**Note**: Make sure `dshelp.dll` is in the same directory as the executable when distributing.

## 🐛 Troubleshooting

### DLL Not Found Error

**Problem**: `OSError: [WinError 126] The specified module could not be found`

**Solutions**:
1. Ensure `dshelp.dll` is in the project root or `build/` directory
2. Check that all dependencies of the DLL are available (e.g., MinGW runtime)
3. Verify the DLL path in the Python files matches your directory structure
4. On Windows, you may need to add the DLL directory to PATH

### Import Errors

**Problem**: `ModuleNotFoundError` or import issues

**Solutions**:
1. Ensure you're running from the correct directory
2. Check that all Python files are in the `visualizer/` directory
3. Verify Python version is 3.7 or higher: `python --version`

### Compilation Errors

**Problem**: GCC compilation fails

**Solutions**:
1. Ensure GCC is installed and in PATH: `gcc --version`
2. Check that all C source files are present
3. Verify header file paths are correct
4. On Windows, ensure MinGW-w64 is properly installed

### GUI Not Displaying

**Problem**: Window doesn't appear or crashes

**Solutions**:
1. Check Tkinter installation: `python -m tkinter`
2. Update graphics drivers
3. Try running with `pythonw` instead of `python` on Windows

## 📝 Extending the Code

### Adding a New Data Structure

1. Create a new Python file (e.g., `heap_ui.py`) in the `visualizer/` directory
2. Follow the pattern from existing modules:
   - Define ctypes structures matching C structs
   - Setup function signatures
   - Create UI with Canvas for visualization
   - Implement drawing functions
3. Import and add to `main.py`:
   ```python
   from heap_ui import HeapVisualizer
   # Add tab in create_tabs()
   ```

### Modifying Visualizations

- **BST**: Modify `draw_tree()` in `bst_ui.py`
- **Linked List**: Modify `draw_list()` in `linkedlist_ui.py`
- **Graph**: Modify `draw_graph()` in `graph_ui.py`

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For issues or questions, please open an issue on the GitHub repository.

---

**Happy Visualizing! 🎉**

