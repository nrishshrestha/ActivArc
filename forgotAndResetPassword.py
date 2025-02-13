import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib

# Database initialization
def init_database():
    conn = sqlite3.connect('ActivArcDatabase.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        security_question TEXT NOT NULL,
        security_answer_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create some sample users (in real application, you'd have proper user registration)
    sample_users = [
        ('john_doe', 'password123', 'What is your mother\'s maiden name?', 'Smith'),
        ('jane_doe', 'password456', 'What was your first pet\'s name?', 'Fluffy'),
        ('bob_smith', 'password789', 'What city were you born in?', 'New York')
    ]
    
    # Hash passwords and security answers before storing
    for username, password, question, answer in sample_users:
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            answer_hash = hashlib.sha256(answer.lower().encode()).hexdigest()
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, security_question, security_answer_hash)
            VALUES (?, ?, ?, ?)
            ''', (username, password_hash, question, answer_hash))
        except sqlite3.IntegrityError:
            pass  # Skip if user already exists
    
    conn.commit()
    conn.close()

def reset_password():
    username = username_entry.get()
    security_ans = security_answer.get()
    new_pwd = new_password.get()
    confirm_pwd = confirm_password.get()
    
    if not all([username, security_ans, new_pwd, confirm_pwd]):
        messagebox.showerror("Error", "All fields are required")
        return
        
    if new_pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Connect to database
    conn = sqlite3.connect('ActivArcDatabase.db')
    cursor = conn.cursor()
    
    # Check if user exists and verify security answer
    cursor.execute('''
    SELECT security_answer_hash, security_question 
    FROM users 
    WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    
    if not result:
        messagebox.showerror("Error", "Username not found")
        conn.close()
        return
    
    stored_answer_hash, stored_question = result
    provided_answer_hash = hashlib.sha256(security_ans.lower().encode()).hexdigest()
    
    if provided_answer_hash != stored_answer_hash:
        messagebox.showerror("Error", "Incorrect security answer")
        conn.close()
        return
    
    # Update password
    new_password_hash = hashlib.sha256(new_pwd.encode()).hexdigest()
    cursor.execute('''
    UPDATE users 
    SET password_hash = ? 
    WHERE username = ?
    ''', (new_password_hash, username))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Password reset successfully!")
    root.destroy()

# Initialize database
init_database()

# Create main window
root = tk.Tk()
root.title("ActivArc")

# Set window size and center it
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = ttk.Label(main_frame, text="Forgot Password?", font=('Helvetica', 14, 'bold'))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username field
ttk.Label(main_frame, text="Username").grid(row=1, column=0, sticky='w', pady=(0, 5))
username_entry = ttk.Entry(main_frame, width=42)
username_entry.grid(row=2, column=0, columnspan=2, pady=(0, 15))

# Security Questions (will be populated based on username)
ttk.Label(main_frame, text="Security Question").grid(row=3, column=0, sticky='w', pady=(0, 5))
security_question = ttk.Entry(main_frame, width=42, state='readonly')
security_question.grid(row=4, column=0, columnspan=2, pady=(0, 15))

# Security Answer
ttk.Label(main_frame, text="Security Answer").grid(row=5, column=0, sticky='w', pady=(0, 5))
security_answer = ttk.Entry(main_frame, width=42)
security_answer.grid(row=6, column=0, columnspan=2, pady=(0, 15))

# New Password
ttk.Label(main_frame, text="New Password").grid(row=7, column=0, sticky='w', pady=(0, 5))
new_password = ttk.Entry(main_frame, width=42, show="*")
new_password.grid(row=8, column=0, columnspan=2, pady=(0, 15))

# Confirm Password
ttk.Label(main_frame, text="Confirm Password").grid(row=9, column=0, sticky='w', pady=(0, 5))
confirm_password = ttk.Entry(main_frame, width=42, show="*")
confirm_password.grid(row=10, column=0, columnspan=2, pady=(0, 15))

# Function to toggle password visibility
def toggle_password_visibility():
    if show_password_var.get():
        new_password.config(show="")
        confirm_password.config(show="")
    else:
        new_password.config(show="*")
        confirm_password.config(show="*")

# Show Password Checkbox
show_password_var = tk.BooleanVar()
show_password_check = ttk.Checkbutton(main_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_check.grid(row=10, column=2, padx=(10, 0))

# Reset Button
reset_button = ttk.Button(main_frame, text="Reset", command=reset_password)
reset_button.grid(row=11, column=0, columnspan=2, pady=(10, 0))

# Company Logo
logo_label = ttk.Label(root, text="ActivArc", font=('Helvetica', 16, 'bold'))
logo_label.place(x=20, y=20)

# Function to update security question when username is entered
def on_username_change(event):
    username = username_entry.get()
    if username:
        conn = sqlite3.connect('ActivArcDatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT security_question FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            security_question.configure(state='normal')
            security_question.delete(0, tk.END)
            security_question.insert(0, result[0])
            security_question.configure(state='readonly')
        else:
            security_question.configure(state='normal')
            security_question.delete(0, tk.END)
            security_question.insert(0, "User not found")
            security_question.configure(state='readonly')

username_entry.bind('<KeyRelease>', on_username_change)

# Start the application
root.mainloop()