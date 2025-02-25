import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import subprocess
import datetime
import sqlite3

# Define the calories burned per rep for each workout type
CALORIES_PER_REP = { 
    "Push-ups": 0.5,
    "Sit-ups": 0.3,
    "Squats": 0.6,
    "Pull-ups": 1.0,
    "Lunges": 0.4,
    "Burpees": 1.2,
}

# Global variables
workout_entries = []
calculate_button = None
result_label = None
workout_frame = None
bk = "#282828"  # Dark background
oran = "#FF9500"  # Orange accent

def load_session():
    try:
        with open("session.txt", "r") as file:
            content = file.read().strip()
            if content:  # Check if content is not empty
                return int(content)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading session: {e}")
    return None  # Return None if any error occurs or file is empty

def add_workout():
    # Add a new row of workout entry fields
    row = len(workout_entries) + 1
    workout_var = tk.StringVar(value="Select Workout")
    
    workout_menu = tk.OptionMenu(workout_frame, workout_var, *list(CALORIES_PER_REP.keys()))
    workout_menu.config(bg=bk, fg=oran, activebackground=oran, activeforeground=bk, font=('Arial', 12))
    workout_menu["menu"].config(bg=bk, fg=oran, activebackground=oran, activeforeground=bk, font=('Arial', 12))
    workout_menu.grid(row=row, column=0, padx=10, pady=5)

    sets_entry = tk.Entry(workout_frame, width=10, font=('Arial', 12), bg=bk, fg=oran, insertbackground=oran, bd=2)
    sets_entry.grid(row=row, column=1, padx=10, pady=5)

    reps_entry = tk.Entry(workout_frame, width=10, font=('Arial', 12), bg=bk, fg=oran, insertbackground=oran, bd=2)
    reps_entry.grid(row=row, column=2, padx=10, pady=5)

    workout_entries.append((workout_var, sets_entry, reps_entry))
    calculate_button.config(state=tk.NORMAL)

def calculate_calories():
    total_calories = 0
    for workout_var, sets_entry, reps_entry in workout_entries:
        try:
            workout = workout_var.get()
            sets = int(sets_entry.get())
            reps = int(reps_entry.get())
            total_calories += CALORIES_PER_REP.get(workout, 0) * sets * reps
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for sets and reps.")
            return
    result_label.config(text=f"Total Calories Burned: {total_calories:.1f} kcal")

def save_workout():
    user_id = load_session()
    if user_id is None:
        messagebox.showerror("Error", "No user session found. Please log in again.")
        return

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workout_data = []

    for workout_var, sets_entry, reps_entry in workout_entries:
        workout = workout_var.get()
        sets = sets_entry.get()
        reps = reps_entry.get()
        if workout != "Select Workout" and sets and reps:
            try:
                sets = int(sets)
                reps = int(reps)
                calories_burned = CALORIES_PER_REP.get(workout, 0) * sets * reps
                workout_data.append((user_id, workout, sets, reps, calories_burned, current_datetime))
            except ValueError:
                continue

    if workout_data:
        try:
            conn = sqlite3.connect("activarc.db")
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO workouts (user_id, workout, sets, reps, calories_burned, datetime)
                VALUES (?, ?, ?, ?, ?, ?)
            """, workout_data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Workout Saved", "Your workout has been saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showerror("Error", "No valid workout data to save.")

def clear_all():
    for widgets in workout_frame.winfo_children()[3:]:
        widgets.destroy()
    workout_entries.clear()
    result_label.config(text="Total Calories Burned: 0 kcal")
    calculate_button.config(state=tk.DISABLED)

def show_success_page():
    success_root = tk.Tk()
    success_root.title("Password Reset Successful")
    
    ttk.Label(success_root, text="Your password is reset. Please go to login page.").pack(pady=20)
    ttk.Button(success_root, text="Go to Login Page", command=lambda: show_login(success_root)).pack(pady=10)
    
    success_root.mainloop()

def show_login(success_root):
    success_root.destroy()
    subprocess.run(["python", "log_sign_combi.py"])

def reset_password():
    username = username_entry.get()
    current_pwd = current_password.get()
    new_pwd = new_password.get()
    confirm_pwd = confirm_password.get()
    
    if not all([username, current_pwd, new_pwd, confirm_pwd]):
        messagebox.showerror("Error", "All fields are required")
        return
        
    if new_pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Verify current password
    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == current_pwd:
        # Update password
        conn = sqlite3.connect("activarc.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_pwd, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password reset successfully!")
        root.destroy()
        show_success_page()
    else:
        messagebox.showerror("Error", "Current password is incorrect")

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

# Current Password
ttk.Label(main_frame, text="Current Password").grid(row=3, column=0, sticky='w', pady=(0, 5))
current_password = ttk.Entry(main_frame, width=42, show="*")
current_password.grid(row=4, column=0, columnspan=2, pady=(0, 15))

# New Password
ttk.Label(main_frame, text="New Password").grid(row=5, column=0, sticky='w', pady=(0, 5))
new_password = ttk.Entry(main_frame, width=42, show="*")
new_password.grid(row=6, column=0, columnspan=2, pady=(0, 15))

# Confirm Password
ttk.Label(main_frame, text="Confirm Password").grid(row=7, column=0, sticky='w', pady=(0, 5))
confirm_password = ttk.Entry(main_frame, width=42, show="*")
confirm_password.grid(row=8, column=0, columnspan=2, pady=(0, 15))

# Function to toggle password visibility
def toggle_password_visibility():
    if show_password_var.get():
        current_password.config(show="")
        new_password.config(show="")
        confirm_password.config(show="")
    else:
        current_password.config(show="*")
        new_password.config(show="*")
        confirm_password.config(show="*")

# Show Password Checkbox
show_password_var = tk.BooleanVar()
show_password_check = ttk.Checkbutton(main_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_check.grid(row=8, column=2, padx=(10, 0))

# Reset Button
reset_button = ttk.Button(main_frame, text="Reset", command=reset_password)
reset_button.grid(row=9, column=0, columnspan=2, pady=(10, 0))

# Company Logo
logo_label = ttk.Label(root, text="ActivArc", font=('Helvetica', 16, 'bold'))
logo_label.place(x=20, y=20)

# Start the application
root.mainloop()

# Initialize the main tkinter window
root = tk.Tk()
root.title("Workout Calorie Calculator")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg=bk)

# Create the main title label
tk.Label(root, text="Workout Calorie Calculator", font=('Arial', 20, 'bold'), bg=bk, fg=oran).pack(pady=20)

# Main frame
main_frame = tk.Frame(root, bg=bk)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Workout details frame
workout_frame = tk.LabelFrame(main_frame, text="Workout Details", font=('Arial', 14), bg=bk, fg=oran)
workout_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Headers
headers = ["Workout", "Sets", "Reps"]
for i, header in enumerate(headers):
    tk.Label(workout_frame, text=header, font=('Arial', 14, 'bold'), bg=bk, fg=oran).grid(row=0, column=i, padx=10, pady=5)

# Button frame
button_frame = tk.Frame(main_frame, bg=bk)
button_frame.pack(fill=tk.X, pady=10)

# Action buttons
tk.Button(button_frame, text="Add Workout", command=add_workout, font=('Arial', 12), 
         relief='solid', bg=oran, fg=bk, activebackground=oran).pack(side=tk.LEFT, padx=5)

calculate_button = tk.Button(button_frame, text="Calculate", command=calculate_calories, font=('Arial', 12),
                            relief='solid', bg=oran, fg=bk, activebackground=oran, state=tk.DISABLED)
calculate_button.pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Clear All", command=clear_all, font=('Arial', 12),
         relief='solid', bg=oran, fg=bk, activebackground=oran).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Save Workout", command=save_workout, font=('Arial', 12),
         relief='solid', bg=oran, fg=bk, activebackground=oran).pack(side=tk.LEFT, padx=5)

# Results frame
result_frame = tk.LabelFrame(main_frame, text="Results", font=('Arial', 14), bg=bk, fg=oran)
result_frame.pack(fill=tk.X, padx=10, pady=5)

# Results label
result_label = tk.Label(result_frame, text="Total Calories Burned: 0 kcal", font=('Arial', 14), bg=bk, fg=oran)
result_label.pack(pady=10)

# Start the application
root.mainloop()