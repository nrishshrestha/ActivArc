import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class FoodEntry:
    food: str
    weight: float
    calories: float

class AddFoodDialog:
    def __init__(self, parent, food_database):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Food")
        self.dialog.geometry("300x200")
        self.dialog.grab_set()  # Make dialog modal
        
        self.food_database = food_database
        self.result = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Food name entry
        ttk.Label(self.dialog, text="Food Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.dialog, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Calories per 100g entry
        ttk.Label(self.dialog, text="Calories (per 100g):").grid(row=1, column=0, padx=5, pady=5)
        self.calories_var = tk.StringVar()
        vcmd = (self.dialog.register(self._validate_number), '%P')
        self.calories_entry = ttk.Entry(
            self.dialog,
            textvariable=self.calories_var,
            validate='key',
            validatecommand=vcmd
        )
        self.calories_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add", command=self._on_add).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).grid(row=0, column=1, padx=5)
        
    def _validate_number(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def _on_add(self):
        name = self.name_var.get().strip()
        try:
            calories = float(self.calories_var.get())
            
            if not name:
                messagebox.showerror("Error", "Please enter a food name.")
                return
                
            if calories <= 0:
                messagebox.showerror("Error", "Calories must be greater than 0.")
                return
                
            if name in self.food_database:
                if not messagebox.askyesno("Warning", 
                    f"{name} already exists. Do you want to update its calories?"):
                    return
                    
            self.result = (name, calories)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid calories value.")
            
    def _on_cancel(self):
        self.dialog.destroy()

class FoodEntryWidget(ttk.Frame):
    def __init__(self, parent: ttk.Frame, food_database: Dict[str, float], **kwargs):
        super().__init__(parent, **kwargs)
        self.food_database = food_database
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        # Food selection
        self.food_var = tk.StringVar()
        food_list = sorted(list(self.food_database.keys()) + ["Add new food..."])
        self.food_combobox = ttk.Combobox(
            self, 
            textvariable=self.food_var,
            width=20,
            values=food_list
        )
        self.food_combobox.grid(row=0, column=0, padx=5)
        
        # Weight entry
        self.weight_var = tk.StringVar()
        vcmd = (self.register(self._validate_number), '%P')
        self.weight_entry = ttk.Entry(
            self,
            textvariable=self.weight_var,
            width=10,
            validate='key',
            validatecommand=vcmd
        )
        self.weight_entry.grid(row=0, column=1, padx=5)
        
        # Calories Frame to hold both input and display
        calories_frame = ttk.Frame(self)
        calories_frame.grid(row=0, column=2, padx=5)
        
        # Calories input
        self.calories_input_var = tk.StringVar()
        self.calories_input = ttk.Entry(
            calories_frame,
            textvariable=self.calories_input_var,
            width=10,
            validate='key',
            validatecommand=vcmd
        )
        self.calories_input.grid(row=0, column=0, padx=(0, 5))
        
        # Calories display label
        self.calories_display_var = tk.StringVar(value="kcal")
        self.calories_display = ttk.Label(
            calories_frame,
            textvariable=self.calories_display_var,
            width=5
        )
        self.calories_display.grid(row=0, column=1)
        
        # Remove button
        self.remove_button = ttk.Button(
            self,
            text="✕",
            width=3,
            style="Remove.TButton"
        )
        self.remove_button.grid(row=0, column=3, padx=5)
    
    def _setup_bindings(self):
        self.food_combobox.bind('<<ComboboxSelected>>', self._on_food_selected)
        self.weight_var.trace('w', self._update_calories)
        self.calories_input_var.trace('w', self._handle_manual_input)
    
    def _validate_number(self, value: str) -> bool:
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _on_food_selected(self, event):
        if self.food_var.get() == "Add new food...":
            dialog = AddFoodDialog(self, self.food_database)
            self.wait_window(dialog.dialog)
            
            if dialog.result:
                name, calories = dialog.result
                self.food_database[name] = calories
                self.refresh_food_list()
                self.food_var.set(name)
        
        self._update_calories()
    
    def _update_calories(self, *args):
        try:
            food = self.food_var.get()
            weight = float(self.weight_var.get() or 0)
            
            if food in self.food_database:
                calories = (self.food_database[food] * weight) / 100
                self.calories_input_var.trace_vdelete("w", self.calories_input_var.trace_info()[0][1])
                self.calories_input_var.set(f"{calories:.1f}")
                self.calories_display_var.set("kcal")
                self.calories_input_var.trace('w', self._handle_manual_input)
        except ValueError:
            pass
    
    def _handle_manual_input(self, *args):
        try:
            calories = float(self.calories_input_var.get() or 0)
            self.calories_display_var.set("kcal")
            
            weight = float(self.weight_var.get() or 0)
            food = self.food_var.get()
            
            if weight > 0 and food and food != "Add new food...":
                calories_per_100g = (calories * 100) / weight
                self.food_database[food] = calories_per_100g
        except ValueError:
            pass
    
    def refresh_food_list(self):
        food_list = sorted(list(self.food_database.keys()) + ["Add new food..."])
        self.food_combobox['values'] = food_list
    
    def get_values(self) -> Optional[FoodEntry]:
        try:
            food = self.food_var.get()
            weight = float(self.weight_var.get() or 0)
            calories = float(self.calories_input_var.get() or 0)
            
            if food and food != "Add new food..." and calories > 0:
                return FoodEntry(food=food, weight=weight, calories=calories)
        except ValueError:
            pass
        return None
    
    def clear(self):
        self.food_var.set("")
        self.weight_var.set("")
        self.calories_input_var.set("")
        self.calories_display_var.set("kcal")

class CalorieCalculator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Food Calorie Calculator")
        self.root.geometry("700x800")
        
        # Dictionary to store food items and their calories (per 100g)
        self.food_database = {
            "Apple": 52, "Banana": 89, "Chicken Breast": 165,
            "Rice (cooked)": 130, "Egg": 155, "Bread": 265,
            "Milk": 42, "Potato": 77, "Pasta (cooked)": 158,
            "Salmon": 208, "Yogurt": 59, "Cheese": 402,
            "Peanut Butter": 588, "Oatmeal": 307, "Orange": 47
        }
        
        self._setup_styles()
        self._create_gui()
        self._configure_grid()
        
    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Remove.TButton", foreground="red")
        
    def _create_gui(self):
        # Main container
        self.container = ttk.Frame(self.root, padding="10")
        self.container.grid(row=0, column=0, sticky="nsew")
        
        # Main box
        self.main_box = ttk.LabelFrame(
            self.container,
            text="Food Calorie Calculator",
            padding="10"
        )
        self.main_box.grid(row=0, column=0, sticky="nsew")
        
        self._create_header()
        self._create_entries_frame()
        self._create_buttons()
        self._create_summary_frame()
        self._create_food_list()
        
    def _configure_grid(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.main_box.columnconfigure(0, weight=1)
        
    def _create_header(self):
        header_frame = ttk.Frame(self.main_box)
        header_frame.grid(row=0, column=0, pady=5, sticky="ew")
        
        headers = [
            ("Food Item", 25),
            ("Weight (g)", 15),
            ("Calories", 20),
            ("", 5)  # For remove button
        ]
        for col, (text, width) in enumerate(headers):
            ttk.Label(header_frame, text=text, width=width).grid(row=0, column=col)
            
    def _create_entries_frame(self):
        self.entries_frame = ttk.Frame(self.main_box)
        self.entries_frame.grid(row=1, column=0, sticky="ew")
        self.food_entries = []
        self.add_food_entry()
        
    def _create_buttons(self):
        button_frame = ttk.Frame(self.main_box)
        button_frame.grid(row=2, column=0, pady=10)
        
        buttons = [
            ("Add Another Food", self.add_food_entry),
            ("Calculate Total", self.calculate_total),
            ("Clear All", self.clear_all)
        ]
        
        for col, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(
                row=0, column=col, padx=5
            )
            
    def _create_summary_frame(self):
        total_frame = ttk.LabelFrame(self.main_box, text="Meal Summary", padding="10")
        total_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        ttk.Label(total_frame, text="Total Calories:").grid(row=0, column=0, sticky="w")
        self.total_calories = 0
        self.total_calories_var = tk.StringVar(value="0 kcal")
        ttk.Label(total_frame, textvariable=self.total_calories_var).grid(
            row=0, column=1, sticky="w"
        )
        
    def _create_food_list(self):
        list_frame = ttk.LabelFrame(self.main_box, text="Added Foods", padding="10")
        list_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        self.food_list = tk.Text(list_frame, height=10, width=50)
        self.food_list.grid(row=0, column=0, sticky="ew")
        
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.food_list.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.food_list.configure(yscrollcommand=scrollbar.set)
        
    def add_food_entry(self):
        entry = FoodEntryWidget(self.entries_frame, self.food_database)
        entry.grid(row=len(self.food_entries), column=0, pady=2)
        entry.remove_button.configure(
            command=lambda e=entry: self.remove_food_entry(e)
        )
        self.food_entries.append(entry)
        
    def remove_food_entry(self, entry: FoodEntryWidget):
        if len(self.food_entries) > 1:
            entry.grid_remove()
            self.food_entries.remove(entry)
            for i, e in enumerate(self.food_entries):
                e.grid(row=i, column=0, pady=2)
        
    def calculate_total(self):
        total_calories = 0
        self.food_list.delete(1.0, tk.END)
        
        for entry in self.food_entries:
            values = entry.get_values()
            if values:
                total_calories += values.calories
                self.food_list.insert(
                    tk.END,
                    f"{values.food}: {values.weight}g - {values.calories:.1f} kcal\n"
                )
        
        self.total_calories = total_calories
        self.total_calories_var.set(f"{total_calories:.1f} kcal")
        
    def clear_all(self):
        for entry in self.food_entries:
            entry.clear()
        self.total_calories = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieCalculator(root)
    root.mainloop()