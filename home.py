from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

# new page for more button
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

    mainloop()

home_page=tk.Tk()
home_page.title("ActivArc")
home_page.attributes("-fullscreen", True)
home_page.configure(bg="#212121")

# opening image for background
image = Image.open("random_image.png")
image = image.resize((1680, 600)) 
bg_image = ImageTk.PhotoImage(image)

Canvas = tk.Canvas(home_page, width=1680, height=600)
Canvas.place(x=125,y=100)

Canvas.create_image(0, 0, image=bg_image, anchor="nw")

# more button
more_button=Button(home_page,text="≡",font=("Times New Roman", 15),command=more)
more_button.place(x=20,y=20)

# active arc label
label_active = Label(home_page, text="ActiveArc",font=("Ink Free", 20),bg="#212121",fg="#FF9500")
label_active.place(x=60,y=20)

# about us
about_us=Label(home_page, text="About us: \nAt ActivArc, we're passionate about empowering individuals to achieve their fitness goals.  Born from a shared desire to make fitness tracking more accessible and insightful, ActivArc combines cutting-edge technology with a user-friendly design.  We believe that everyone deserves the tools to understand their bodies and unlock their full potential.  Our team is dedicated to continuous innovation, constantly striving to improve ActivArc and provide you with the most accurate and motivating fitness companion.",font=("Arial", 10),height=10,width=70,justify="center",wraplength=500,bg="#212121",fg="#FF9500")
about_us.place(x=1250,y=750)

home_page.mainloop()