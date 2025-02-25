from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from typing import List, Tuple, Dict
import datetime
from PIL import Image, ImageTk
import subprocess

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

signup()