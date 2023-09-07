import tkinter as tk
import feedback
import ActionRecognition
import NumAndAlpheRecognition

def menuSelection():
    Menu = tk.Tk()
    ## geting the current users name to show it on the menu page.
    userName = " "
    with open('currentUser.txt') as f:
        userName = f.read()
    title = tk.Label(Menu, text="Hello " + userName, font=("Arial", 20, "bold"), bg="lightblue",foreground="black")
    title.pack()
    canvas = tk.Canvas(Menu, width=400, height=400, bg="lightblue")
    canvas.pack()
    # made three rounded buttons
    button1 = tk.Button(Menu, text="Number & Alphabet Recognition", font=("Arial", 16, "bold"),
                         command=NumAndAlpheRecognition.NumAlpheRecognition, bg="lightblue", bd=1)
    button2 = tk.Button(Menu, text="Actions Recognition", font=("Arial", 16, "bold"), 
                        command=ActionRecognition.runAction, bg="lightblue", bd=2)
    button3 = tk.Button(Menu, text="Feedback", font=("Arial", 16, "bold"), 
                        command=feedback.feedback_main, bg="lightblue", bd=3)

    canvas.create_window(200, 100, window=button1)
    canvas.create_window(200, 200, window=button2)
    canvas.create_window(200, 300, window=button3)

    Menu.title("Menu")
    Menu.geometry("400x400")

    Menu.mainloop()
