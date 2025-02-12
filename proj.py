from tkinter import *
import tkinter as tk

def close_page():
    page1.destroy()

def login():
    global page1  # make page1 global so that it can be accessed in close_page function

    page1 = tk.Tk()
    page1.title("ActivArc")
    page1.attributes("-fullscreen", True)
    page1.configure(bg="#212121")

    def password_show_hide():
        check = var.get()
        if check == 1:
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    # Frame for centralization
    main_frame = Frame(page1, bg="lightgray", relief=GROOVE, bd=2, padx=20, pady=20)
    main_frame.place(x=850, y=400)  # Adjusted for centralization

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
    login = Button(main_frame, text="Login", font=("Times New Roman", 15), command=close_page)
    login.pack(pady=10)

    # Forgot Password
    fpassword = Button(main_frame, text="Forgot Password", font=("Times New Roman", 15))
    fpassword.pack(pady=10)

    # Don't Have an account?
    noacc = Label(main_frame, text="Don't have an account? | Create one for free!", font=("Times New Roman", 10), fg="blue", bg="lightgray")
    noacc.pack(pady=10)

    # Sign Up Button
    signup = Button(main_frame, text="Sign up", font=("Times New Roman", 15))
    signup.pack(pady=10)

    page1.mainloop()

login()

mainloop()
