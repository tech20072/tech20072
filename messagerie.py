import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import socket
import json
from sqlalchemy import or_
from user_management_window import UserManagementWindow
from database import *
from tkinter import filedialog
from reportlab.pdfgen import canvas
from tkcalendar import DateEntry
from sqlalchemy.orm import joinedload



def envoyer_message(self):
    self.label_destinataire = tk.Label(self.menu_options_frame, text="Destinataire:")
    self.label_destinataire.grid(row=11, column=0, pady=5)
    self.entry_destinataire = tk.Entry(self.menu_options_frame)
    self.entry_destinataire.grid(row=11, column=1, pady=5)

    self.label_message = tk.Label(self.menu_options_frame, text="Message:")
    self.label_message.grid(row=12, column=0, pady=5)
    self.text_message = tk.Text(self.menu_options_frame, height=5, width=30)
    self.text_message.grid(row=12, column=1, pady=5)

    self.button_envoyer_message = tk.Button(self.menu_options_frame, text="Envoyer Message",
                                            command=self.envoyer_message)
    self.button_envoyer_message.grid(row=13, column=0, columnspan=2, pady=10)

    # Stockage des messages en mémoire
    self.messages = []

    # Démarrer un thread pour écouter les messages entrants
    self.server_thread = threading.Thread(target=self.demarrer_serveur_messages)
    self.server_thread.daemon = True

    self.server_thread.start()

    destinataire = self.entry_destinataire.get()
    contenu = self.text_message.get("1.0", tk.END).strip()

    if not destinataire or not contenu:
        tk.messagebox.showinfo("Erreur", "Veuillez remplir le destinataire et le contenu du message.")
        return

    # Enregistrez le message en mémoire
    message = {"expediteur": "Vous", "destinataire": destinataire, "contenu": contenu}
    self.messages.append(message)

    # Envoyez le message au destinataire
    self.envoyer_message_reseau(destinataire, contenu)

    tk.messagebox.showinfo("Succès", "Message envoyé avec succès.")


def demarrer_serveur_messages(self):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))  # Utilisez un port approprié
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=self.gerer_message_entree, args=(client_socket,)).start()


def gerer_message_entree(self, client_socket):
    try:
        message_entree = client_socket.recv(1024).decode("utf-8")
        expediteur, contenu = message_entree.split(":")

        # Enregistrez le message en mémoire
        message = {"expediteur": expediteur, "destinataire": "Vous", "contenu": contenu}
        self.messages.append(message)

        # Mettez à jour l'interface utilisateur pour afficher le nouveau message
        self.afficher_messages()

    except Exception as e:
        print(f"Erreur lors de la gestion du message entrant: {e}")
    finally:
        client_socket.close()


def afficher_messages(self):
    message_text = "\n".join([f"{message['expediteur']}: {message['contenu']}" for message in self.messages])
    self.text_liste_eleves.config(state=tk.NORMAL)
    self.text_liste_eleves.delete(1.0, tk.END)
    self.text_liste_eleves.insert(tk.END, message_text)
    self.text_liste_eleves.config(state=tk.DISABLED)

def envoyer_message_reseau(destinataire, contenu):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((destinataire, 12345))  # Utilisez le port approprié

        message_sortie = f"Vous:{contenu}"
        client_socket.send(message_sortie.encode("utf-8"))

    except Exception as e:
        tk.messagebox.showinfo("Erreur", f"Erreur lors de l'envoi du message: {e}")

    finally:
        client_socket.close()



    def afficher_messages_envoyes(self):
        self.afficher_messages_utilisateur("envoyes")

    def afficher_messages_recus(self):
        self.afficher_messages_utilisateur("recus")

    def afficher_messages_utilisateur(self, type_messages):
        # Effacez le contenu précédent du main panel
        for widget in self.main_content_label.winfo_children():
            widget.destroy()

        # Récupérez les messages de la liste en mémoire en fonction du type de messages
        messages = self.get_messages_utilisateur(type_messages)

        if not messages:
            label_message = tk.Label(self.main_content_label, text=f"Aucun message {type_messages}.")
            label_message.pack(pady=20)
        else:
            # Affichez les messages dans le main panel
            for message in messages:
                label_message = tk.Label(self.main_content_label, text=message)
                label_message.pack()

    def get_messages_utilisateur(self, type_messages):
        expediteurs = set()
        destinataires = set()

        # Récupérez les expéditeurs et destinataires des messages
        for message in self.messages:
            expediteur = message["expediteur"]
            destinataire = message["destinataire"]

            expediteurs.add(expediteur)
            destinataires.add(destinataire)

        if type_messages == "envoyes":
            return list(expediteurs)
        elif type_messages == "recus":
            return list(destinataires)
        else:
            return []