from tkinter import *
import tkinter as tk

page1 = tk.Tk()
page1.title("ActivArc")
page1.geometry("1920x1080")

def password_show_hide():
    check = var.get()
    if check == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Creating a Canvas
Canvas = tk.Canvas(page1, width=800, height=600, highlightbackground="black", highlightthickness=1)
Canvas.pack(expand=True, padx=20,pady=20)

# Username Entrybox and label
username = Label(page1, text="Username",font=("Times New Roman", 15))
Canvas.create_window(400,150, window=username)
username_entry = Entry(page1, font=("Times New Roman", 15))
Canvas.create_window(400,200,window=username_entry)

# Password Entrybox and label
password = Label(page1, text="Password",font=("Times New Roman", 15))
Canvas.create_window(400,250, window=password)
password_entry = Entry(page1, font=("Times New Roman", 15),show="*")
Canvas.create_window(400,300,window=password_entry)

# Show and Hide password
var = IntVar()
c1 = Checkbutton(page1, text="Show Password", variable=var, font=("Times New Roman", 10),command=password_show_hide)
Canvas.create_window(570,300,window=c1)

# Login Button
login = Button(page1, text="Login",font=("Times New Roman", 15))
Canvas.create_window(400,350,window=login)

# Forgot Password
fpassword = Button(page1, text="Forgot Password",font=("Times New Roman", 15))
Canvas.create_window(400,400,window=fpassword)

# Don't Have an account?
noacc = Label(page1, text="Don't have an account? | Create one for free!",font=("Times New Roman", 10))
Canvas.create_window(400,450, window=noacc)

# Sign Up Button
signup = Button(page1, text="Sign up",font=("Times New Roman", 15))
Canvas.create_window(400,500,window=signup)

page1.mainloop()

