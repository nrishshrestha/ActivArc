import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Tuple, Dict
import datetime

class WorkoutCalculator:
    # Define the calories burned per rep for each workout type
    CALORIES_PER_REP: Dict[str, float] = { 
        "Push-ups": 0.5,
        "Sit-ups": 0.3,
        "Squats": 0.6,
        "Pull-ups": 1.0,
        "Lunges": 0.4,
        "Burpees": 1.2,
    }

    def __init__(self):
        # Initialize the main tkinter window (app) and set the title and size
        self.root = tk.Tk()
        self.root.title("Workout Calorie Calculator")
        self.root.geometry("600x500")

        # List to hold the workout details (workout type, sets, reps)
        self.workout_entries: List[Tuple[tk.StringVar, tk.Entry, tk.Entry]] = []

        # Call setup functions to style widgets and create UI elements
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        # Configure styles for various UI elements
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Result.TLabel", font=("Helvetica", 14))

    def _create_widgets(self):
        # Create the main title label
        ttk.Label(self.root, text="Workout Calorie Calculator", style="Title.TLabel").pack(pady=20)

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Workout details frame
        self.workout_frame = ttk.LabelFrame(self.main_frame, text="Workout Details")
        self.workout_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Headers
        headers = ["Workout", "Sets", "Reps"]
        for i, header in enumerate(headers):
            ttk.Label(self.workout_frame, text=header, style="Header.TLabel").grid(row=0, column=i, padx=10, pady=5)

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Action buttons
        ttk.Button(button_frame, text="Add Workout", command=self.add_workout).pack(side=tk.LEFT, padx=5)
        self.calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate_calories, state=tk.DISABLED)
        self.calculate_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Workout", command=self.save_workout).pack(side=tk.LEFT, padx=5)

        # Results frame
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Results")
        self.result_frame.pack(fill=tk.X, padx=10, pady=5)

        # Results label
        self.result_label = ttk.Label(self.result_frame, text="Total Calories Burned: 0 kcal", style="Result.TLabel")
        self.result_label.pack(pady=10)

    def add_workout(self):
        # Add a new row of workout entry fields
        row = len(self.workout_entries) + 1
        workout_var = tk.StringVar(value="Select Workout")
        workout_combo = ttk.Combobox(
            self.workout_frame, textvariable=workout_var, values=list(self.CALORIES_PER_REP.keys()), state="readonly"
        )
        workout_combo.grid(row=row, column=0, padx=10, pady=5)

        sets_entry = ttk.Entry(self.workout_frame, width=10)
        sets_entry.grid(row=row, column=1, padx=10, pady=5)

        reps_entry = ttk.Entry(self.workout_frame, width=10)
        reps_entry.grid(row=row, column=2, padx=10, pady=5)

        self.workout_entries.append((workout_var, sets_entry, reps_entry))
        self.calculate_button.config(state=tk.NORMAL)

    def calculate_calories(self):
        total_calories = 0
        for workout_var, sets_entry, reps_entry in self.workout_entries:
            try:
                workout = workout_var.get()
                sets = int(sets_entry.get())
                reps = int(reps_entry.get())
                total_calories += self.CALORIES_PER_REP.get(workout, 0) * sets * reps
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for sets and reps.")
                return
        self.result_label.config(text=f"Total Calories Burned: {total_calories:.1f} kcal")

    def save_workout(self):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("workout_log.txt", "a") as file:
            file.write(f"Workout Log - {current_datetime}\n")
            for workout_var, sets_entry, reps_entry in self.workout_entries:
                workout = workout_var.get()
                sets = sets_entry.get()
                reps = reps_entry.get()
                if workout != "Select Workout" and sets and reps:
                    try:
                        sets = int(sets)
                        reps = int(reps)
                        calories_burned = self.CALORIES_PER_REP.get(workout, 0) * sets * reps
                        file.write(f"{workout}: {sets} sets x {reps} reps - {calories_burned:.1f} kcal\n")
                    except ValueError:
                        continue
            file.write("\n")
        
        messagebox.showinfo("Workout Saved", "Your workout has been saved successfully!")

    def clear_all(self):
        for widgets in self.workout_frame.winfo_children()[3:]:
            widgets.destroy()
        self.workout_entries.clear()
        self.result_label.config(text="Total Calories Burned: 0 kcal")
        self.calculate_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WorkoutCalculator()
    app.run()