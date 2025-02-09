from tkinter import *
import tkinter as tk

def close_page():
    page1.destroy()

def login():
    global page1 # make page1 global so that it can be accessed in close_page function

    page1 = tk.Tk()
    page1.title("ActivArc")
    page1.attributes("-fullscreen",True)

    def password_show_hide():
        check = var.get()
        if check == 1:
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    # Username Entrybox and label
    username = Label(page1, text="Username",font=("Times New Roman", 15))
    username.place(x=400, y=150, anchor="center")
    username_entry = Entry(page1, font=("Times New Roman", 15))
    username_entry.place(x=400, y=200, anchor="center")

    # Password Entrybox and label
    password = Label(page1, text="Password",font=("Times New Roman", 15))
    password.place(x=400, y=250, anchor="center")
    password_entry = Entry(page1, font=("Times New Roman", 15),show="*")
    password_entry.place(x=400, y=300, anchor="center")

    # Show and Hide password
    var = IntVar()
    c1 = Checkbutton(page1, text="Show Password", variable=var, font=("Times New Roman", 10),command=password_show_hide)
    c1.place(x=600, y=300, anchor="center")

    # Login Button
    login = Button(page1, text="Login",font=("Times New Roman", 15),command=close_page)
    login.place(x=400, y=350, anchor="center")

    # Forgot Password
    fpassword = Button(page1, text="Forgot Password",font=("Times New Roman", 15))
    fpassword.place(x=400, y=400, anchor="center")

    # Don't Have an account?
    noacc = Label(page1, text="Don't have an account? | Create one for free!",font=("Times New Roman", 10),fg="blue")
    noacc.place(x=400, y=450, anchor="center")

    # Sign Up Button
    signup = Button(page1, text="Sign up",font=("Times New Roman", 15))
    signup.place(x=400, y=475, anchor="center")

    page1.mainloop()

login()

mainloop()