import tkinter as tk
from tkinter import messagebox

def submit():
    email = email_entry.get()
    if email:
        email_label.pack_forget()
        email_entry.pack_forget()
        submit_button.pack_forget()
        code_label.pack(pady=10)
        code_entry.pack(pady=5)
        verify_button.pack(pady=20)
        messagebox.showinfo("Code Sent", f"A verification code has been sent to {email}")
    else:
        messagebox.showwarning("Error", "Please enter your email address.")

def verify():
    code = code_entry.get()
    if code == "123456":
        messagebox.showinfo("Success", "Verification successful!")
        root.destroy()
        open_password_reset_window()
    else:
        messagebox.showerror("Error", "Invalid verification code. Please try again.")

def open_password_reset_window():
    password_reset_window = tk.Tk()
    password_reset_window.title("Reset Password")
    password_reset_window.geometry("300x200")
    reset_frame = tk.Frame(password_reset_window, bd=2, relief="groove", padx=10, pady=10)
    reset_frame.pack(pady=20, padx=20, fill="both", expand=True)
    new_password_label = tk.Label(reset_frame, text="New Password:")
    new_password_label.pack(pady=10)
    new_password_entry = tk.Entry(reset_frame, width=30, show="*")
    new_password_entry.pack(pady=5)
    confirm_password_label = tk.Label(reset_frame, text="Confirm Password:")
    confirm_password_label.pack(pady=10)
    confirm_password_entry = tk.Entry(reset_frame, width=30, show="*")
    confirm_password_entry.pack(pady=5)

    def toggle_password_visibility():
        if show_password_var.get():
            new_password_entry.config(show="")
            confirm_password_entry.config(show="")
        else:
            new_password_entry.config(show="*")
            confirm_password_entry.config(show="*")

    show_password_var = tk.BooleanVar()
    show_password_check = tk.Checkbutton(reset_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
    show_password_check.pack(pady=5)

    def reset_password():
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if new_password == confirm_password:
            messagebox.showinfo("Success", "Password reset successfully!")
            password_reset_window.destroy()
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")

    reset_button = tk.Button(reset_frame, text="Reset Password", command=reset_password)
    reset_button.pack(pady=20)

root = tk.Tk()
root.title("Forgot Password")
root.geometry("300x250")
frame = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)
email_label = tk.Label(frame, text="Email:")
email_label.pack(pady=10)
email_entry = tk.Entry(frame, width=30)
email_entry.pack(pady=5)
submit_button = tk.Button(frame, text="Submit", command=submit)
submit_button.pack(pady=20)
code_label = tk.Label(frame, text="Verification Code:")
code_entry = tk.Entry(frame, width=30)
verify_button = tk.Button(frame, text="Verify", command=verify)
root.mainloop()
