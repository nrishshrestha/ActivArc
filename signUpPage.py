import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import hashlib

# Function to create name input fields
def create_name_fields(frame):
    ttk.Label(frame, text="First Name").grid(row=0, column=0, sticky=tk.W)
    first_name = ttk.Entry(frame, width=30)
    first_name.grid(row=1, column=0, padx=(0,10), sticky=tk.W)
    
    ttk.Label(frame, text="Last Name").grid(row=0, column=1, sticky=tk.W)
    last_name = ttk.Entry(frame, width=30)
    last_name.grid(row=1, column=1, sticky=tk.W)
    return first_name, last_name

# Function to create birthday input fields
def create_birthday_fields(frame):
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
    
    years = list(range(1900, 2101))
    year = ttk.Combobox(birthday_frame, values=years, width=12, state='readonly')
    year.set('Year')
    year.grid(row=0, column=2, padx=5)
    return month, day, year

# Function to create gender selection fields
def create_gender_fields(frame):
    ttk.Label(frame, text="Gender").grid(row=4, column=0, sticky=tk.W, pady=(10,0))
    
    gender_frame = ttk.Frame(frame)
    gender_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W)
    
    gender = tk.StringVar()
    ttk.Radiobutton(gender_frame, text="Male", variable=gender, value="male").grid(row=0, column=0, padx=(0,10))
    ttk.Radiobutton(gender_frame, text="Female", variable=gender, value="female").grid(row=0, column=1)
    return gender

# Function to create username input fields
def create_username_fields(frame):
    ttk.Label(frame, text="Username").grid(row=6, column=0, sticky=tk.W, pady=(10,0))
    username = ttk.Entry(frame, width=40)
    username.grid(row=7, column=0, columnspan=2, sticky=tk.W)
    
    ttk.Label(frame, text="Confirm Username").grid(row=8, column=0, sticky=tk.W, pady=(10,0))
    confirm_username = ttk.Entry(frame, width=40)
    confirm_username.grid(row=9, column=0, columnspan=2, sticky=tk.W)
    return username, confirm_username

# Function to create password input fields
def create_password_fields(frame):
    ttk.Label(frame, text="Password").grid(row=10, column=0, sticky=tk.W, pady=(10,0))
    password = ttk.Entry(frame, width=30, show="*")
    password.grid(row=11, column=0, padx=(0,10), sticky=tk.W)
    
    ttk.Label(frame, text="Re-enter Password").grid(row=10, column=1, sticky=tk.W, pady=(10,0))
    confirm_password = ttk.Entry(frame, width=30, show="*")
    confirm_password.grid(row=11, column=1, sticky=tk.W)
    return password, confirm_password

# Function to create security question fields
def create_security_fields(frame):
    ttk.Label(frame, text="Security Question").grid(row=12, column=0, sticky=tk.W, pady=(10,0))
    security_question = ttk.Entry(frame, width=40)
    security_question.grid(row=13, column=0, columnspan=2, sticky=tk.W)
    
    ttk.Label(frame, text="Security Answer").grid(row=14, column=0, sticky=tk.W, pady=(10,0))
    security_answer = ttk.Entry(frame, width=40)
    security_answer.grid(row=15, column=0, columnspan=2, sticky=tk.W)
    return security_question, security_answer

# Function to handle sign up button click
def sign_up():
    # Get input values
    first_name_val = first_name.get()
    last_name_val = last_name.get()
    month_val = month.get()
    day_val = day.get()
    year_val = year.get()
    gender_val = gender.get()
    username_val = username.get()
    confirm_username_val = confirm_username.get()
    password_val = password.get()
    confirm_password_val = confirm_password.get()
    security_question_val = security_question.get()
    security_answer_val = security_answer.get()
    
    # Validate inputs
    if not all([first_name_val, last_name_val, month_val, day_val, year_val, gender_val, username_val, confirm_username_val, password_val, confirm_password_val, security_question_val, security_answer_val]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    if username_val != confirm_username_val:
        messagebox.showerror("Error", "Usernames do not match")
        return
    
    if password_val != confirm_password_val:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Hash the password and security answer
    password_hash = hashlib.sha256(password_val.encode()).hexdigest()
    security_answer_hash = hashlib.sha256(security_answer_val.lower().encode()).hexdigest()
    
    # Simulate successful registration
    messagebox.showinfo("Success", "Account created successfully!")
    root.destroy()
    show_success_page()

# Function to handle navigation to login page
def show_login(success_root):
    success_root.destroy()
    subprocess.run(["python", "loginPage.py"])
    print("Navigate to login page")

# Function to show success page
def show_success_page():
    success_root = tk.Tk()
    success_root.title("Registration Successful")
    
    ttk.Label(success_root, text="You are successfully registered. Please go to the login page.").pack(pady=20)
    ttk.Button(success_root, text="Go to Login Page", command=lambda: show_login(success_root)).pack(pady=10)
    
    success_root.mainloop()

# Function to create the sign-up form
def create_signup_form():
    global root
    root = tk.Tk()
    root.title("Create a new account")
    
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Create input fields
    global first_name, last_name, month, day, year, gender, username, confirm_username, password, confirm_password, security_question, security_answer
    first_name, last_name = create_name_fields(main_frame)
    month, day, year = create_birthday_fields(main_frame)
    gender = create_gender_fields(main_frame)
    username, confirm_username = create_username_fields(main_frame)
    password, confirm_password = create_password_fields(main_frame)
    security_question, security_answer = create_security_fields(main_frame)
    
    # Terms and policy text
    terms_text = "People who use our service may have uploaded your contact information to ActivArc."
    ttk.Label(main_frame, text=terms_text, wraplength=400).grid(row=16, column=0, columnspan=2, pady=(20,5))
    
    policy_text = "By clicking Sign Up, you agree to our Terms, Privacy Policy and Cookies Policy."
    ttk.Label(main_frame, text=policy_text, wraplength=400).grid(row=17, column=0, columnspan=2, pady=(0,10))
    
    # Sign up button
    ttk.Button(main_frame, text="Sign Up", command=sign_up).grid(row=18, column=0, columnspan=2)
    
    # Link to login page
    account_link = ttk.Label(main_frame, text="Already have an account?", foreground="blue", cursor="hand2")
    account_link.grid(row=19, column=0, columnspan=2, pady=(10,0))
    account_link.bind("<Button-1>", lambda e: show_login(root))
    
    return root

# Main entry point
if __name__ == "__main__":
    root = create_signup_form()
    root.mainloop()