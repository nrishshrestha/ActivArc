import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
from PIL import Image, ImageTk
<<<<<<< HEAD
import sqlite3
from typing import List, Tuple, Dict
=======
import subprocess
>>>>>>> 3f2d58c45b746cc08c4992972e73dadf6fe7445f

#Global declarations at the top of the file
global root, first_name, last_name, month, day, year, gender, username, password, confirm_password

# Database setup
def database():
    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   birthday TEXT NOT NULL,
                   gender TEXT NOT NULL,
                   username TEXT UNIQUE,
                   password TEXT NOT NULL)""")
    conn.commit()
    conn.close()

database() # Initializes the database

# Function to sign up a new user
def signup(confirm_password_value):  
    fname = first_name.get()
    lname = last_name.get()
    user = username.get()
    passw = password.get()
    birth_date = f"{year.get()} {month.get()} {day.get()}"
    gender_value = gender.get()

    # Validate all fields
    if not all([fname, lname, birth_date, gender_value, user, passw]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    if passw != confirm_password_value:  
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (first_name, last_name, birthday, gender, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                       (fname, lname, birth_date, gender_value, user, passw))
        conn.commit()
        conn.close()
        
        # Show success message
        messagebox.showinfo("Success", "You have signed up successfully!")
        
        # Destroy signup window and show login page
        root.destroy()
        login()
        
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
        conn.close()


# Save the logged-in user ID to a file
def save_session(user_id):
    with open("session.txt", "w") as file:
        file.write(str(user_id))

# Login verification
logged_in_user_id = None

def verify_login():
    global logged_in_user_id
    user = username_entry.get()
    passw = password_entry.get()

    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (user, passw))
    result = cursor.fetchone()
    conn.close()

    if result:
        logged_in_user_id = result[0]
        save_session(logged_in_user_id)

        messagebox.showinfo("Login Successful", "Welcome!")
        page1.destroy()
        from homePage import refresh_home_page 
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


# Login page
def login():
    global page1, username_entry, password_entry

    page1 = tk.Tk()
    page1.title("ActivArc")
    page1.configure(bg="#212121")

    def close_page():
        page1.destroy()

    def open_signup_page():
        page1.destroy()
        subprocess.run(["python", "signUpPage.py"])

    def open_forgot_password_page():
        page1.destroy()
        subprocess.run(["python", "forgotAndResetPassword.py"])

    # Maximize the window manually by getting the screen's dimensions
    screen_width = page1.winfo_screenwidth()
    screen_height = page1.winfo_screenheight()
    page1.geometry(f"{screen_width}x{screen_height}")  # Set window size to screen size

    def password_show_hide():
        check = var.get()
        if check == 1:
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    # Frame for centralization
    main_frame = Frame(page1, bg="lightgray", relief=GROOVE, bd=2, padx=20, pady=20)
    main_frame_width = 400  # Set the width of the frame
    main_frame_height = 400  # Set the height of the frame
    main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the frame relative to the window

    # Username Entrybox and label
    username = Label(main_frame, text="Username", font=("Times New Roman", 15), bg="lightgray")
    username.pack(pady=10, anchor="w")
    username_entry = Entry(main_frame, font=("Times New Roman", 15))
    username_entry.pack(pady=5, fill=X)

    # Password Entrybox and label
    password = Label(main_frame, text="Password", font=("Times New Roman", 15), bg="lightgray")
    password.pack(pady=10, anchor="w")
    password_entry = Entry(main_frame, font=("Times New Roman", 15), show="*")
    password_entry.pack(pady=5, fill=X)

    # Show and Hide password
    var = IntVar()
    c1 = Checkbutton(main_frame, text="Show Password", variable=var, font=("Times New Roman", 10), command=password_show_hide, bg="lightgray")
    c1.pack(pady=10, anchor="w")

    # Login Button
    login_button = Button(main_frame, text="Login", font=("Times New Roman", 15), command=home_page)
    login_button.pack(pady=10)

    # Forgot Password
    fpassword = Button(main_frame, text="Forgot Password", font=("Times New Roman", 15), command=open_forgot_password_page)
    fpassword.pack(pady=10)

    # Don't Have an account?
    noacc = Label(main_frame, text="Don't have an account? | Create one for free!", font=("Times New Roman", 10), fg="blue", bg="lightgray")
    noacc.pack(pady=10)

    # Sign Up Button
    signup = Button(main_frame, text="Sign up", font=("Times New Roman", 15), command=open_signup_page)
    signup.pack(pady=10)

    page1.mainloop()

# Signup page
def signup_page():
    page1.destroy()

    def create_name_fields(frame):
        global first_name,last_name
        ttk.Label(frame, text="First Name").grid(row=0, column=0, sticky=tk.W)
        first_name = ttk.Entry(frame, width=30)
        first_name.grid(row=1, column=0, padx=(0,10), sticky=tk.W)
        
        ttk.Label(frame, text="Last Name").grid(row=0, column=1, sticky=tk.W)
        last_name = ttk.Entry(frame, width=30)
        last_name.grid(row=1, column=1, sticky=tk.W)
        return first_name, last_name

    # Function to create birthday input fields
    def create_birthday_fields(frame):
        global month, day, year
        ttk.Label(frame, text="Birthday").grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        
        birthday_frame = ttk.Frame(frame)
        birthday_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']
        month = ttk.Combobox(birthday_frame, values=months, width=17, state='readonly')
        month.set('Month')
        month.grid(row=0, column=0, padx=(0,5))
        
        days = list(range(1, 32))
        day = ttk.Combobox(birthday_frame, values=days, width=7, state='readonly')
        day.set('Day')
        day.grid(row=0, column=1, padx=5)
        
        years = list(range(1980, 2101))
        year = ttk.Combobox(birthday_frame, values=years, width=12, state='readonly')
        year.set('Year')
        year.grid(row=0, column=2, padx=5)
        return month, day, year

    # Function to create gender fields
    def create_gender_fields(frame):
        global gender
        ttk.Label(frame, text="Gender").grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        
        gender = tk.StringVar()
        gender_frame = ttk.Frame(frame)
        gender_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Radiobutton(gender_frame, text="Male", variable=gender, value="male").grid(row=0, column=0, padx=(0,10))
        ttk.Radiobutton(gender_frame, text="Female", variable=gender, value="female").grid(row=0, column=1)
        return gender

    # Function to create username input fields
    def create_username_fields(frame):
        global username
        ttk.Label(frame, text="Username").grid(row=6, column=0, sticky=tk.W, pady=(10,0))
        username = ttk.Entry(frame, width=40)
        username.grid(row=7, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(frame, text="Confirm Username").grid(row=8, column=0, sticky=tk.W, pady=(10,0))
        confirm_username = ttk.Entry(frame, width=40)
        confirm_username.grid(row=9, column=0, columnspan=2, sticky=tk.W)
        return username, confirm_username

    # Function to create password input fields
    def create_password_fields(frame):
        global password
        ttk.Label(frame, text="Password").grid(row=10, column=0, sticky=tk.W, pady=(10,0))
        password = ttk.Entry(frame, width=30, show="*")
        password.grid(row=11, column=0, padx=(0,10), sticky=tk.W)
        
        global confirm_password
        ttk.Label(frame, text="Re-enter Password").grid(row=10, column=1, sticky=tk.W, pady=(10,0))
        confirm_password = ttk.Entry(frame, width=30, show="*")
        confirm_password.grid(row=11, column=1, sticky=tk.W)
        return password, confirm_password

    # Function to handle sign up button click
    def sign_up():
        print("Sign up clicked")

    # Function to create the sign-up form
    global root
    def create_signup_form():
        root = tk.Tk()
        root.title("Create a new account")
        root.configure(bg="#212121")

        # Maximize the window manually by getting the screen's dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")  # Set window size to screen size

        # Create a main frame to center the content
        main_frame = ttk.Frame(root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

        # Create input fields
        first_name, last_name = create_name_fields(main_frame)
        month, day, year = create_birthday_fields(main_frame)
        gender = create_gender_fields(main_frame)
        username, confirm_username = create_username_fields(main_frame)
        password, confirm_password = create_password_fields(main_frame)
        
        # Terms and policy text
        terms_text = "People who use our service may have uploaded your contact information to ActivArc."
        ttk.Label(main_frame, text=terms_text, wraplength=400).grid(row=12, column=0, columnspan=2, pady=(20,5))
        
        policy_text = "By clicking Sign Up, you agree to our Terms, Privacy Policy and Cookies Policy."
        ttk.Label(main_frame, text=policy_text, wraplength=400).grid(row=13, column=0, columnspan=2, pady=(0,10))
        
        # Sign up button
        ttk.Button(main_frame, text="Sign Up", command=lambda: signup(confirm_password.get())).grid(row=14, column=0, columnspan=2)
        
        # Link to login page
        account_link = ttk.Label(main_frame, text="Already have an account?", foreground="blue", cursor="hand2")
        account_link.grid(row=15, column=0, columnspan=2, pady=(10,0))
        account_link.bind("<Button-1>", lambda e: switch_to_login(root))

        
        return root
    
    def switch_to_login(current_window):
        current_window.destroy()  # Close the sign-up page
        subprocess.run(["python", "loginPage.py"])

    # Main entry point
    if __name__ == "__main__":
        root = create_signup_form()
        root.mainloop()
def home_page():
<<<<<<< HEAD
    # new page for more  
    def more():
        more_page=Toplevel()

        more_page.title("More")
        more_page.geometry("250x1080")

        # BMI calculator button
        bmi_button=Button(more_page,text="BMI Calculator",font=("Times New Roman", 15))
        bmi_button.place(x=20,y=20)

        # Calorie calculator button
        calorie_button=Button(more_page,text="Calorie Calculator",font=("Times New Roman", 15))
        calorie_button.place(x=20,y=60)

        # Workout button
        workout_button=Button(more_page,text="Workout",font=("Times New Roman", 15))
        workout_button.place(x=20,y=100)

        # Log out button
        log_out_btn=Button(more_page,text="Log Out",font=("Times New Roman",15))
        log_out_btn.place(x=20,y=150)

        mainloop()

    home_page=tk.Tk()
    home_page.title("ActivArc")
    home_page.geometry("600x600")
    home_page.configure(bg="#212121")

    def food():
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
            
            def add_food(self):
                try:
                    food = self.food_var.get()
                    weight = float(self.weight_var.get() or 0)
                    calories = float(self.calories_var.get() or 0) or (self.food_db.get(food, 0) * weight / 100)
                    
                    if not food:
                        messagebox.showerror("Error", "Please select a food item")
                        return
                        
                    if calories <= 0:
                        messagebox.showerror("Error", "Calories must be greater than 0")
                        return
                        
                    self.history.insert("", 0, values=(food, f"{weight}g", f"{calories:.1f} kcal"))
                    self.update_total()
                    
                    # Clear inputs
                    self.weight_var.set("")
                    self.calories_var.set("")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers")
            
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
    
    def logout():
        try:
            home_page.destroy()
        except:
            pass
        login()

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

        root.mainloop()


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

    # Log out Button
    log_out_btn = Button(frame1, text="Log Out",font=("Times New Roman",15),fg="#FF9500",bg="#212121",command=logout)
    log_out_btn.pack(pady=10,anchor="w")

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
=======
    page1.destroy()
    # calls homePage
    subprocess.run(["python","homePage.py"])
>>>>>>> 3f2d58c45b746cc08c4992972e73dadf6fe7445f

login()  # starts with login 