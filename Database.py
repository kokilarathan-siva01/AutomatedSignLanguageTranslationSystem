import sqlite3
import os
from tkinter import *
from tkinter import messagebox

# making sure that the working directory is where the file is stored at.
currentDir = os.getcwd()
try:
    user_Data = sqlite3.connect(currentDir+"/Database/Users_Data.db")
    cursor_ = user_Data.cursor()
except Exception as error:
    messagebox.showerror("Error", "Invalid Directory, Please fix and try agian.")

try:
    # primary key can be customised.
    cursor_.execute('''CREATE TABLE IF NOT EXISTS users(
        userID text,
        password text,
        firstname text,
        surname text,
        email text
        )''')
    user_Data.commit()
except Exception as error:
    messagebox.showwarning("Warning", "Table has not been created due to invalid directory.")

### function to update and add new data into the database.
def update_data(userID,password,firstname,surname,email):
    
    cursor_.execute("INSERT INTO users VALUES (:userID, :password, :forename, :surname, :email)", {
        'userID': userID,
        'password': password,
        'forename': firstname,
        'surname': surname,
        'email': email,
        })
    user_Data.commit()

# to get the username and password to match in login process
def getUserPass():
    allUsername = []
    allPassword = []
    
    for i in cursor_.execute("SELECT * from users"):
        allUsername.append(i[0])
        allPassword.append(i[1])

    
    return allUsername,allPassword

### this function is used to get information based on a given userID.
def GetUserName(userID):
    currentPP = "SELECT * FROM users WHERE userID="+str(userID)
    cursoR =cursor_.execute(currentPP)
    names = None
    
    for i in cursoR:
        names = i
    
    return names

