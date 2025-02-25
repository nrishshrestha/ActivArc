import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Define colors
bk = "#282828"  # Dark background
oran = "#FF9500"  # Orange accent

# Food database
food_db = {
    "Apple": 52, "Banana": 89, "Chicken Breast": 165,
    "Rice (cooked)": 130, "Egg": 155, "Bread": 265,
    "Milk": 42, "Potato": 77, "Pasta (cooked)": 158,
    "Salmon": 208, "Yogurt": 59, "Cheese": 402,
    "Peanut Butter": 588, "Oatmeal": 307, "Orange": 47
}

# Global variables
history = None
total_var = None
food_var = None
weight_var = None
calories_var = None
conn = None
cursor = None

def apply_style():
    # Create custom style for ttk widgets
    style = ttk.Style()
    style.theme_use('clam')  # Use clam theme as base
    
    # Configure colors for various widget elements
    style.configure('TFrame', background=bk)
    style.configure('TLabel', background=bk, foreground=oran, font=('Arial', 12))
    style.configure('TLabelframe', background=bk, foreground=oran, font=('Arial', 14))
    style.configure('TLabelframe.Label', background=bk, foreground=oran, font=('Arial', 14))
    style.configure('TButton', background=oran, foreground=bk, font=('Arial', 12), relief='solid')
    style.map('TButton',
             background=[('active', oran)],
             foreground=[('active', bk)])
    
    # Configure Treeview
    style.configure('Treeview', 
                   background=bk, 
                   foreground=oran, 
                   fieldbackground=bk,
                   font=('Arial', 11))
    style.configure('Treeview.Heading', 
                   background=oran, 
                   foreground=bk,
                   font=('Arial', 12, 'bold'))
    
    # Configure Combobox and Entry
    style.configure('TCombobox', 
                   fieldbackground=bk, 
                   background=bk,
                   foreground=oran,
                   selectbackground=oran,
                   selectforeground=bk)
    style.configure('TEntry', 
                   fieldbackground=bk, 
                   foreground=oran,
                   insertcolor=oran)

def init_database():
    global conn, cursor
    conn = sqlite3.connect('ActivArcDatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food TEXT NOT NULL,
        weight REAL NOT NULL,
        calories REAL NOT NULL
    )
    ''')
    conn.commit()

def add_food():
    food = food_var.get()
    try:
        weight = float(weight_var.get() or 0)
        calories = float(calories_var.get() or 0) or (food_db.get(food, 0) * weight / 100)
        
        if food and calories > 0:
            history.insert("", 0, values=(food, f"{weight}g", f"{calories:.1f} kcal"))
            update_total()
            
            # Clear inputs
            weight_var.set("")
            calories_var.set("")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and calories.")

def update_total():
    total = sum(float(history.item(item)["values"][2].split()[0]) 
               for item in history.get_children())
    total_var.set(f"Total: {total:.1f} kcal")

def clear_all():
    for item in history.get_children():
        history.delete(item)
    total_var.set("Total: 0 kcal")

def save_history():
    for item in history.get_children():
        food, weight, calories = history.item(item)["values"]
        weight = float(weight.replace("g", ""))
        calories = float(calories.replace(" kcal", ""))
        cursor.execute('''
        INSERT INTO food_history (food, weight, calories)
        VALUES (?, ?, ?)
        ''', (food, weight, calories))
    conn.commit()
    messagebox.showinfo("Success", "Food history saved successfully!")

def on_closing():
    if conn:
        conn.close()
    root.destroy()

def setup_ui(root):
    global history, total_var, food_var, weight_var, calories_var
    
    # Configure root with new colors
    root.title("Simple Calorie Calculator")
    root.geometry("800x600")
    root.configure(bg=bk)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Apply ttk style
    apply_style()
    
    # Main frames
    input_frame = ttk.LabelFrame(root, text="Add Food")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Input fields frame with labels
    fields_frame = ttk.Frame(input_frame)
    fields_frame.pack(fill="x", padx=5, pady=5)
    
    # Food selection with label
    food_frame = ttk.Frame(fields_frame)
    food_frame.pack(side="left", padx=5)
    ttk.Label(food_frame, text="Food Item").pack()
    food_var = tk.StringVar()
    food_combo = ttk.Combobox(food_frame, textvariable=food_var, 
                 values=sorted(food_db.keys()))
    food_combo.pack()
    
    # Weight input with label
    weight_frame = ttk.Frame(fields_frame)
    weight_frame.pack(side="left", padx=5)
    ttk.Label(weight_frame, text="Weight (g)").pack()
    weight_var = tk.StringVar()
    ttk.Entry(weight_frame, textvariable=weight_var, 
              width=10).pack()
    
    # Calories input with label
    calories_frame = ttk.Frame(fields_frame)
    calories_frame.pack(side="left", padx=5)
    ttk.Label(calories_frame, text="Calories").pack()
    calories_var = tk.StringVar()
    ttk.Entry(calories_frame, textvariable=calories_var, 
              width=10).pack()
    
    # Add button
    ttk.Button(fields_frame, text="Add", 
               command=add_food).pack(side="left", padx=5, pady=20)
    
    # History section
    history_frame = ttk.LabelFrame(root, text="Food History")
    history_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # History table
    columns = ("Food", "Weight", "Calories")
    history = ttk.Treeview(history_frame, columns=columns, show="headings")
    for col in columns:
        history.heading(col, text=col)
        history.column(col, width=100)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", 
                             command=history.yview)
    history.configure(yscrollcommand=scrollbar.set)
    
    history.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Total calories
    total_var = tk.StringVar(value="Total: 0 kcal")
    total_label = ttk.Label(root, textvariable=total_var)
    total_label.pack(pady=5)
    
    # Button frame
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=5)
    
    # Clear button
    clear_button = ttk.Button(button_frame, text="Clear All", 
               command=clear_all)
    clear_button.pack(side="left", padx=5)
    
    # Save button
    save_button = ttk.Button(button_frame, text="Save", 
               command=save_history)
    save_button.pack(side="left", padx=5)
    
    # Initialize database
    init_database()

def main():
    global root
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()