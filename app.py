import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import time
import threading

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager")
        master.geometry("600x500")

        # Initialize tasks
        self.tasks = self.load_tasks()

        # Create GUI elements
        self.create_widgets()

    def load_tasks(self):
        try:
            with open("db.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open("db.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def create_widgets(self):
        # Task List Frame
        list_frame = tk.Frame(self.master)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar for task list
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(list_frame, width=70, yscrollcommand=scrollbar.set)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        self.refresh_task_list()

        # Buttons Frame
        button_frame = tk.Frame(self.master)
        button_frame.pack(padx=10, pady=10)

        # Create Buttons
        buttons = [
            ("Create New Task", self.create_new_task),
            ("Set Current Task", self.set_current_task),
            ("Modify Task", self.modify_task),
            ("Delete Task", self.delete_task)
        ]

        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command, width=20).pack(side=tk.LEFT, padx=5)

    def refresh_task_list(self):
        # Clear existing items
        self.task_listbox.delete(0, tk.END)
        
        # Sort tasks by deadline
        self.tasks = sorted(self.tasks, key=lambda x: x['deadline'], reverse=True)
        
        # Populate listbox
        for task in self.tasks:
            display_text = f"Task: {task['task_name']} | Deadline: {task['deadline']} hrs | By: {task['person_name']}"
            self.task_listbox.insert(tk.END, display_text)

    def create_new_task(self):
        # Create a new window for task input
        task_window = tk.Toplevel(self.master)
        task_window.title("Create New Task")
        task_window.geometry("400x300")

        # Input fields
        labels = ["Name", "Task Name", "Task Description", "Deadline (hours)"]
        entries = []

        for i, label_text in enumerate(labels):
            tk.Label(task_window, text=label_text).pack(pady=(10, 0))
            entry = tk.Entry(task_window, width=40)
            entry.pack(pady=(0, 10))
            entries.append(entry)

        def submit_task():
            # Validate inputs
            if not all(entry.get().strip() for entry in entries):
                messagebox.showerror("Error", "All fields are required!")
                return

            # Create task dictionary
            task = {
                "person_name": entries[0].get(),
                "task_name": entries[1].get(),
                "task_description": entries[2].get(),
                "deadline": int(entries[3].get()),
                "roll_no": len(self.tasks) + 1
            }

            # Add to tasks list
            self.tasks.append(task)
            
            # Sort tasks by deadline
            self.tasks = sorted(self.tasks, key=lambda x: x['deadline'], reverse=True)
            
            # Save to file
            self.save_tasks()

            # Refresh list
            self.refresh_task_list()

            # Close window
            task_window.destroy()
            messagebox.showinfo("Success", "Task added successfully!")

        # Submit button
        tk.Button(task_window, text="Submit Task", command=submit_task).pack(pady=10)

    def set_current_task(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks available!")
            return

        # Let user select a task
        task_names = [task['task_name'] for task in self.tasks]
        task_name = simpledialog.askstring("Select Task", "Enter Task Name:", initialvalue=task_names[0])
        
        if not task_name:
            return

        # Find the task
        task_found = next((task for task in self.tasks if task["task_name"] == task_name), None)

        if not task_found:
            messagebox.showerror("Error", "Task not found!")
            return

        # Get time to work on task
        time_hours = simpledialog.askfloat("Time Allocation", "Time in hours:", minvalue=0.1)
        
        if not time_hours:
            return

        # Start a timer thread
        def task_timer():
            messagebox.showinfo("Task Timer", f"Working on '{task_name}' for {time_hours} hours.")
            time.sleep(time_hours * 3600)  # Convert hours to seconds
            messagebox.showinfo("Task Timer", f"Time is over for task '{task_name}'.")

        # Start timer in a separate thread
        timer_thread = threading.Thread(target=task_timer)
        timer_thread.start()

    def modify_task(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks available!")
            return

        # Let user select a task
        task_names = [task['task_name'] for task in self.tasks]
        task_name = simpledialog.askstring("Modify Task", "Enter Task Name:", initialvalue=task_names[0])
        
        if not task_name:
            return

        # Find the task
        task_found = next((task for task in self.tasks if task["task_name"] == task_name), None)

        if not task_found:
            messagebox.showerror("Error", "Task not found!")
            return

        # Get new deadline
        new_deadline = simpledialog.askinteger("Modify Deadline", "Enter new deadline in hours:", 
                                                initialvalue=task_found['deadline'], minvalue=1)
        
        if new_deadline is not None:
            task_found['deadline'] = new_deadline
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task deadline updated!")

    def delete_task(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks available!")
            return

        # Let user select a task
        task_names = [task['task_name'] for task in self.tasks]
        task_name = simpledialog.askstring("Delete Task", "Enter Task Name:", initialvalue=task_names[0])
        
        if not task_name:
            return

        # Remove task
        self.tasks = [task for task in self.tasks if task["task_name"] != task_name]
        
        # Save and refresh
        self.save_tasks()
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task deleted successfully!")

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
