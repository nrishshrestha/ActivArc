from tkinter import *
root=Tk()
root.geometry("1000x600")
root.title("BMI Calculator")
root.resizable(False,False)

def calculate():
    try:
        h=float(height.get())/100
        w=float(weight.get())
        category=""

        if h <= 0 or w <= 0:
           result.config(text="Error: Height and Weight \nmust be positive numbers.", fg="red")
           return
        
        bmi=w/(h**2)
        
        if bmi < 18.5:
            category = "Underweight"
            message='You are underweight.\nYou need to gain weight.'
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
            message='You are healthy.\nKeep it up!'
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            message='You are overweight.\nYou need to lose weight.'
        else:
            category= "Obese"
            message='You are obese.\nYou need to lose weight.'

        result.config(text=f"Your BMI: {bmi:.2f}\n\nCategory: {category} \n\n{message}",font=('Arial',18),fg='black')

    except ValueError:
        result.config(text="Error: Please enter valid values.", fg="red")

def clear():
    age.delete(0, END)
    height.delete(0, END)
    weight.delete(0, END)
    gender.set(" ")
    result.config(text="Your BMI: \n\nCategory: ",font=('Arial',18),fg='black')

#Age Input
Label(root,text="Age",font=('Arial',20)).place(x=70,y=30)
age=Entry(root,font=('Arial',18))
age.place(x=150,y=35)

#Gender Input
gender=StringVar(value=' ')
Label(root,text='Gender',font=('Arial',20)).place(x=50,y=90)
Radiobutton(root,text='Male',variable=gender,value='Male',font=('Arial',18)).place(x=150,y=93.5)
Radiobutton(root,text='Female',variable=gender,value='Female',font=('Arial',18)).place(x=150,y=130)

#Height Input
Label(root,text="Height",font=('Arial',20)).place(x=55,y=180)
Label(root,text="cm",font=('Arial',20)).place(x=420,y=180)
height=Entry(root,font=('Arial',18))
height.place(x=150,y=185)

#Weight Input
Label(root,text="Weight",font=('Arial',20)).place(x=50,y=240)
Label(root,text="kg",font=('Arial',20)).place(x=420,y=240)
weight=Entry(root,font=('Arial',18))
weight.place(x=150,y=245)

#Calcuate and Clear Button
Button(root,text="Caclulate",command=calculate,font=('Arial',18),relief='solid').place(x=100,y=300)
Button(root,text="Clear",command=clear,font=('Arial',18),relief='solid').place(x=280,y=300)

#Result
Frame(root,width=400,height=100,bd=1,relief='solid').place(x=500,y=30)
Frame(root,width=400,height=200,bd=1,relief='solid').place(x=500,y=80)
Label(root,text="Result",font=('Arial',20,'bold')).place(x=510,y=35)
result=Label(root,text="Your BMI: \n\nCategory: ",font=('Arial',18))
result.place(x=510,y=85)

#Information
Label(root,text='BMI Information',font=('Arial',20,'bold')).place(x=50,y=380)
bmi_info_text = (
    "Body Mass Index (BMI) is a measurement of a person's weight \n"
    "with respect to their height. It is an indicator rather than \n"
    "a direct measurement of total body fat. BMI helps assess \n"
    "whether an individual is underweight, normal, overweight, \n"
    "or obese based on standardized categories."
)

Label(root, text=bmi_info_text, font=('Arial',16), justify="left").place(x=50, y=420)

mainloop()