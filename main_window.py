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

    def create_dependency_tab(self):
        frame = ttk.LabelFrame(self.dependency_tab, text="Add Task Dependencies")
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Add Dependency (task depends on):").pack(pady=5)
        self.task_main_entry = ttk.Entry(frame, width=30)
        self.task_main_entry.pack(pady=5)
        self.task_main_entry.insert(0, "Task A")

        self.task_depends_on_entry = ttk.Entry(frame, width=30)
        self.task_depends_on_entry.pack(pady=5)
        self.task_depends_on_entry.insert(0, "Task B")

        ttk.Button(frame, text="➕ Add Dependency", command=self.add_dependency).pack(pady=5)
        ttk.Button(frame, text="🧭 Show Topological Order", command=self.show_task_order).pack(pady=5)

    def create_log_tab(self):
        frame = ttk.LabelFrame(self.log_tab, text="📜 DS Operations Log")
        frame.pack(fill='both', padx=20, pady=20, expand=True)

        self.log_text = tk.Text(frame, height=25, bg='lightgray', fg='black', wrap='word', state='disabled')
        self.log_text.pack(fill='both', expand=True)

    def log(self, message):
        timestamped = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.log_entries.append(timestamped)
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, timestamped + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def export_logs_to_file(self):
        try:
            with open("ds_operations_log.txt", "w") as f:
                f.write("\n".join(self.log_entries))
            messagebox.showinfo("Export Success", "Log exported to ds_operations_log.txt")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def flash_listbox(self, color):
        original = self.task_listbox.cget("background")
        self.task_listbox.config(background=color)
        self.root.after(200, lambda: self.task_listbox.config(background=original))

    def load_tasks(self):
        tasks = self.db.get_all_tasks()
        for task_id, desc in tasks:
            priority = 5
            self.bst.insert(priority, task_id, desc)
            self.linked_list.insert(desc)
            self.graph.add_task(desc)
            self.task_listbox.insert(tk.END, f"[{priority}] {desc}")
            self.log(f"Loaded task from DB: [{priority}] {desc}")

    def show_help(self):
        messagebox.showinfo("How to Use Task Manager", (
            "🧩 To add a task:\n"
            "- Enter the task description\n"
            "- Set a priority between 1 and 10\n"
            "- Click 'Add Task'\n\n"
            "🗑 To delete or undo:\n"
            "- Select a task from the list\n"
            "- Click 'Delete Task' or 'Undo Delete'\n\n"
            "📚 Other Features:\n"
            "- View tasks by priority (BST)\n"
            "- View history (Linked List)\n"
            "- Show notifications\n"
            "- Add task dependencies\n"
            "- Perform topological sort to get task order"
        ))

    def add_task(self):
        desc = self.task_entry.get().strip()
        if not desc:
            messagebox.showerror("Missing Description", "Please enter a task description.")
            return

        try:
            priority = int(self.priority_entry.get().strip())
            if not 1 <= priority <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Priority", "Please enter a number between 1 and 10.")
            return

        self.db.add_task(desc)
        task_id = self.db.get_all_tasks()[-1][0]

        self.bst.insert(priority, task_id, desc)
        self.linked_list.insert(desc)
        self.graph.add_task(desc)

        self.task_listbox.insert(tk.END, f"[{priority}] {desc}")
        self.notifications.enqueue(f"Task added: {desc}")
        self.log(f"Added task: [{priority}] {desc}")
        self.log("Inserted into BST, LinkedList, and Graph")

        self.task_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.flash_listbox("lightgreen")



    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        index = selected[0]
        line = self.task_listbox.get(index)
        desc = line.split("] ", 1)[1]

        confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{desc}'?")
        if confirm:
            self.db.delete_task(desc)
            self.task_listbox.delete(index)
            self.stack.push((desc, 5))
            self.linked_list.delete(desc)
            self.notifications.enqueue(f"Task deleted: {desc}")
            self.log(f"Deleted task: {desc}")
            self.log("Pushed to stack, removed from LinkedList")
            self.flash_listbox("orange")

    def undo_delete(self):
        if self.stack.is_empty():
            messagebox.showinfo("Undo", "Nothing to undo.")
            return

        desc, priority = self.stack.pop()
        self.db.add_task(desc)
        task_id = self.db.get_all_tasks()[-1][0]

        self.bst.insert(priority, task_id, desc)
        self.linked_list.insert(desc)
        self.graph.add_task(desc)

        self.task_listbox.insert(tk.END, f"[{priority}] {desc}")
        self.notifications.enqueue(f"Undo: Restored task '{desc}'")
        messagebox.showinfo("Undo", f"Task '{desc}' has been restored.")
        self.log(f"Undo delete: Restored task '{desc}'")
        self.log("Inserted into BST, LinkedList, and Graph")
        self.flash_listbox("lightblue")

    def show_sorted_tasks(self):
        sorted_tasks = self.bst.inorder()
        if not sorted_tasks:
            messagebox.showinfo("No Tasks", "No tasks found.")
            return

        window = tk.Toplevel(self.root)
        window.title("Tasks by Priority (BST)")
        window.geometry("450x300")

        listbox = tk.Listbox(window, width=50, height=15)
        listbox.pack(pady=10)

        for priority, _, desc in sorted_tasks:
            listbox.insert(tk.END, f"[{priority}] {desc}")

        self.log("Displayed BST in-order traversal")

    def show_task_history(self):
        task_list = self.linked_list.display()
        if not task_list:
            messagebox.showinfo("No Tasks", "No task history available.")
            return

        window = tk.Toplevel(self.root)
        window.title("Task History (Linked List)")
        window.geometry("450x300")

        listbox = tk.Listbox(window, width=50, height=15)
        listbox.pack(pady=10)

        for task in task_list:
            listbox.insert(tk.END, task)

        self.log("Displayed LinkedList task history")

    def show_notification(self):
        if self.notifications.is_empty():
            messagebox.showinfo("Notifications", "No new notifications.")
        else:
            message = self.notifications.dequeue()
            messagebox.showinfo("Notification", message)
            self.log(f"Dequeued notification: {message}")

    def add_dependency(self):
        task = self.task_main_entry.get().strip()
        depends_on = self.task_depends_on_entry.get().strip()

        if not task or not depends_on:
            messagebox.showerror("Input Error", "Both Task A and Task B must be filled.")
            return
        if task == depends_on:
            messagebox.showerror("Invalid Dependency", "A task cannot depend on itself.")
            return

        self.graph.add_task(task)
        self.graph.add_task(depends_on)
        self.graph.add_dependency(task, depends_on)
        self.notifications.enqueue(f"Added dependency: {task} → {depends_on}")
        messagebox.showinfo("Success", f"{task} now depends on {depends_on}")
        self.log(f"Added dependency: {task} → {depends_on}")

    def show_task_order(self):
        try:
            order = self.graph.topological_sort()
            if not order:
                messagebox.showinfo("No Tasks", "No tasks available in graph.")
                return

            window = tk.Toplevel(self.root)
            window.title("Task Order (Topological Sort)")
            window.geometry("400x300")

            listbox = tk.Listbox(window, width=50, height=15)
            listbox.pack(pady=10)

            for task in order:
                listbox.insert(tk.END, task)

            self.log("Performed topological sort")

        except Exception as e:
            messagebox.showerror("Error", f"Topological sort failed: {e}")
            self.log(f"Topological sort error: {e}")


if _name_ == "_main_":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
