from tkinter import messagebox, ttk
import sqlite3
import datetime
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# Loading session
def load_session():
    try:
        with open("session.txt", "r") as file:
            return int(file.read().strip())
    except:
        return None  # If no session exists, return None

# Fetching data from database
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

# delete user
def del_acc():
    delete_page = tk.Toplevel(home_page)
    delete_page.title("Delete User")
    delete_page.geometry("400x300")
    delete_page.configure(bg="#212121")

    # Username field
    tk.Label(delete_page, text="Username:", font=("Times New Roman", 12), fg="#FF9500", bg="#212121").pack(pady=5)
    username_entry = tk.Entry(delete_page, font=("Times New Roman", 12))
    username_entry.pack(pady=5)

    # Password field
    tk.Label(delete_page, text="Password:", font=("Times New Roman", 12), fg="#FF9500", bg="#212121").pack(pady=5)
    password_entry = tk.Entry(delete_page, font=("Times New Roman", 12), show="*")  # Password hidden
    password_entry.pack(pady=5)

    # Confirm deletion
    def confirm_delete():
        user = username_entry.get()
        passw = password_entry.get()

        # Ensuring all fields are filled
        if not user or not passw:
            messagebox.showerror("Error", "Please fill all the fields!")
            return

        # Delete user from database
        conn = sqlite3.connect("activarc.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=? AND password=?", (user, passw))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account deleted successfully!")
        delete_page.destroy()
        home_page.destroy()
        subprocess.run(["python", "loginPage.py"])

    # Confirm
    con = Button(delete_page, text="Confirm Delete", font=("Times New Roman", 12), fg="#FF9500", bg="#212121", command=confirm_delete)
    con.pack(pady=10)

# logout
def logout():
    home_page.destroy()
    subprocess.run(["python", "loginPage.py"])

# new page for more
def more():
    more_page = Toplevel()
    more_page.title("More")
    more_page.geometry("250x1080")

def change_pwd():
    subprocess.run(["python", "forgotAndResetPassword.py"])

home_page = tk.Tk()
home_page.title("ActivArc")
home_page.geometry("600x600")
home_page.configure(bg="#212121")

def food():
    subprocess.run(["python", "food.py"])

def work():
    subprocess.run(["python", "workout_calculator.py"])

def bmi():
    subprocess.run(["python", "BMI.py"])

# Maximize the window manually by getting the screen's dimensions
screen_width = home_page.winfo_screenwidth()
screen_height = home_page.winfo_screenheight()
home_page.geometry(f"{screen_width}x{screen_height}")  # Set window size to screen size

# frame1
frame1 = Frame(home_page, bg="#212121", relief=GROOVE, bd=2, padx=20, pady=20)  # frame1
frame1_width = 400  # width of frame1
frame1_height = screen_height  # height of screen
frame1.place(relx=0.0, rely=0.0, width=frame1_width, height=frame1_height)  # Specify width and height in place()

# Load and display the logo
try:
    image1 = Image.open("image 1.png")
    # Resize the image here
    resized_image1 = image1.resize((125, 125), Image.LANCZOS) # Adjust dimensions as needed
    image1_photo = ImageTk.PhotoImage(resized_image1)
    image1_label = Label(home_page, image=image1_photo, bg="#212121")
    image1_label.image = image1_photo
    image1_label.place(relx=0.25, rely=0.1, anchor=tk.CENTER) # adjust relx,rely, anchor as needed.
except FileNotFoundError:
    print("Error: image 1.png not found!")

# Load and display the banner image
try:
    banner_image = Image.open("banner.png")
    banner_photo = ImageTk.PhotoImage(banner_image)
    banner_label = Label(home_page, image=banner_photo, bg="#212121")  # add background color to label.
    banner_label.image = banner_photo  # Keep a reference!
    banner_label.place(relx=0.64, rely=0.5, anchor=tk.CENTER)  # adjust relx,rely, anchor as needed.
except FileNotFoundError:
    print("Error: banner.png not found!")

user_data = database()

# User
username = Label(frame1, text=f"Username: {user_data[4]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
username.pack(pady=10, anchor="w")

# Full Name
fullname = Label(frame1, text=f"Full Name: {user_data[0]} {user_data[1]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
fullname.pack(pady=10, anchor="w")

# BMI Calculator
bmi_button = Button(frame1, text="BMI Calculator", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=bmi)
bmi_button.pack(pady=10, anchor="w")

# Calorie Eaten
calorie_button = Button(frame1, text="Calorie Eaten", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=food)
calorie_button.pack(pady=10, anchor="w")

# Calorie Burned
workout_button = Button(frame1, text="Calorie Burned", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=work)
workout_button.pack(pady=10, anchor="w")

# Change Password Button
change_pwd = Button(frame1, text="Change Password", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=change_pwd)
change_pwd.pack(pady=10, anchor="w")

# Log out Button
log_out_btn = Button(frame1, text="Log Out", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=logout)
log_out_btn.pack(pady=10, anchor="w")

# Delete user Button
del_user = Button(frame1, text="Delete User", font=("Times New Roman", 15), fg="#DC143C", bg="#212121", command=del_acc)
del_user.pack(pady=10, anchor="w")

# About us
about_us = Label(frame1, text="About us: \nAt ActivArc, we're passionate about empowering \nindividuals to achieve their fitness goals. \nBorn from a shared desire to make fitness tracking \nmore accessible and insightful, ActivArc combines \ncutting-edge technology with a user-friendly design.\nWe believe that everyone deserves the tools to \nunderstand their bodies and unlock their full potential.\nOur team is dedicated to continuous innovation, constantly \nstriving to improve ActivArc and provide you with the \nmost accurate and motivating fitness companion.", font=("Arial", 10), height=15, width=70, justify="center", wraplength=500, bg="#212121", fg="#FF9500")
about_us.pack(side="bottom", pady=50, anchor="w")

mainloop()