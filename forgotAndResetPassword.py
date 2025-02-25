import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import subprocess

def show_success_page():
    success_root = tk.Tk()
    success_root.title("Password Reset Successful")
    
    ttk.Label(success_root, text="Your password is reset. Please go to login page.").pack(pady=20)
    ttk.Button(success_root, text="Go to Login Page", command=lambda: show_login(success_root)).pack(pady=10)
    
    success_root.mainloop()

def show_login(success_root):
    success_root.destroy()
    subprocess.run(["python", "log_sign_combi.py"])

def reset_password():
    username = username_entry.get()
    new_pwd = new_password.get()
    confirm_pwd = confirm_password.get()
    
    if not all([username, new_pwd, confirm_pwd]):
        messagebox.showerror("Error", "All fields are required")
        return
        
    if new_pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Simulate password reset
    messagebox.showinfo("Success", "Password reset successfully!")
    root.destroy()
    show_success_page()

# Create main window
root = tk.Tk()
root.title("ActivArc")

# Set window size and center it
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = ttk.Label(main_frame, text="Forgot Password?", font=('Helvetica', 14, 'bold'))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username field
ttk.Label(main_frame, text="Username").grid(row=1, column=0, sticky='w', pady=(0, 5))
username_entry = ttk.Entry(main_frame, width=42)
username_entry.grid(row=2, column=0, columnspan=2, pady=(0, 15))

# New Password
ttk.Label(main_frame, text="New Password").grid(row=3, column=0, sticky='w', pady=(0, 5))
new_password = ttk.Entry(main_frame, width=42, show="*")
new_password.grid(row=4, column=0, columnspan=2, pady=(0, 15))

# Confirm Password
ttk.Label(main_frame, text="Confirm Password").grid(row=5, column=0, sticky='w', pady=(0, 5))
confirm_password = ttk.Entry(main_frame, width=42, show="*")
confirm_password.grid(row=6, column=0, columnspan=2, pady=(0, 15))

# Function to toggle password visibility
def toggle_password_visibility():
    if show_password_var.get():
        new_password.config(show="")
        confirm_password.config(show="")
    else:
        new_password.config(show="*")
        confirm_password.config(show="*")

# Show Password Checkbox
show_password_var = tk.BooleanVar()
show_password_check = ttk.Checkbutton(main_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_check.grid(row=6, column=2, padx=(10, 0))

# Reset Button
reset_button = ttk.Button(main_frame, text="Reset", command=reset_password)
reset_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))

# Company Logo
logo_label = ttk.Label(root, text="ActivArc", font=('Helvetica', 16, 'bold'))
logo_label.place(x=20, y=20)

# Start the application
root.mainloop()