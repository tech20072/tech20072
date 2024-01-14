# main.py
from login_window import LoginWindow
import json

def verify_user(username, password):
    try:
        with open("user_access.json", "r") as file:
            user_access = json.load(file)
    except FileNotFoundError:
        user_access = {}

    # Vérifiez l'utilisateur en fonction des données chargées
    if username in user_access and "password" in user_access[username] and user_access[username]["password"] == password:
        return True
    else:
        return False

# Créer et démarrer la fenêtre de connexion
login_window = LoginWindow(verify_user)
login_window.mainloop()