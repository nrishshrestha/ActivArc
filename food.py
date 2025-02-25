import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class CalorieCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calorie Calculator")
        self.root.geometry("800x600")
        
        # Food database
        self.food_db = {
            "Apple": 52, "Banana": 89, "Chicken Breast": 165,
            "Rice (cooked)": 130, "Egg": 155, "Bread": 265,
            "Milk": 42, "Potato": 77, "Pasta (cooked)": 158,
            "Salmon": 208, "Yogurt": 59, "Cheese": 402,
            "Peanut Butter": 588, "Oatmeal": 307, "Orange": 47
        }
        
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
        self.food_var = tk.StringVar()
        ttk.Combobox(food_frame, textvariable=self.food_var, 
                     values=sorted(self.food_db.keys())).pack()
        
        # Weight input with label
        weight_frame = ttk.Frame(fields_frame)
        weight_frame.pack(side="left", padx=5)
        ttk.Label(weight_frame, text="Weight (g)").pack()
        self.weight_var = tk.StringVar()
        ttk.Entry(weight_frame, textvariable=self.weight_var, 
                  width=10).pack()
        
        # Calories input with label
        calories_frame = ttk.Frame(fields_frame)
        calories_frame.pack(side="left", padx=5)
        ttk.Label(calories_frame, text="Calories").pack()
        self.calories_var = tk.StringVar()
        ttk.Entry(calories_frame, textvariable=self.calories_var, 
                  width=10).pack()
        
        # Add button
        ttk.Button(fields_frame, text="Add", 
                   command=self.add_food).pack(side="left", padx=5, pady=20)
        
        # History section
        history_frame = ttk.LabelFrame(root, text="Food History")
        history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # History table
        columns = ("Food", "Weight", "Calories")
        self.history = ttk.Treeview(history_frame, columns=columns, show="headings")
        for col in columns:
            self.history.heading(col, text=col)
            self.history.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", 
                                 command=self.history.yview)
        self.history.configure(yscrollcommand=scrollbar.set)
        
        self.history.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Total calories
        self.total_var = tk.StringVar(value="Total: 0 kcal")
        ttk.Label(root, textvariable=self.total_var).pack(pady=5)
        
        # Clear button
        ttk.Button(root, text="Clear All", 
                   command=self.clear_all).pack(pady=5)
        
        # Save button
        ttk.Button(root, text="Save", 
                   command=self.save_history).pack(pady=5)
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        self.conn = sqlite3.connect('ActivArcDatabase.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food TEXT NOT NULL,
            weight REAL NOT NULL,
            calories REAL NOT NULL
        )
        ''')
        self.conn.commit()
    def add_food(self):
        food = self.food_var.get()
        try:
            weight = float(self.weight_var.get() or 0)
            calories = float(self.calories_var.get() or 0) or (self.food_db.get(food, 0) * weight / 100)
            
            if food and calories > 0:
                self.history.insert("", 0, values=(food, f"{weight}g", f"{calories:.1f} kcal"))
                self.update_total()
                
                # Clear inputs
                self.weight_var.set("")
                self.calories_var.set("")
        except ValueError:
            pass
    
    def update_total(self):
        total = sum(float(self.history.item(item)["values"][2].split()[0]) 
                   for item in self.history.get_children())
        self.total_var.set(f"Total: {total:.1f} kcal")
    
    def clear_all(self):
        for item in self.history.get_children():
            self.history.delete(item)
        self.total_var.set("Total: 0 kcal")
    def save_history(self):
        for item in self.history.get_children():
            food, weight, calories = self.history.item(item)["values"]
            weight = float(weight.replace("g", ""))
            calories = float(calories.replace(" kcal", ""))
            self.cursor.execute('''
            INSERT INTO food_history (food, weight, calories)
            VALUES (?, ?, ?)
            ''', (food, weight, calories))
        self.conn.commit()
        messagebox.showinfo("Success", "Food history saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieCalculator(root)
    root.mainloop()