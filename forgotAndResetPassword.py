import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import subprocess
import sqlite3

bk = "#282828"  # Dark background
bg = "#212121"  # Light background
oran = "#FF9500"  # Orange accent

def show_success_page():
    success_root = tk.Tk()
    success_root.title("Password Reset Successful")
    success_root.configure(bg=bk)
    
    ttk.Label(success_root, text="Your password is reset. Please go to login page.", background=bk, foreground=oran).pack(pady=20)
    ttk.Button(success_root, text="Go to Login Page", command=lambda: show_login(success_root), style="TButton").pack(pady=10)
    
    success_root.mainloop()

def show_login(success_root):
    success_root.destroy()
    subprocess.run(["python", "log_sign_combi.py"])

def reset_password():
    username = username_entry.get()
    current_pwd = current_password.get()
    new_pwd = new_password.get()
    confirm_pwd = confirm_password.get()
    
    if not all([username, current_pwd, new_pwd, confirm_pwd]):
        messagebox.showerror("Error", "All fields are required")
        return
        
    if new_pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Verify current password
    conn = sqlite3.connect("activarc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == current_pwd:
        # Update password
        conn = sqlite3.connect("activarc.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_pwd, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password reset successfully!")
        root.destroy()
        show_success_page()
    else:
        messagebox.showerror("Error", "Current password is incorrect")

# Create main window
root = tk.Tk()
root.title("ActivArc")
root.configure(bg=bk)

# Set window size and center it
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Update the grid configurations for centering
main_frame = ttk.Frame(root, padding="20", style="TFrame")
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.grid_columnconfigure(0, weight=1)  # Center contents horizontally

# Title - centered
title_label = ttk.Label(main_frame, text="Forgot Password?", font=('Helvetica', 14, 'bold'), 
                       background=bk, foreground=oran)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username field - centered
ttk.Label(main_frame, text="Username", background=bk, foreground=oran).grid(row=1, column=0, pady=(0, 5))
username_entry = ttk.Entry(main_frame, width=42)
username_entry.grid(row=2, column=0, pady=(0, 15))

# Current Password - centered
ttk.Label(main_frame, text="Current Password", background=bk, foreground=oran).grid(row=3, column=0, pady=(0, 5))
current_password = ttk.Entry(main_frame, width=42, show="*")
current_password.grid(row=4, column=0, pady=(0, 15))

# New Password - centered
ttk.Label(main_frame, text="New Password", background=bk, foreground=oran).grid(row=5, column=0, pady=(0, 5))
new_password = ttk.Entry(main_frame, width=42, show="*")
new_password.grid(row=6, column=0, pady=(0, 15))

# Confirm Password - centered
ttk.Label(main_frame, text="Confirm Password", background=bk, foreground=oran).grid(row=7, column=0, pady=(0, 5))
confirm_password = ttk.Entry(main_frame, width=42, show="*")
confirm_password.grid(row=8, column=0, pady=(0, 15))

# Function to toggle password visibility
def toggle_password_visibility():
    if show_password_var.get():
        current_password.config(show="")
        new_password.config(show="")
        confirm_password.config(show="")
    else:
        current_password.config(show="*")
        new_password.config(show="*")
        confirm_password.config(show="*")

# Show Password Checkbox - moved below confirm password
show_password_var = tk.BooleanVar()
show_password_check = ttk.Checkbutton(main_frame, text="Show Password", 
                                     variable=show_password_var, 
                                     command=toggle_password_visibility, 
                                     style="TCheckbutton")
show_password_check.grid(row=9, column=0, pady=(0, 15))

# Reset Button - centered
reset_button = ttk.Button(main_frame, text="Reset", command=reset_password, style="TButton")
reset_button.grid(row=10, column=0, pady=(10, 0))

# Company Logo
logo_label = ttk.Label(root, text="ActivArc", font=('Helvetica', 16, 'bold'), background=bk, foreground=oran)
logo_label.place(x=20, y=20)

# Apply styles
style = ttk.Style()
style.configure("TFrame", background=bk)
style.configure("TLabel", background=bk, foreground=oran)
style.configure("TButton", background=oran, foreground=bk, font=('Helvetica', 12, 'bold'))
style.configure("TCheckbutton", background=bk, foreground=oran)

# Start the application
root.mainloop()