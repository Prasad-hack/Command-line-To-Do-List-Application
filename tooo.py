import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3


def initialize_database():
    connect = sqlite3.connect("TODO.db")
    cursor = connect.cursor()

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            due_date TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')

    connect.commit()
    connect.close()

def activate(event):
    if due_date_entry.get() == placeholder:
        due_date_entry.delete(0, tk.END)
        due_date_entry.config(fg='black')

def disactivate(event):
    if due_date_entry.get() == '':
        due_date_entry.insert(0, placeholder)
        due_date_entry.config(fg='grey')

def add_task():
    task = task_entry.get()
    due_date = due_date_entry.get()
    priority = priority_var.get()

    if task and due_date and due_date != placeholder:
        formatted_due_date = datetime.strptime(due_date, "%Y/%m/%d").strftime("%d-%b-%Y")
        
        
        connect = sqlite3.connect("TODO.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO tasks (task, due_date, priority) VALUES (?, ?, ?)",(task, formatted_due_date, priority))
        connect.commit()
        connect.close()

        task_listbox.insert(tk.END, f"{task} (Due: {formatted_due_date}, Priority: {priority})")
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        due_date_entry.insert(0, placeholder)
        due_date_entry.config(fg='grey')
        priority_var.set(priority_options[0])
    else:
        messagebox.showwarning("Warning", "Please enter both task and due date.")

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        

        task_id = task_text.split()[0]

       
        connect = sqlite3.connect("todo.db")
        cursor = connect.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        connect.commit()
        connect.close()

        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def mark_as_completed():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        task_id = task_text.split()[0]

        
        connect = sqlite3.connect("TODO.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        connect.commit()
        connect.close()

        if "(Completed)" not in task_text:
            task_listbox.delete(selected_task_index)
            task_listbox.insert(tk.END, f"{task_text} (Completed)")
        else:
            messagebox.showinfo("Info", "Task is already marked as completed.")
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

def list_tasks():
   task_listbox.delete(0, tk.END)

    
   connect = sqlite3.connect("TODO.db")
   cursor = connect.cursor()
   cursor.execute("SELECT id, task, due_date, priority, completed FROM tasks")
   tasks = cursor.fetchall()
   connect.close()

   for task_id, task, due_date, priority, completed in tasks:
       completion_status = "(Completed)" if completed else ""
       task_listbox.insert(tk.END, f"{task_id}. {task} (Due: {due_date}, Priority: {priority}) {completion_status}")


root = tk.Tk()
root.title("Command LIne To-Do-List Application")
root.configure(bg="lightblue")


priority_options = ["Low", "Medium", "High"]


task_entry = tk.Entry(root, width=40)
placeholder = "YYYY/MM/DD"
due_date_entry = tk.Entry(root, width=40, fg='grey', bg='white', font=('Arial', 14))  
due_date_entry.insert(0, placeholder)
due_date_entry.bind('<FocusIn>', activate)
due_date_entry.bind('<FocusOut>', disactivate)
priority_var = tk.StringVar(root)
priority_var.set(priority_options[0])
priority_menu = tk.OptionMenu(root, priority_var, *priority_options)
add_button = tk.Button(root, text="Add Task", command=add_task, fg='black', font=('Arial', 14)) 
remove_button = tk.Button(root, text="Remove Task", command=remove_task, fg='black', font=('Arial', 14))  
mark_button = tk.Button(root, text="Mark as Completed", command=mark_as_completed, fg='black', font=('Arial', 14))  
list_button = tk.Button(root, text="List Tasks", command=list_tasks, fg='black',font=('Arial', 14)) 
task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, fg='black', font=('Arial', 14))  



root.update_idletasks()
win_width = root.winfo_width()
win_height = root.winfo_height()

for i in range(4): 
    root.grid_rowconfigure(i, weight=1)
for i in range(4):  
    root.grid_columnconfigure(i, weight=1)


widgets = [
    (task_entry, 0, 0, 1, 4, "nsew"),
    (due_date_entry, 1, 0, 1, 2, "nsew"),
    (priority_menu, 1, 2, 1, 2, "nsew"),
    (add_button, 2, 0, 1, 1, "nsew"),
    (remove_button, 2, 1, 1, 1, "nsew"),
    (mark_button, 2, 2, 1, 1, "nsew"),
    (list_button, 2, 3, 1, 1, "nsew"),
    (task_listbox, 3, 0, 1, 4, "nsew")
]

for widget, row, column, rowspan, columnspan, sticky in widgets:
    widget.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=20, pady=20, sticky=sticky)

initialize_database()

root.mainloop()