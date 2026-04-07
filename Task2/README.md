![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Data Structure](https://img.shields.io/badge/Data%20Structure-Heap-blue)
![Algorithm](https://img.shields.io/badge/Algorithm-Heap%20Sort-green)


## Contents
- [Overview](#overview)
- [Data Structure](#datastructure)
- [Algorithm](#algorithm)
- [Modules](#modules)
- [Installation](#installation)
- [User Guide](#userGuide)

## <a name="overview">Overview</a>
This project implements a **Max Heap** data structure and the **Heap Sort** algorithm through a **CLI-based Task Manager System** that manages tasks by priority. The Max Heap enables efficient retrieval of the highest-priority task, while Heap Sort demonstrates systematic task sorting by priority.

## <a name="datastructure">Data Structure: Heap</a>

### Description
This Task Manager System uses a **Max Heap** to store and manage tasks efficiently.  
The heap ensures that the task with the **highest priority** (largest priority number) is always at the root and can be retrieved or removed immediately.

### Main Methods Implemented In The System
| Method | Description | Time Complexity |
|--------|-------------|----------------|
| `insert(task)` | Add a new task and restore heap order | O(log n) |
| `pop()` | Remove and return the highest priority task | O(log n) |
| `peek()` | Return the highest priority task without removing | O(1) |
| `_heapify_up()` | Sift a node up to maintain heap property | O(log n) |
| `_heapify_down()` | Sift a node down after removal | O(log n) |

## <a name="algorithm">Algorithm: Heap sort</a>
### Description
This Task Manager System uses **Heap Sort** to display all tasks in ascending order of priority (from lowest to highest) when the user selects the "Show All Tasks (Sorted)" option.

## <a name="modules">Modules</a>
| Module | Description |
|--------|-------------|
| `main.py` | Entry point and logic of application and CLI menu |
| `heap.py` | Max Heap implementation , include insert, pop, peek, heapify |
| `heap_sort.py` | Heap Sort algorithm (lowest → highest priority) |

## <a name="installation">Installation</a>

### Prerequisites
- Python 3.0 or higher
- Standard library only (no extra packages needed)

### Steps
1. **Download or copy all Python files into the same folder:**
- `main.py`
- `heap.py`
- `heap_sort.py`

2. **Run the application**
```
python main.py
```

## <a name="userGuide">User Guide</a>

### First Time Use
Launch the application by executing `python main.py`.  
You will see the main menu with six options.

---

### 1. Add New Task
1. Select option `1`
2. Enter task name
3. Enter priority (1 = lowest, 10 = highest)
4. Task is automatically inserted into the heap

---

### 2. Remove Highest Priority Task
1. Select option `2`
2. The highest priority task is removed and displayed
3. If no tasks exist, an error message appears

---

### 3. View Highest Priority Task
1. Select option `3`
2. The highest priority task is shown

---

### 4. Show All Tasks (Sorted by Priority)
1. Select option `4`
2. All tasks are displayed from **lowest priority → highest priority** using **Heap Sort**

---

### 5. Show All Tasks (Unsorted)
1. Select option `5`
2. All sorted tasks are displayed in the order

---

### 6. Exit
1. Select option `6`
2. The program terminates

---
