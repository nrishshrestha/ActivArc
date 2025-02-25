from tkinter import messagebox, ttk
from typing import List, Tuple, Dict
import sqlite3
import datetime
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

#Loading session
def load_session():
    try:
        with open("session.txt", "r") as file:
            return int(file.read().strip())
    except:
        return None  # If no session exists, return None

#Fetching data from database
def database():
    user_id = load_session()

    if user_id is None:
        return ("N/A", "N/A", "N/A", "N/A", "N/A")

    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, birthday, gender, username
        FROM users WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    return user if user else ("N/A", "N/A", "N/A", "N/A", "N/A")

def refresh_home_page():
    """Reload user data and update the labels."""
    global user_data
    user_data = database()
    username.config(text=f"Username: {user_data[4]}")
    fullname.config(text=f"Full Name: {user_data[0]} {user_data[1]}")
    home_page.update_idletasks()

# logout
def logout():
    home_page.destroy()
    subprocess.run(["python", "loginPage.py"])


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

    #Change Password button
    change_pswd=Button(more_page,text="Change Password",font=("Times New Roman",15))
    change_pswd.place(x=20,y=150)

    # Log out button
    log_out_btn=Button(more_page,text="Log Out",font=("Times New Roman",15))
    log_out_btn.place(x=20,y=200)

    mainloop()

def change_pwd():
    subprocess.run(["python","forgotAndResetPassword.py"])

home_page=tk.Tk()
home_page.title("ActivArc")
home_page.geometry("600x600")
home_page.configure(bg="#212121")

def food():
    subprocess.run(["python","food.py"])

def work():
    subprocess.run(["python","workout_calculator.py"])

def bmi():
    subprocess.run(["python","BMI.py"])


# Maximize the window manually by getting the screen's dimensions
screen_width = home_page.winfo_screenwidth()
screen_height = home_page.winfo_screenheight()
home_page.geometry(f"{screen_width}x{screen_height}")  # Set window size to screen size

# frame1
frame1=Frame(home_page,bg="#212121",relief=GROOVE,bd=2,padx=20,pady=20) # frame1
frame1_width=400 # width of frame1
frame1_height=screen_height # height of screen
frame1.place(relx=0.0, rely=0.0, width=frame1_width, height=frame1_height)  # Specify width and height in place()

user_data = database()

# User
username = Label(frame1, text=f"Username: {user_data[4]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
username.pack(pady=10, anchor="w")

# Full Name
fullname = Label(frame1, text=f"Full Name: {user_data[0]} {user_data[1]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
fullname.pack(pady=10, anchor="w")

# BMI Calculator
bmi_button=Button(frame1,text="BMI Calculator",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=bmi)
bmi_button.pack(pady=10,anchor="w")

# Calorie Eaten
calorie_button=Button(frame1,text="Calorie Eaten",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=food)
calorie_button.pack(pady=10,anchor="w")

# Calorie Burned  
workout_button=Button(frame1,text="Calorie Burned",font=("Times New Roman", 15),fg="#FF9500",bg="#212121",command=work)
workout_button.pack(pady=10,anchor="w")

# Change Password Button   
change_pwd = Button(frame1, text="Change Password",font=("Times New Roman",15),fg="#FF9500",bg="#212121",command=change_pwd)
change_pwd.pack(pady=10,anchor="w")

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