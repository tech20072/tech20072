# login_window.py
import tkinter as tk
from tkinter import messagebox
from gestion_scolaire_app import GestionScolaireApp

class LoginWindow(tk.Tk):
    def __init__(self, verify_user):
        super().__init__()

        self.verify_user = verify_user

        self.title("Login")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.verify_user(username, password):
            self.destroy()  # Fermer la fenêtre de connexion
            app = GestionScolaireApp(username)
            app.mainloop()
        else:
            messagebox.showinfo("Login Failed", "Invalid username or password.")