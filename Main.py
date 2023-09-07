from tkinter import *
from tkinter import messagebox
import Database
import Menu


class SignLanguageTranslatorApp:
    def __init__(self):
        self.mainScreen = None
        self.loginScreem = None
        self.registerScreen = None
        self.userIDRegister = None
        self.passwordRegister = None
        self.confirmPass = None
        self.firstname = None
        self.surname = None
        self.email = None
        self.code = None
        self.entryUserIDREgister = None
        self.entryPasswordRegister = None
        self.entryConfirmPassword = None
        self.entryFirstname = None
        self.entrySurname = None
        self.entryEmail = None
        self.entryAuthenCodes = None
        self.userIDLogin = None
        self.passwordLogin = None

    def getUserName(self, userID):
        alldetail = Database.GetUserName(userID)
        currentUser = str(alldetail[2] + " " + alldetail[3])
        return currentUser

    def clearEntry(self):
        self.entryUserIDREgister.delete(0, END)
        self.entryPasswordRegister.delete(0, END)
        self.entryConfirmPassword.delete(0, END)
        self.entryFirstname.delete(0, END)
        self.entrySurname.delete(0, END)
        self.entryEmail.delete(0, END)
        self.entryAuthenCodes.delete(0, END)

    def registerVerify(self):
        authenticationCode = "university"
        userIDdetail = self.userIDRegister.get()
        passwordDetail = self.passwordRegister.get()
        confirmPasswordDetail = self.confirmPass.get()
        firstnameDetail = self.firstname.get()
        surnameDetail = self.surname.get()
        emailDetail = self.email.get()
        autheCodeDetail = self.code.get()

        self.entryPasswordRegister.config(background='#D3D3D3')
        self.entryConfirmPassword.config(background='#D3D3D3')
        self.entryAuthenCodes.config(background='#D3D3D3')

        list_info = {'userID': userIDdetail, 'password': passwordDetail, 'confirmPassword': confirmPasswordDetail,
                     'firstname': firstnameDetail,
                     'surname': surnameDetail, 'email': emailDetail, 'code': autheCodeDetail}

        column_names = ['userID', 'password', 'confirmPassword', 'firstname', 'surname', 'email', 'code']
        counter = 0
        warn_mess = "Please fill in the following blank entries: \n"

        for i in range(len(column_names)):
            if not list_info[column_names[i]]:
                warn_mess += "({0}) ".format(i + 1) + column_names[i] + "\n"
            else:
                counter += 1

        if counter == len(list_info):
            if autheCodeDetail == authenticationCode:
                if passwordDetail == confirmPasswordDetail:
                    self.clearEntry()
                    Database.update_data(userIDdetail, passwordDetail, firstnameDetail, surnameDetail, emailDetail)
                    messagebox.showinfo("Successful", message="Successfully Registered.")
                else:
                    self.entryPasswordRegister.delete(0, END)
                    self.entryConfirmPassword.delete(0, END)
                    self.entryPasswordRegister.config(background="orange")
                    self.entryConfirmPassword.config(background="orange")
                    messagebox.showwarning("Error", message="Passwords do not match. Please Try Again.")
            else:
                self.entryAuthenCodes.delete(0, END)
                messagebox.showwarning("Error", message="Authentication code is invalid. Please Try Again.")
                self.entryAuthenCodes.config(background="orange")
        else:
            messagebox.showwarning("Warning", message=warn_mess)

    def loginVerify(self):
        allUser, allPass = Database.getUserPass()
        userIDdetail = self.userIDLogin.get()
        passwordDetail = self.passwordLogin.get()

        self.entryUserIDLogin.delete(0, END)
        self.entryPasswordLogin.delete(0, END)

        if userIDdetail in allUser:
            if passwordDetail in allPass:
                CurrentNameDetails = self.getUserName(userIDdetail)
                with open('currentUser.txt', 'w') as f:
                    f.write(CurrentNameDetails)
                messagebox.showinfo("Congratulations", message="Login Successful")
                self.loginScreem.destroy()
                self.mainScreen.destroy()
                Menu.menuSelection()

            else:
                messagebox.showwarning("Error", message="Invalid Password")
        else:
            messagebox.showwarning("Error", message="Invalid UserID")

    def register(self):
        self.registerScreen = Toplevel(self.mainScreen)
        self.registerScreen.title("Sign Up")
        self.registerScreen.geometry("700x700")
        self.registerScreen.resizable(0, 0)
        self.registerScreen.config(bg="lightblue")

        title_label = Label(
            self.registerScreen,
            text="Register an account using valid credentials",
            bg="gray",
            width="400",
            height="2",
            font=("Arial", 16, "bold"),
        )
        title_label.pack()

        self.userIDRegister = StringVar()
        self.passwordRegister = StringVar()
        self.confirmPass = StringVar()
        self.firstname = StringVar()
        self.surname = StringVar()
        self.email = StringVar()
        self.code = StringVar()

        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="User ID", bg="lightblue", font=("Arial", 14)).pack()
        self.entryUserIDREgister = Entry(self.registerScreen, textvariable=self.userIDRegister, bg="white", fg="black")
        self.entryUserIDREgister.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="Password", bg="lightblue", font=("Arial", 14)).pack()
        self.entryPasswordRegister = Entry(self.registerScreen, textvariable=self.passwordRegister, show='*',
                                           bg="white", fg="black")
        self.entryPasswordRegister.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="Confirm Password", bg="lightblue", font=("Arial", 14)).pack()
        self.entryConfirmPassword = Entry(self.registerScreen, textvariable=self.confirmPass, show='*',
                                           bg="white", fg="black")
        self.entryConfirmPassword.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="firstname", bg="lightblue", font=("Arial", 14)).pack()
        self.entryFirstname = Entry(self.registerScreen, textvariable=self.firstname, bg="white", fg="black")
        self.entryFirstname.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="Surname", bg="lightblue", font=("Arial", 14)).pack()
        self.entrySurname = Entry(self.registerScreen, textvariable=self.surname, bg="white", fg="black")
        self.entrySurname.pack()
        Label(self.registerScreen, bg="lightblue", height="1", font=("Arial", 14)).pack()

        Label(self.registerScreen, text="Email", bg="lightblue", font=("Arial", 14)).pack()
        self.entryEmail = Entry(self.registerScreen, textvariable=self.email, bg="white", fg="black")
        self.entryEmail.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        Label(self.registerScreen, text="Authentication Code", bg="lightblue", font=("Arial", 14)).pack()
        self.entryAuthenCodes = Entry(self.registerScreen, textvariable=self.code, show='*', bg="white", fg="black")
        self.entryAuthenCodes.pack()
        Label(self.registerScreen, bg="lightblue", height="1").pack()

        register_button = Button(
            self.registerScreen,
            text="Sign Up",
            height="3",
            bg="orange",
            font=("Arial", 12, "bold"),
            command=self.registerVerify,
        )
        register_button.pack()

        exit_button = Button(
            self.registerScreen,
            text="Exit",
            height="3",
            bg="red",
            font=("Arial", 12, "bold"),
            command=self.registerScreen.destroy,
        )
        exit_button.pack()

        self.registerScreen.mainloop()

    def logIn(self):
        self.loginScreem = Toplevel(self.mainScreen)
        self.loginScreem.title("Login")
        self.loginScreem.geometry("350x300")
        self.loginScreem.resizable(0, 0)
        self.loginScreem.config(bg="lightblue")

        title_label = Label(
            self.loginScreem,
            text="Please Login using your valid credentials",
            bg="gray",
            width="400",
            height="2",
            font=("Arial", 16, "bold"),
        )
        title_label.pack()

        self.userIDLogin = StringVar()
        self.passwordLogin = StringVar()

        Label(self.loginScreem, text="User ID", bg="lightblue", font=("Arial", 14)).pack()
        self.entryUserIDLogin = Entry(self.loginScreem, textvariable=self.userIDLogin, bg="white", fg="black")
        self.entryUserIDLogin.pack()
        Label(self.loginScreem, bg="lightblue", height="1").pack()

        Label(self.loginScreem, text="Password", bg="lightblue", font=("Arial", 14)).pack()
        self.entryPasswordLogin = Entry(self.loginScreem, textvariable=self.passwordLogin, show='*', bg="white",
                                        fg="black")
        self.entryPasswordLogin.pack()
        Label(self.loginScreem, bg="lightblue", height="1").pack()

        login_button = Button(
            self.loginScreem,
            text="Login",
            height="3",
            bg="green",
            font=("Arial", 12, "bold"),
            command=self.loginVerify,
        )
        login_button.pack()

        exit_button = Button(
            self.loginScreem,
            text="Exit",
            height="3",
            bg="red",
            font=("Arial", 12, "bold"),
            command=self.loginScreem.destroy,
        )
        exit_button.pack()

        self.loginScreem.mainloop()

    def main(self):
        self.mainScreen = Tk()
        self.mainScreen.geometry("500x400")
        self.mainScreen.resizable(0, 0)
        self.mainScreen.title("SignLanguageTranslator")
        self.mainScreen.config(bg="lightblue")

        title_label = Label(
            self.mainScreen,
            text="Welcome To Sign Language Translation System",
            bg="gray",
            width="400",
            height="2",
            font=("Arial", 16, "bold"),
        )
        title_label.pack()

        spacer = Label(bg="lightblue", height="2")
        spacer.pack()

        login_button = Button(
            self.mainScreen,
            text="Login",
            width="40",
            height="3",
            bg="green",
            font=("Arial", 12, "bold"),
            command=self.logIn,
        )
        login_button.pack()

        spacer = Label(bg="lightblue", height="1")
        spacer.pack()

        register_button = Button(
            self.mainScreen,
            text="Sign up",
            width="40",
            height="3",
            bg="orange",
            font=("Arial", 12, "bold"),
            command=self.register,
        )
        register_button.pack()

        spacer = Label(bg="lightblue", height="1")
        spacer.pack()

        exit_button = Button(
            self.mainScreen,
            text="Exit",
            width="40",
            height="3",
            bg="red",
            font=("Arial", 12, "bold"),
            command=exit,
        )
        exit_button.pack()

        self.mainScreen.mainloop()

if __name__ == "__main__":
    application = SignLanguageTranslatorApp()
    application.main()
