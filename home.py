from tkinter import messagebox, ttk
from typing import List, Tuple, Dict
import datetime
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

home_page=tk.Tk()
home_page.title("ActivArc")
home_page.configure(bg="#212121")

def food():
    class CalorieCalculator:
        def __init__(self, root):
            self.root = root
            self.root.title("Simple Calorie Calculator")
            self.root.geometry("600x400")
            
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

    if __name__ == "__main__":
        root = tk.Tk()
        app = CalorieCalculator(root)
        root.mainloop()

def work():
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

def bmi():
    root=Tk()
    root.geometry("1000x600")
    root.title("BMI Calculator")
    root.resizable(False, False)
    bk = "#282828"
    root.configure(bg=bk)

    oran = "#FF9500"

    def calculate():
        try:
            h = float(height.get()) / 100
            w = float(weight.get())
            category = ""

            if h <= 0 or w <= 0:
                result.config(text="Error: Height and Weight \nmust be positive numbers.", fg="red")
                return

            bmi = w / (h ** 2)

            if bmi < 18.5:
                category = "Underweight"
                message = 'You are underweight.\nYou need to gain weight.'
            elif 18.5 <= bmi < 24.9:
                category = "Normal"
                message = 'You are healthy.\nKeep it up!'
            elif 25 <= bmi < 29.9:
                category = "Overweight"
                message = 'You are overweight.\nYou need to lose weight.'
            else:
                category = "Obese"
                message = 'You are obese.\nYou need to lose weight.'

            result.config(text=f"Your BMI: {bmi:.2f}\n\nCategory: {category} \n\n{message}", font=('Arial', 18), fg=oran)

        except ValueError:
            result.config(text="Error: Please enter valid values.", fg="red")

    def clear():
        age.delete(0, END)
        height.delete(0, END)
        weight.delete(0, END)
        gender.set(" ")
        result.config(text="Your BMI: \n\nCategory: ", font=('Arial', 18), fg=oran)

    # Age Input
    Label(root, text="Age", font=('Arial', 20), bg=bk, fg=oran).place(x=70, y=30)
    age = Entry(root, font=('Arial', 18), bg=bk, fg=oran, insertbackground=oran, bd=2)
    age.place(x=150, y=35)

    # Gender Input
    gender = StringVar(value=' ')
    Label(root, text='Gender', font=('Arial', 20), bg=bk, fg=oran).place(x=50, y=90)
    Radiobutton(root, text='Male', variable=gender, value='Male', font=('Arial', 18), bg=bk, fg=oran, selectcolor=bk).place(x=150, y=93.5)
    Radiobutton(root, text='Female', variable=gender, value='Female', font=('Arial', 18), bg=bk, fg=oran, selectcolor=bk).place(x=150, y=130)

    # Height Input
    Label(root, text="Height", font=('Arial', 20), bg=bk, fg=oran).place(x=55, y=180)
    Label(root, text="cm", font=('Arial', 20), bg=bk, fg=oran).place(x=420, y=180)
    height = Entry(root, font=('Arial', 18), bg=bk, fg=oran, insertbackground=oran, bd=2)
    height.place(x=150, y=185)

    # Weight Input
    Label(root, text="Weight", font=('Arial', 20), bg=bk, fg=oran).place(x=50, y=240)
    Label(root, text="kg", font=('Arial', 20), bg=bk, fg=oran).place(x=420, y=240)
    weight = Entry(root, font=('Arial', 18), bg=bk, fg=oran, insertbackground=oran, bd=2)
    weight.place(x=150, y=245)

    # Calculate and Clear Button
    Button(root, text="Calculate", command=calculate, font=('Arial', 18), relief='solid', bg=oran, fg=bk, activebackground=oran).place(x=100, y=300)
    Button(root, text="Clear", command=clear, font=('Arial', 18), relief='solid', bg=oran, fg=bk, activebackground=oran).place(x=280, y=300)

    # Result
    Frame(root, width=400, height=100, bd=1, relief='solid', bg=bk).place(x=500, y=30)
    Frame(root, width=400, height=200, bd=1, relief='solid', bg=bk).place(x=500, y=80)
    Label(root, text="Result", font=('Arial', 20, 'bold'), bg=bk, fg=oran).place(x=510, y=35)
    result = Label(root, text="Your BMI: \n\nCategory: ", font=('Arial', 18), bg=bk, fg=oran)
    result.place(x=510, y=85)

    # Information
    Label(root, text='BMI Information', font=('Arial', 20, 'bold'), bg=bk, fg=oran).place(x=50, y=380)
    bmi_info_text = (
        "Body Mass Index (BMI) is a measurement of a person's weight \n"
        "with respect to their height. It is an indicator rather than \n"
        "a direct measurement of total body fat. BMI helps assess \n"
        "whether an individual is underweight, normal, overweight, \n"
        "or obese based on standardized categories."
    )

    Label(root, text=bmi_info_text, font=('Arial', 16), justify="left", bg=bk, fg=oran).place(x=50, y=420)

    bmi.mainloop()


# Maximize the window manually by getting the screen's dimensions
screen_width = home_page.winfo_screenwidth()
screen_height = home_page.winfo_screenheight()
home_page.geometry(f"{screen_width}x{screen_height}")  # Set window size to screen size

# frame1
frame1=Frame(home_page,bg="#212121",relief=GROOVE,bd=2,padx=20,pady=20) # frame1
frame1_width=400 # width of frame1
frame1_height=screen_height # height of screen
frame1.place(relx=0.0, rely=0.0, width=frame1_width, height=frame1_height)  # Specify width and height in place()

# User
username=Label(frame1,text="Username: ",font=("Times New Roman",15),bg="#212121",fg="#FF9500")
username.pack(pady=10,anchor="w") # needs to be pulled from database

# Full Name
fullname=Label(frame1,text="Full Name: ",font=("Times New Roman",15),bg="#212121",fg="#FF9500")
fullname.pack(pady=10,anchor="w") # needs to be pulled from database

# Weight
weight=Label(frame1,text="Weight: ",font=("Times New Roman",15),bg="#212121",fg="#FF9500")
weight.pack(pady=10,anchor="w") # needs to be pulled from database

# Height
height=Label(frame1,text="Height: ",font=("Times New Roman",15),bg="#212121",fg="#FF9500")
height.pack(pady=10,anchor="w") # needs to be pulled from database

# Age
age=Label(frame1,text="Age: ",font=("Times New Roman",15),bg="#212121",fg="#FF9500")
age.pack(pady=10,anchor="w") # needs to be pulled from database

# BMI Calculator
bmi_button=Button(frame1,text="BMI Calculator",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=bmi)
bmi_button.pack(pady=10,anchor="w")

# Calorie Eaten
calorie_button=Button(frame1,text="Calorie Eaten",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=food)
calorie_button.pack(pady=10,anchor="w")

# Calorie Burned  
workout_button=Button(frame1,text="Calorie Burned",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=work)
workout_button.pack(pady=10,anchor="w")

# About us
about_us=Label(frame1, text=
               "About us: \n"
               "At ActivArc, we're passionate about empowering \n"
               "individuals to achieve their fitness goals.  \n"
               "Born from a shared desire to make fitness tracking \n"
               "more accessible and insightful, ActivArc combines \n"
               "cutting-edge technology with a user-friendly design.\n"
               "We believe that everyone deserves the tools to \n"
               "understand their bodies and unlock their full potential.\n"
               "Our team is dedicated to continuous innovation, constantly \n"
               "striving to improve ActivArc and provide you with the \n"
               "most accurate and motivating fitness companion.",
               font=("Arial", 10),height=15,width=70,justify="center",wraplength=500,bg="#212121",fg="#FF9500")
about_us.pack(side="bottom",pady=50,anchor="w") 

mainloop()