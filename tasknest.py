import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('tasknest.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    priority TEXT,
    status TEXT
)''')
conn.commit()

class Task:
    def __init__(self, title, description, due_date, priority, status="To Do"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def save_to_db(self):
        c.execute("INSERT INTO tasks (title, description, due_date, priority, status) VALUES (?, ?, ?, ?, ?)",
                  (self.title, self.description, self.due_date, self.priority, self.status))
        conn.commit()

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskNest - Enhanced Task Manager")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)

        self.tree = ttk.Treeview(root, columns=("Title", "Priority", "Status", "Due Date"), show='headings')
        self.tree.heading("Title", text="Title")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")

        self.tree.column("Title", width=250)
        self.tree.column("Priority", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("Due Date", width=120)

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.add_btn = tk.Button(button_frame, text="Add Task", width=15, command=self.add_task, bg="#4CAF50", fg="white")
        self.add_btn.grid(row=0, column=0, padx=10)

        self.update_btn = tk.Button(button_frame, text="Mark as Done", width=15, command=self.mark_done, bg="#2196F3", fg="white")
        self.update_btn.grid(row=0, column=1, padx=10)

        self.delete_btn = tk.Button(button_frame, text="Delete Task", width=15, command=self.delete_task, bg="#f44336", fg="white")
        self.delete_btn.grid(row=0, column=2, padx=10)

        self.refresh_btn = tk.Button(button_frame, text="Refresh", width=15, command=self.display_tasks, bg="#9C27B0", fg="white")
        self.refresh_btn.grid(row=0, column=3, padx=10)

        self.display_tasks()

    def add_task(self):
        title = simpledialog.askstring("Title", "Enter task title:")
        description = simpledialog.askstring("Description", "Enter task description:")
        due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
        priority = simpledialog.askstring("Priority", "Enter priority (Low/Medium/High):")

        if title:
            task = Task(title, description, due_date, priority)
            task.save_to_db()
            self.display_tasks()

    def display_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in c.execute("SELECT * FROM tasks"):
            self.tree.insert("", tk.END, values=(row[1], row[4], row[5], row[3]))

    def mark_done(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_values = self.tree.item(selected_item, 'values')
            title = selected_values[0]
            c.execute("UPDATE tasks SET status=? WHERE title=?", ("Done", title))
            conn.commit()
            self.display_tasks()
        else:
            messagebox.showwarning("Select Task", "Please select a task to mark as done.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_values = self.tree.item(selected_item, 'values')
            title = selected_values[0]
            c.execute("DELETE FROM tasks WHERE title=?", (title,))
            conn.commit()
            self.display_tasks()
        else:
            messagebox.showwarning("Select Task", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
    conn.close()
