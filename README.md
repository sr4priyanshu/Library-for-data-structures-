# 📚 Library for Data Structures in C

A **modular and reusable library** that implements fundamental **data structures** in the C programming language — designed for educational use, algorithmic practice, and integration into larger C projects.

---

## 🧩 Overview

This library provides ready-to-use implementations of commonly used data structures such as:

- **Linked Lists**
- **Binary Search Trees (BST)**
- **Graphs**

Each data structure is implemented as a separate C module with clear function definitions and header files for easy integration into any C project.

---

## 🗂️ Folder Structure
```bash
Library-for-data-structures/
├── dshelp.h # Common helper functions and type definitions
├── llist.c # Linked List implementation
├── bst.c # Binary Search Tree implementation
├── graph.c # Graph implementation
├── dshelp.dll # Precompiled dynamic library (for Windows)
└── README.md # Project documentation
```

---

## ⚙️ Features

| Data Structure | Key Operations | Source File |
|----------------|----------------|--------------|
| **Linked List** | Insert, Delete, Traverse, Search | `llist.c` |
| **Binary Search Tree (BST)** | Insert, Delete, Search, Inorder/Preorder/Postorder traversal | `bst.c` |
| **Graph** | Add vertex, Add edge, Depth-First Search (DFS), Breadth-First Search (BFS) | `graph.c` |

---

## 🚀 Getting Started

### 🧠 Prerequisites

Ensure you have a C compiler installed on your system:

- **Windows:** MinGW / MSVC / Code::Blocks  
- **Linux / macOS:** GCC or Clang  

You can verify installation by running:

```bash
gcc --version
```
