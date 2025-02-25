import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

bk, oran = "#282828", "#FF9500"
food_db = {"Apple": 52, "Banana": 89, "Chicken Breast": 165, "Rice (cooked)": 130, "Egg": 155, "Bread": 265, "Milk": 42, "Potato": 77, "Pasta (cooked)": 158, "Salmon": 208, "Yogurt": 59, "Cheese": 402, "Peanut Butter": 588, "Oatmeal": 307, "Orange": 47}
history = total_var = food_var = weight_var = calories_var = conn = cursor = None

def load_session():
    try:
        with open("session.txt", "r") as file:
            content = file.read().strip()
            if content:
                return int(content)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading session: {e}")
    return None

def apply_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background=bk)
    style.configure('TLabel', background=bk, foreground=oran, font=('Arial', 12))
    style.configure('TLabelframe', background=bk, foreground=oran, font=('Arial', 14))
    style.configure('TLabelframe.Label', background=bk, foreground=oran, font=('Arial', 14))
    style.configure('TButton', background=oran, foreground=bk, font=('Arial', 12), relief='solid')
    style.map('TButton', background=[('active', oran)], foreground=[('active', bk)])
    style.configure('Treeview', background=bk, foreground=oran, fieldbackground=bk, font=('Arial', 11))
    style.configure('Treeview.Heading', background=oran, foreground=bk, font=('Arial', 12, 'bold'))
    style.configure('TCombobox', fieldbackground=bk, background=bk, foreground=oran, selectbackground=oran, selectforeground=bk)
    style.configure('TEntry', fieldbackground=bk, foreground=oran, insertcolor=oran)

# Replace the init_database function
def init_database():
    global conn, cursor
    conn = sqlite3.connect('activarc.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        food TEXT NOT NULL,
        weight REAL NOT NULL,
        calories REAL NOT NULL,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    conn.commit()

def add_food():
    food = food_var.get()
    try:
        weight = float(weight_var.get() or 0)
        calories = float(calories_var.get() or 0) or (food_db.get(food, 0) * weight / 100)
        if food and calories > 0:
            history.insert("", 0, values=(food, f"{weight}g", f"{calories:.1f} kcal"))
            update_total()
            weight_var.set("")
            calories_var.set("")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and calories.")

def update_total():
    total = sum(float(history.item(item)["values"][2].split()[0]) for item in history.get_children())
    total_var.set(f"Total: {total:.1f} kcal")

def clear_all():
    for item in history.get_children(): history.delete(item)
    total_var.set("Total: 0 kcal")

# Replace the save_history function
def save_history():
    user_id = load_session()
    if not user_id:
        messagebox.showerror("Error", "No active session found. Please log in again.")
        return

    try:
        # Save to database
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in history.get_children():
            food, weight, calories = history.item(item)["values"]
            weight = float(weight.replace("g", ""))
            calories = float(calories.replace(" kcal", ""))
            cursor.execute('''
            INSERT INTO food_history (user_id, food, weight, calories, date_added)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, food, weight, calories, current_time))
        conn.commit()
        
        # Save to text file
        with open("food_log.txt", "a") as file:
            file.write("\n=== Food Log ===\n")
            file.write(f"User ID: {user_id}\n")
            file.write(f"Date: {current_time}\n")
            file.write("-" * 50 + "\n")
            
            # Write food items
            total_calories = 0
            for item in history.get_children():
                food, weight, calories = history.item(item)["values"]
                calories_float = float(calories.replace(" kcal", ""))
                total_calories += calories_float
                file.write(f"Food: {food:<20} Weight: {weight:<10} Calories: {calories}\n")
            
            # Write total
            file.write("-" * 50 + "\n")
            file.write(f"Total Calories: {total_calories:.1f} kcal\n\n")
        
        messagebox.showinfo("Success", "Food history saved successfully!")
        clear_all()  # Clear the history after saving
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save food history: {str(e)}")

def on_closing():
    if conn: conn.close()
    root.destroy()

def setup_ui(root):
    global history, total_var, food_var, weight_var, calories_var
    root.title("Simple Calorie Calculator")
    root.geometry("800x600")
    root.configure(bg=bk)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    apply_style()
    
    input_frame = ttk.LabelFrame(root, text="Add Food")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    fields_frame = ttk.Frame(input_frame)
    fields_frame.pack(fill="x", padx=5, pady=5)
    
    food_frame = ttk.Frame(fields_frame)
    food_frame.pack(side="left", padx=5)
    ttk.Label(food_frame, text="Food Item").pack()
    food_var = tk.StringVar()
    ttk.Combobox(food_frame, textvariable=food_var, values=sorted(food_db.keys())).pack()
    
    weight_frame = ttk.Frame(fields_frame)
    weight_frame.pack(side="left", padx=5)
    ttk.Label(weight_frame, text="Weight (g)").pack()
    weight_var = tk.StringVar()
    ttk.Entry(weight_frame, textvariable=weight_var, width=10).pack()
    
    calories_frame = ttk.Frame(fields_frame)
    calories_frame.pack(side="left", padx=5)
    ttk.Label(calories_frame, text="Calories").pack()
    calories_var = tk.StringVar()
    ttk.Entry(calories_frame, textvariable=calories_var, width=10).pack()
    
    ttk.Button(fields_frame, text="Add", command=add_food).pack(side="left", padx=5, pady=20)
    
    history_frame = ttk.LabelFrame(root, text="Food History")
    history_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    history = ttk.Treeview(history_frame, columns=("Food", "Weight", "Calories"), show="headings")
    for col in ("Food", "Weight", "Calories"): history.heading(col, text=col)
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history.yview)
    history.configure(yscrollcommand=scrollbar.set)
    history.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    total_var = tk.StringVar(value="Total: 0 kcal")
    ttk.Label(root, textvariable=total_var).pack(pady=5)
    
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=5)
    ttk.Button(button_frame, text="Clear All", command=clear_all).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Save", command=save_history).pack(side="left", padx=5)
    
    init_database()

def main():
    global root
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()