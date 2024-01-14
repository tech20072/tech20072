# user_management_window.py
import tkinter as tk
from tkinter import ttk, messagebox

class UserManagementWindow(tk.Toplevel):
    def __init__(self, user_access, save_callback):
        super().__init__()

        self.title("Gestion des Utilisateurs")
        self.geometry("400x300")

        self.user_access = user_access
        self.save_callback = save_callback

        # Create widgets for user management
        self.label_username = tk.Label(self, text="Nom d'utilisateur:")
        self.label_username.grid(row=0, column=0, pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1, pady=10)

        self.label_password = tk.Label(self, text="Mot de passe:")
        self.label_password.grid(row=1, column=0, pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, pady=10)

        self.label_access = tk.Label(self, text="Niveau d'accès:")
        self.label_access.grid(row=2, column=0, pady=10)
        self.combo_access = ttk.Combobox(self, values=["Admin", "User"])
        self.combo_access.grid(row=2, column=1, pady=10)

        self.button_add_user = tk.Button(self, text="Ajouter Utilisateur", command=self.add_user)
        self.button_add_user.grid(row=3, column=0, columnspan=2, pady=10)

    def add_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        access_level = self.combo_access.get()

        if not username or not password or not access_level:
            messagebox.showinfo("Erreur", "Veuillez remplir tous les champs.")
            return

        if username in self.user_access:
            messagebox.showinfo("Erreur", "Nom d'utilisateur déjà existant.")
            return

        self.user_access[username] = {"password": password, "access": access_level}
        self.save_callback()

        messagebox.showinfo("Succès", f"Utilisateur {username} ajouté avec succès.")
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_access.set("")