import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.db.database import TaskDatabase
from src.bst import TaskBST
from src.TaskStack import TaskStack
from src.queue import NotificationQueue
from src.LinkedList import TaskLinkedList
from src.Graph import TaskGraph


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager (Tabbed Interface)")
        self.root.geometry("900x700")
        self.root.configure(bg="lightblue")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", background="lightblue", foreground="black")
        style.configure("TButton", background="lightgray", foreground="black", padding=6)
        style.map("TButton", background=[("active", "gray")])
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TLabelframe", background="lightblue", foreground="black", padding=10)
        style.configure("TLabelframe.Label", background="lightblue", foreground="black")
        style.configure("TNotebook", background="lightblue")
        style.configure("TNotebook.Tab", background="lightsteelblue", foreground="black", padding=10)
        style.map("TNotebook.Tab", background=[("selected", "lavender")])

        self.db = TaskDatabase()
        self.bst = TaskBST()
        self.stack = TaskStack()
        self.notifications = NotificationQueue()
        self.linked_list = TaskLinkedList()
        self.graph = TaskGraph()
        self.log_entries = []

        self.create_menu()
        self.create_notebook_tabs()
        self.load_tasks()

    def create_menu(self):
        menubar = tk.Menu(self.root, background="lightsteelblue", foreground="black")
        helpmenu = tk.Menu(menubar, tearoff=0, background="lightsteelblue", foreground="black")
        helpmenu.add_command(label="How to Use", command=self.show_help)
        helpmenu.add_command(label="Export Log", command=self.export_logs_to_file)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

    def create_notebook_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.task_tab = ttk.Frame(notebook)
        self.history_tab = ttk.Frame(notebook)
        self.notification_tab = ttk.Frame(notebook)
        self.dependency_tab = ttk.Frame(notebook)
        self.log_tab = ttk.Frame(notebook)
