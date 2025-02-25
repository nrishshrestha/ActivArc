from tkinter import messagebox, ttk
import sqlite3
import datetime
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Loading session
def load_session():
    try:
        with open("session.txt", "r") as file:
            return int(file.read().strip())
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

# Fetching data from database
def database():
    user_id = load_session()

    if user_id is None:
        return ("N/A", "N/A", "N/A", "N/A", "N/A")

    try:
        conn = sqlite3.connect("activarc.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT first_name, last_name, birthday, gender, username
            FROM users WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()
        conn.close()

        return user if user else ("N/A", "N/A", "N/A", "N/A", "N/A")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return ("N/A", "N/A", "N/A", "N/A", "N/A")

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

        try:
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
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

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
frame1_width = int(screen_width * 0.25)  # 25% of screen width for the left panel
frame1_height = screen_height  # height of screen
frame1.place(relx=0.0, rely=0.0, width=frame1_width, height=frame1_height)  # Specify width and height in place()

# Modify the logo size and position
if os.path.exists("image 1.png"):
    image1 = Image.open("image 1.png")
    # Make logo smaller - 15% of frame width instead of 60%
    logo_width = int(frame1_width * 0.15)  
    logo_height = logo_width  # Keep aspect ratio square
    resized_image1 = image1.resize((logo_width, logo_height), Image.LANCZOS)
    image1_photo = ImageTk.PhotoImage(resized_image1)
    image1_label = Label(frame1, image=image1_photo, bg="#212121")
    image1_label.image = image1_photo
    # Position logo in top-left corner with small padding
    image1_label.pack(pady=(10, 5), padx=(5, 0), anchor="w")  
else:
    print("Error: image 1.png not found!")

# Load and display the banner image with adjusted position
if os.path.exists("banner.png"):
    banner_image = Image.open("banner.png")
    banner_width = int(screen_width * 0.73)  # 73% of screen width
    banner_height = int(screen_height * 0.8)  # 80% of screen height
    
    # Calculate aspect ratio to maintain image proportions
    banner_ratio = min(banner_width / banner_image.width, banner_height / banner_image.height)
    new_width = int(banner_image.width * banner_ratio)
    new_height = int(banner_image.height * banner_ratio)
    
    resize_banner = banner_image.resize((new_width, new_height), Image.LANCZOS)
    banner_photo = ImageTk.PhotoImage(resize_banner)
    
    # Create a frame for the banner
    banner_frame = Frame(home_page, bg="#212121")
    banner_frame.place(relx=0.26, rely=0.0, relwidth=0.74, relheight=1.0)
    
    banner_label = Label(banner_frame, image=banner_photo, bg="#212121")
    banner_label.image = banner_photo
    banner_label.place(relx=0.5, rely=0.5, anchor="center")
else:
    print("Error: banner.png not found!")

user_data = database()

# User
username = Label(frame1, text=f"User: {user_data[4]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
username.pack(pady=10, anchor="w")

# Full Name
fullname = Label(frame1, text=f"Name: {user_data[0]} {user_data[1]}", font=("Times New Roman", 15), bg="#212121", fg="#FF9500")
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
chnge_pwd = Button(frame1, text="Change Password", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=change_pwd)
chnge_pwd.pack(pady=10, anchor="w")

# Log out Button
log_out_btn = Button(frame1, text="Log Out", font=("Times New Roman", 15), fg="#FF9500", bg="#212121", command=logout)
log_out_btn.pack(pady=10, anchor="w")

# Delete user Button
del_user = Button(frame1, text="Delete User", font=("Times New Roman", 15), fg="#DC143C", bg="#212121", command=del_acc)
del_user.pack(pady=10, anchor="w")

# About us
about_us = Label(frame1, text='''About us:
                 At ActivArc, we're passionate about empowering individuals to achieve their fitness goals. \nBorn from a shared desire to make fitness tracking \nmore accessible and insightful, ActivArc combines \ncutting-edge technology with a user-friendly design.\nWe believe that everyone deserves the tools to \nunderstand their bodies and unlock their full potential.\nOur team is dedicated to continuous innovation, constantly \nstriving to improve ActivArc and provide you with the \nmost accurate and motivating fitness companion.''', font=("Arial", 10), height=15, width=70, justify="center", wraplength=500, bg="#212121", fg="#FF9500")
about_us.pack(side="bottom", pady=50, anchor="w")

mainloop()