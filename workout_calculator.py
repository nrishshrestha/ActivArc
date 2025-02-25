import tkinter as tk
from tkinter import messagebox
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    workout TEXT NOT NULL,
                    sets INTEGER NOT NULL,
                    reps INTEGER NOT NULL,
                    calories_burned REAL NOT NULL,
                    datetime TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
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