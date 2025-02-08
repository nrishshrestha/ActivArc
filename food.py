import tkinter as tk
from tkinter import*

root = Tk()
root.title("Food and Calories Tracker")
root.geometry("400x400")


def add_food():
    food = food_entry.get()
    calories = calories_entry.get()
    food_list.insert(END, food)
    calories_list.insert(END, calories)
    food_entry.delete(0, END)
    calories_entry.delete(0, END)

food_label = Label(root, text="Enter Food: ")
food_label.place(x=30, y=50)
food_entry = Entry(root)
food_entry.place(x=100, y=50)

calories_label = Label(root, text="Enter Calories: ")
calories_label.place(x=30, y=90)
calories_entry = Entry(root)
calories_entry.place(x=110, y=90)

add_button = Button(root, text="Add Food", command=add_food)
add_button.place(x=230, y=300)

food_list = Listbox(root)
food_list.place(x=30, y=130)

calories_list = Listbox(root)
calories_list.place(x=170, y=130)

root.mainloop()