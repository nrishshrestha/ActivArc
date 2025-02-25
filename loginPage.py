from tkinter import *
import tkinter as tk
import subprocess

def close_page():
    page1.destroy()
    subprocess.run(["python","homePage.py"])

def open_signup_page():
    page1.destroy()
    subprocess.run(["python", "signUpPage.py"])

def open_forgot_password_page():
    page1.destroy()
    subprocess.run(["python", "forgotAndResetPassword.py"])

def login():
    global page1  # make page1 global so that it can be accessed in close_page function

    page1 = tk.Tk()
    page1.title("ActivArc")
    page1.configure(bg="#212121")

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
    login_button = Button(main_frame, text="Login", font=("Times New Roman", 15), command=close_page)
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

login()