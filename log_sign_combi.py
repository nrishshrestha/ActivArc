import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
from PIL import Image, ImageTk
import subprocess
import sqlite3

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
def signup():  
    fname = first_name.get()
    lname = last_name.get()
    user = username.get()
    passw = password.get()
    conf_pass = confirm_password.get()  # Get confirm password directly
    birth_date = f"{year.get()} {month.get()} {day.get()}"
    gender_value = gender.get()

    # Validate all fields
    if not all([fname, lname, birth_date, gender_value, user, passw]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    if passw != conf_pass:  # Compare with local confirm password
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
    login_button = Button(main_frame, text="Login", font=("Times New Roman", 15), command=verify_login)
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
def signup():
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
        ttk.Button(main_frame, text="Sign Up", command=lambda: signup()).grid(row=14, column=0, columnspan=2)
        
        # Link to login page
        account_link = ttk.Label(main_frame, text="Already have an account?", foreground="blue", cursor="hand2")
        account_link.grid(row=15, column=0, columnspan=2, pady=(10,0))
        account_link.bind("<Button-1>", lambda e: switch_to_login(root))

        
        return root
    
    def switch_to_login(current_window):
        current_window.destroy()  # Close the sign-up page
        login()

    # Main entry point
    if __name__ == "__main__":
        root = create_signup_form()
        root.mainloop()

def home_page():
    page1.destroy()
    # calls homePage
    subprocess.run(["python","homePage.py"])

login()  # starts with login