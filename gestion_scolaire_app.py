# gestion_scolaire_app.py
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


class GestionScolaireApp(tk.Tk):
    def __init__(self, username):
        super().__init__()

        # Load user access information from JSON file
        self.verify_user = None

        self.title("Gestion Scolaire")
        self.geometry("800x600")

        # Frame principale avec pack
        self.main_panel = tk.Frame(self, bg="#0f969c")
        self.main_panel.pack(side="left", fill="both", expand=True)

        # Frame du menu avec pack
        self.menu_panel = tk.Frame(self.main_panel, width=200, height=600, bg="#280a50")
        self.menu_panel.pack(side="left", fill="y")

        # Frame pour les options du menu à droite
        self.menu_options_frame = tk.Frame(self.main_panel, bg="#0f969c")
        self.menu_options_frame.pack(side="left", fill="both", expand=True)

        self.date_entry = None
        self.combo_classe = None
        self.critere_recherche = None
        self.info_recherche = None
        self.resultats = None
        self.annee_scolaire = None

        self.session = Session()
        self.create_menu_panel()


    def create_menu_panel(self):

        button_gestion_eleves = tk.Button(self.menu_panel, text="Gestion des Élèves",
                                          command=self.afficher_gestion_eleves)
        button_gestion_eleves.pack(pady=10, padx=5, fill=tk.X)

        button_gestion_finances = tk.Button(self.menu_panel, text="Gestion des Finances",
                                            command=self.afficher_gestion_finances)
        button_gestion_finances.pack(pady=10, padx=5, fill=tk.X)

        button_gestion_bulletins = tk.Button(self.menu_panel, text="Gestion des Bulletins",
                                             command=self.afficher_gestion_bulletins)
        button_gestion_bulletins.pack(pady=10, padx=5, fill=tk.X)

        button_messagerie = tk.Button(self.menu_panel, text="Messagerie",
                                      command=self.afficher_gestion_messagerie)
        button_messagerie.pack(pady=10, padx=5, fill=tk.X)

        button_gestion_utilisateur = tk.Button(self.menu_panel, text="Gestion des Utilisateurs",
                                               command=self.afficher_gestion_utilisateur)
        button_gestion_utilisateur.pack(pady=10, padx=5, fill=tk.X)

        button_configuration = tk.Button(self.menu_panel, text="Configuration",
                                         command=self.afficher_configuration)
        button_configuration.pack(pady=10, padx=5, fill=tk.X)

    def afficher_gestion_messagerie(self):
        self.afficher_contenu_menu("Messagerie")

    def afficher_gestion_finances(self):
        self.afficher_contenu_menu("Finances")

    def afficher_gestion_eleves(self):
        self.afficher_contenu_menu("Élèves")

    def afficher_gestion_bulletins(self):
        self.afficher_contenu_menu("Bulletins")

    def afficher_gestion_utilisateur(self):
        self.afficher_contenu_menu("User_management")

    def afficher_configuration(self):
        self.afficher_contenu_menu("Configuration")

    def afficher_contenu_menu(self, menu):
        for widget in self.menu_options_frame.winfo_children():
            widget.destroy()

        if menu == "Messagerie":
            self.show_messagerie_menu()
        elif menu == "Finances":
            self.show_finance_menu()
        elif menu == "Élèves":
            self.show_eleves_menu()
        elif menu == "Bulletins":
            self.show_bulletins_menu()
        elif menu == "User_management":
            self.show_user_management_menu()
        elif menu == "Configuration":
            self.show_configuration_menu()

    def show_eleves_menu(self):

        bouton_ajouter_eleve = tk.Button(self.menu_options_frame, text="Ajouter un élève",
                                         command=self.ajouter_eleve)
        bouton_ajouter_eleve.pack(pady=10, padx=5, fill=tk.X)

        bouton_supprimer_eleve = tk.Button(self.menu_options_frame, text="Supprimer un élève",
                                           command=self.supprimer_eleve)
        bouton_supprimer_eleve.pack(pady=10, padx=5, fill=tk.X)

        bouton_rechercher_eleve = tk.Button(self.menu_options_frame, text="Rechercher un élève",
                                            command=self.rechercher_eleve)
        bouton_rechercher_eleve.pack(pady=10, padx=5, fill=tk.X)

        bouton_gestion_quantite = tk.Button(self.menu_options_frame, text="Gérer la quantité d'élèves",
                                            command=self.gerer_quantite)
        bouton_gestion_quantite.pack(pady=10, padx=5, fill=tk.X)

        bouton_modifier_eleve = tk.Button(self.menu_options_frame, text="Modifier un élève",
                                          command=self.modifier_eleve)
        bouton_modifier_eleve.pack(pady=10, padx=5, fill=tk.X)

        bouton_inscrire_eleve = tk.Button(self.menu_options_frame, text="Inscrire un élève",
                                          command=self.inscrire_eleve)
        bouton_inscrire_eleve.pack(pady=10, padx=5, fill=tk.X)

        bouton_mettre_a_la_porte = tk.Button(self.menu_options_frame, text="Mettre à la porte",
                                             command=self.mettre_a_la_porte)
        bouton_mettre_a_la_porte.pack(pady=10, padx=5, fill=tk.X)

    def show_finance_menu(self):

        button_rapport_paiement = tk.Button(self.menu_options_frame, text="Rapport de Paiement",
                                                 command=FinancialsManagement.generer_rapport_paiement)
        button_rapport_paiement.grid(row=11, column=0, columnspan=3, pady=10)

        button_rapport_paiement_eleve = tk.Button(self.menu_options_frame, text="Rapport de Paiement pour un Élève",
                                                  command=FinancialsManagement.generer_rapport_paiement_eleve)
        button_rapport_paiement_eleve.grid(row=12, column=0, columnspan=3, pady=10)

    def show_bulletins_menu(self):

        bouton_ajouter_notes = tk.Button(self.menu_options_frame, text="Ajouter Notes",
                                         command=self.ajouter_note)
        bouton_ajouter_notes.pack(pady=10, padx=5, fill=tk.X)

        bouton_supprimer_notes = tk.Button(self.menu_options_frame, text="Supprimer Notes",
                                           command=self.supprimer_note)
        bouton_supprimer_notes.pack(pady=10, padx=5, fill=tk.X)

        bouton_modifier_notes = tk.Button(self.menu_options_frame, text="Modifier Notes",
                                          command=self.modifier_note)
        bouton_modifier_notes.pack(pady=10, padx=5, fill=tk.X)

        bouton_rechercher_bultin = tk.Button(self.menu_options_frame, text="Rechercher un bultin",
                                             command=self.rechercher_bultin)
        bouton_rechercher_bultin.pack(pady=10, padx=5, fill=tk.X)

        bouton_imprimer_palmareste = tk.Button(self.menu_options_frame, text="Impression du Palmareste",
                                               command=self.imprimmer_palmareste)
        bouton_imprimer_palmareste.pack(pady=10, padx=5, fill=tk.X)

        bouton_imprimer_bultin = tk.Button(self.menu_options_frame, text="Impression du Bulletin",
                                           command=self.imprimer_bultin)
        bouton_imprimer_bultin.pack(pady=10, padx=5, fill=tk.X)

        bouton_configurer_matiere = tk.Button(self.menu_options_frame, text="Configuration Des Matieres",
                                              command=self.configurer_matiere)
        bouton_configurer_matiere.pack(pady=10, padx=5, fill=tk.X)

        bouton_configurer_bultin = tk.Button(self.menu_options_frame, text="Configuration Des Bulletins",
                                             command=self.configurer_bultin)
        bouton_configurer_bultin.pack(pady=10, padx=5, fill=tk.X)

    def show_messagerie_menu(self):

        button_messages_envoyes = tk.Button(self.menu_options_frame, text="Messages Envoyés",
                                            command=MessageriesManagement.afficher_messages_envoyes)
        button_messages_envoyes.pack(pady=10, padx=5, fill=tk.X)

        button_messages_recus = tk.Button(self.menu_options_frame, text="Messages Reçus",
                                          command=MessageriesManagement.afficher_messages_recus)
        button_messages_recus.pack(pady=10, padx=5, fill=tk.X)

    def show_user_management_menu(self):

        button_ajouter_utilisateur = tk.Button(self.menu_options_frame, text="Ajouter Utilisateur",
                                               command=UsersManagement.ajouter_utilisateur)
        button_ajouter_utilisateur.pack(pady=10, padx=5, fill=tk.X)

        button_supprimer_utilisateur = tk.Button(self.menu_options_frame, text="Supprimer Utilisateur",
                                                 command=UsersManagement.supprimer_utilisateur)
        button_supprimer_utilisateur.pack(pady=10, padx=5, fill=tk.X)

        button_modifier_utilisateur = tk.Button(self.menu_options_frame, text="Modifier Utilisateur",
                                                command=UsersManagement.modifier_utilisateur)
        button_modifier_utilisateur.pack(pady=10, padx=5, fill=tk.X)

        button_rechercher_utilisateur = tk.Button(self.menu_options_frame, text="Rechercher Utilisateur",
                                                  command=UsersManagement.rechercher_utilisateur)
        button_rechercher_utilisateur.pack(pady=10, padx=5, fill=tk.X)

    def show_configuration_menu(self):

        button_modifier_db_config = tk.Button(self.menu_options_frame, text="Modifier Config. BD",
                                              command=ConfigurationsManagement.modifier_config_bd)
        button_modifier_db_config.pack(pady=10, padx=5, fill=tk.X)

        button_annee_scolaire = tk.Button(self.menu_options_frame, text="Modifier Année Scolaire",
                                          command=ConfigurationsManagement.modifier_annee_scolaire)
        button_annee_scolaire.pack(pady=10, padx=5, fill=tk.X)

        button_ajouter_classe = tk.Button(self.menu_options_frame, text="Ajouter Classe",
                                          command=ConfigurationsManagement.ajouter_classe)
        button_ajouter_classe.pack(pady=10, padx=5, fill=tk.X)



    def ajouter_eleve(self):
        for widget in self.menu_options_frame.winfo_children():
            widget.destroy()

        self.label_photo_path = tk.Label(self.menu_options_frame, text="")
        self.label_photo_path.grid(row=7, column=1, padx=10, pady=5)

        # Logique pour ajouter un élève
        self.label_annee = tk.Label(self.menu_options_frame, text="Année Scolaire:")
        self.label_annee.grid(row=0, column=0, pady=5)

        # Utilisez un ttk.Combobox pour afficher les années scolaires disponibles
        self.combo_annee = ttk.Combobox(self.menu_options_frame, values=self.get_annees_scolaires())
        self.combo_annee.grid(row=0, column=1, pady=5)

        self.label_nom = tk.Label(self.menu_options_frame, text="Nom:")
        self.label_nom.grid(row=1, column=0, pady=5)
        self.entry_nom = tk.Entry(self.menu_options_frame)
        self.entry_nom.grid(row=1, column=1, pady=5)

        self.label_prenom = tk.Label(self.menu_options_frame, text="Prénom:")
        self.label_prenom.grid(row=2, column=0, pady=5)
        self.entry_prenom = tk.Entry(self.menu_options_frame)
        self.entry_prenom.grid(row=2, column=1, pady=5)

        self.label_photo = tk.Label(self.menu_options_frame, text="Photo d'Identité:")
        self.label_photo.grid(row=3, column=0, pady=5)
        self.photo_button = tk.Button(self.menu_options_frame, text="Choisir la photo", command=self.choisir_photo)
        self.photo_button.grid(row=3, column=1, pady=5)

        self.label_sexe = tk.Label(self.menu_options_frame, text="Sexe:")
        self.label_sexe.grid(row=4, column=0, pady=5)

        # Utilisez un ttk.Combobox pour choisir le sexe de l'élève
        self.combo_sexe = ttk.Combobox(self.menu_options_frame, values=["male", "female"])
        self.combo_sexe.grid(row=4, column=1, pady=5)

        self.label_date_naissance = tk.Label(self.menu_options_frame, text="Date de Naissance:")
        self.label_date_naissance.grid(row=5, column=0, pady=5)
        self.entry_date_naissance = DateEntry(self.menu_options_frame, date_pattern="yyyy-mm-dd")
        self.entry_date_naissance.grid(row=5, column=1, pady=5)

        self.label_classe = tk.Label(self.menu_options_frame, text="Classe:")
        self.label_classe.grid(row=6, column=0, pady=5)
        self.combo_classe = ttk.Combobox(self.menu_options_frame, values=self.get_classes())
        self.combo_classe.grid(row=6, column=1, pady=5)

        self.button_ajouter = tk.Button(self.menu_options_frame, text="Ajouter Élève", command=self.ajouter_infos_eleve)
        self.button_ajouter.grid(row=7, column=0, columnspan=2, pady=10)

    def ajouter_infos_eleve(self):

        # Lire la photo en tant que données binaires à partir du fichier image
        with open(self.label_photo_path.cget("text"), 'rb') as file:
            photo_data = file.read()

        session = Session()

        date_naissance = self.entry_date_naissance.get()
        sexe = self.combo_sexe.get()

        # Utilisez la valeur sélectionnée dans le ttk.Combobox pour récupérer l'ID de l'année scolaire
        annee_scolaire = session.query(AnneeScolaire).filter_by(Annee_Scolaire=self.combo_annee.get()).first()

        # Ajoutez la logique pour déterminer la section en fonction de la classe sélectionnée
        classe_selected = self.combo_classe.get()
        section_name = "Primaire" if classe_selected.startswith(("1", "2", "3", "4", "5", "6")) else "Secondaire"

        # Vérifiez si la section existe déjà, sinon ajoutez-la à la base de données
        section = session.query(Section).filter_by(Nom_Section=section_name).first()
        if section is None:
            section = Section(Nom_Section=section_name)
            session.add(section)

        # Ajoutez la logique pour déterminer l'année scolaire en fonction de la valeur de self.combo_annee
        if annee_scolaire is None:
            # Ajoutez la logique pour déterminer le statut en fonction de la date actuelle ou d'autres critères
            statut = "En cours"  # Remplacez cette logique par la vôtre
            annee_scolaire = AnneeScolaire(Annee_Scolaire=self.combo_annee.get(), Statut=statut)
            session.add(annee_scolaire)

        # Ajoutez la logique pour déterminer la classe en fonction de la valeur de self.combo_classe
        classe = session.query(Classe).filter_by(Nom_Classe=classe_selected, section=section).first()
        if classe is None:
            classe = Classe(Nom_Classe=classe_selected, section=section)
            session.add(classe)

        eleve = Eleve(
            Nom=self.entry_nom.get(),
            Prenom=self.entry_prenom.get(),
            Date_Naissance=date_naissance,
            Photo_Identite=photo_data,
            Sexe=sexe,
            Annee_ID=annee_scolaire.ID_Annee,  # Utilisez la clé étrangère Annee_ID
            Classe_ID=classe.ID_Classe  # Utilisez la clé étrangère Classe_ID
        )

        session.add(eleve)
        session.commit()

        tk.messagebox.showinfo("Succès", "Élève ajouté avec succès.")

    def get_classes(self):
        session = Session()
        classes = session.query(Classe).all()
        return [classe.Nom_Classe for classe in classes]

    """def get_annes_scolaires(self):
        session = Session()
        annees = session.query(AnneeScolaire).all()
        return [str(annee.Annee_Scolaire) for annee in annees]"""

    def afficher_liste_eleves(self, event):
        selected_annee = self.combo_annee.get()

        if not selected_annee:
            tk.messagebox.showinfo("Erreur", "Veuillez sélectionner une année scolaire.")
            return

        session = Session()
        annee_scolaire = session.query(AnneeScolaire).filter_by(Annee_Scolaire=selected_annee).first()

        if annee_scolaire is None:
            tk.messagebox.showinfo("Erreur", "Année scolaire non trouvée.")
            return

        eleves = session.query(Eleve).filter_by(Annee=annee_scolaire).all()

        self.text_liste_eleves.delete(1.0, tk.END)
        for eleve in eleves:
            self.text_liste_eleves.insert(tk.END, f"{eleve.Nom} {eleve.Prenom}\n")



    def choisir_photo(self):
        # Ouvrir l'explorateur de fichiers pour choisir la photo
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        # Mettre à jour un label ou une autre interface utilisateur pour afficher le chemin du fichier choisi
        self.label_photo_path.config(text=file_path)

    def get_annees_scolaires(self):
        session = Session()
        annees_scolaires = session.query(AnneeScolaire.Annee_Scolaire).all()
        session.close()
        return [annee[0] for annee in annees_scolaires]

    """def get_annees_scolaires(self):
        session = Session()
        annees_scolaires = session.query(AnneeScolaire.Annee_Scolaire).all()
        session.close()
        return [annee[0] for annee in annees_scolaires]"""

    def supprimer_eleve(self):
        # Effacez le contenu précédent du main panel
        for widget in self.menu_options_frame.winfo_children():
            widget.destroy()

        # Ajoutez un champ de recherche pour rechercher un élève
        self.label_recherche = tk.Label(self.menu_options_frame, text="Rechercher un élève:")
        self.label_recherche.grid(row=0, column=0, pady=5)

        # Utilisez un ttk.Combobox pour choisir le critère de recherche
        critere_options = ["ID", "Nom", "Prénom", "Date de Naissance", "Classe"]
        self.combo_critere_recherche = ttk.Combobox(self.menu_options_frame, values=critere_options)
        self.combo_critere_recherche.grid(row=0, column=1, pady=5)
        self.combo_critere_recherche.bind("<<ComboboxSelected>>", self.on_critere_selection_change)

        # Ajoutez un champ d'entrée initial (entry ou dateentry selon le critère)
        self.create_champ_entree("")

        # Ajoutez un bouton pour lancer la recherche et la suppression
        self.button_rechercher_supprimer = tk.Button(self.menu_options_frame, text="Rechercher et Supprimer",
                                                     command=self.rechercher_et_supprimer_eleve)
        self.button_rechercher_supprimer.grid(row=0, column=3, pady=5)

    def create_champ_entree(self, critere):
        # Détruisez le champ d'entrée actuel s'il existe
        if hasattr(self, 'entry_info_recherche'):
            self.entry_info_recherche.destroy()

        # Utilisez un ttk.Combobox avec autocomplétion pour les critères ID, Nom, et Prénom
        if critere in ["ID", "Nom", "Prénom"]:
            self.entry_info_recherche = AutocompleteCombobox(self.menu_options_frame, width=20)
            self.entry_info_recherche.grid(row=0, column=2, pady=5)
            self.entry_info_recherche.set_completion_list(self.get_autocomplete_list(critere))
        # Utilisez DateEntry pour le critère Date de Naissance
        elif critere == "Date de Naissance":
            self.entry_info_recherche = DateEntry(self.menu_options_frame, width=12, background='darkblue',
                                                  foreground='white', borderwidth=2)
            self.entry_info_recherche.grid(row=0, column=2, pady=5)
        # Utilisez un ttk.Combobox pour le critère Classe
        elif critere == "Classe":
            classes = self.get_info_classes_from_database()  # Assurez-vous d'avoir cette fonction dans votre code
            self.entry_info_recherche = ttk.Combobox(self.menu_options_frame, values=classes)
            self.entry_info_recherche.grid(row=0, column=2, pady=5)
            self.combo_classe = self.entry_info_recherche  # Ajoutez cette ligne pour référencer le combo_classe
        else:
            self.entry_info_recherche = tk.Entry(self.menu_options_frame)
            self.entry_info_recherche.grid(row=0, column=2, pady=5)

    def on_critere_selection_change(self, event):
        selected_critere = self.combo_critere_recherche.get()
        self.create_champ_entree(selected_critere)

    def get_autocomplete_list(self, critere):
        autocomplete_list = ["Nom1", "Nom2", "Nom3"]
        return autocomplete_list

    def get_info_classes_from_database(self):
        # Connexion à la base de données
        engine = create_engine(DATABASE_URL, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Exécutez la requête pour obtenir la liste des classes depuis la base de données
        # Assurez-vous d'adapter cela à votre modèle de données réel
        classes_list = session.query(Classe.Nom_Classe).all()

        # Transformez la liste résultante en une liste simple
        classes_list = [classe[0] for classe in classes_list]

        return classes_list

    def update_champ_recherche(self, event):
        # Mettez à jour le champ de recherche en fonction du critère sélectionné
        critere_selectionne = self.combo_critere_recherche.get()

        if critere_selectionne == "Date de Naissance":
            self.entry_info_recherche.grid_remove()
            self.date_entry.grid()
            self.combo_classe.grid_remove()
        elif critere_selectionne == "Classe":
            self.entry_info_recherche.grid_remove()
            self.date_entry.grid_remove()
            self.combo_classe.grid()
        else:
            self.entry_info_recherche.grid()
            self.date_entry.grid_remove()
            self.combo_classe.grid_remove()

    def rechercher_et_supprimer_eleve(self):
        self.critere_recherche = self.combo_critere_recherche.get()
        self.info_recherche = ""

        if self.critere_recherche == "Date de Naissance":
            self.info_recherche = self.entry_info_recherche.get_date()  # Utilisez get_date() pour DateEntry
        elif self.critere_recherche == "Classe":
            self.info_recherche = self.entry_info_recherche.get()
        else:
            self.info_recherche = self.entry_info_recherche.get()

        if self.critere_recherche and self.info_recherche:
            # Connexion à la base de données
            engine = create_engine(DATABASE_URL, echo=False)
            Session = sessionmaker(bind=engine)
            self.session = Session()

            # Logique de recherche dans la base de données
            self.resultats = self.rechercher_eleve()

            # Afficher les résultats et permettre à l'utilisateur de cocher les élèves à supprimer
            if len(self.resultats) > 0:
                self.afficher_resultats()
            else:
                tk.messagebox.showinfo("Information", "Aucun élève trouvé.")
        else:
            tk.messagebox.showinfo("Erreur", "Veuillez entrer un critère de recherche et une information de recherche.")

    def rechercher_eleve(self):
        # Logique de recherche dans la base de données
        if self.critere_recherche == "Date de Naissance":
            return self.session.query(Eleve).filter_by(Date_Naissance=self.info_recherche).all()
        elif self.critere_recherche == "Classe":
            return self.session.query(Eleve).join(Classe).filter(Classe.Nom_Classe == self.info_recherche).all()
        else:
            # Recherche par nom ou prénom avec autocomplétion
            return self.session.query(Eleve).filter(
                or_(Eleve.Nom.ilike(f"%{self.info_recherche}%"), Eleve.Prenom.ilike(f"%{self.info_recherche}%"))).all()


    def afficher_resultats(self):
        # Créez une nouvelle fenêtre pour afficher les résultats
        self.fenetre_resultats = tk.Toplevel(self.master)
        self.fenetre_resultats.title("Résultats de la Recherche")

        # Ajoutez des cases à cocher pour chaque élève
        self.eleves_a_supprimer = []

        for eleve in self.resultats:
            var = tk.BooleanVar()
            # Utilisez les attributs corrects de l'objet Eleve (Nom et Prenom)
            checkbutton = tk.Checkbutton(self.fenetre_resultats, text=f"{eleve.Nom} {eleve.Prenom}", variable=var)
            checkbutton.eleve = eleve  # Attachez l'objet élève au checkbutton
            checkbutton.grid(sticky="w")
            self.eleves_a_supprimer.append((var, eleve))

        # Ajoutez un bouton pour confirmer la suppression des élèves sélectionnés
        bouton_confirmer_suppression = tk.Button(self.fenetre_resultats, text="Confirmer Suppression",
                                                 command=self.confirmer_suppression_multiple)
        bouton_confirmer_suppression.grid()


    def confirmer_suppression_multiple(self):
        # Implémentez la logique de suppression pour les élèves cochés
        eleves_supprimes = [eleve for var, eleve in self.eleves_a_supprimer if var.get()]

        if eleves_supprimes:
            for eleve in eleves_supprimes:
                # Implémentez la suppression de l'élève de la base de données
                # Utilisez eleve.id pour identifier l'élève à supprimer
                pass

            tk.messagebox.showinfo("Succès", f"{len(eleves_supprimes)} élève(s) supprimé(s) avec succès.")
            self.fenetre_resultats.destroy()
        else:
            tk.messagebox.showinfo("Information", "Aucun élève sélectionné.")
            self.fenetre_resultats.destroy()

    def rechercher_info_eleve(self):
        # Logique pour rechercher un élève
        tk.messagebox.showinfo("Rechercher des Eleves", "Fonctionnalité non implémentée.")

    def gerer_quantite(self):
        # Logique pour gérer la quantité d'élèves dans une classe
        tk.messagebox.showinfo("Gerer la Quantite d Eleve", "Fonctionnalité non implémentée.")

    def modifier_eleve(self):
        # Logique pour modifier un élève
        tk.messagebox.showinfo("Modifier Caracteristique Eleve", "Fonctionnalité non implémentée.")

    def inscrire_eleve(self):
        # Logique pour inscrire un élève dans l'établissement
        tk.messagebox.showinfo("Inscrire Un Eleve", "Fonctionnalité non implémentée.")

    def mettre_a_la_porte(self):
        # Logique pour mettre un élève à la porte
        tk.messagebox.showinfo("Mettre a la Porte un Eleve", "Fonctionnalité non implémentée.")



    def ajouter_note_examen(self):
        session = Session()
        eleve = session.query(Eleve).filter_by(Nom=self.entry_nom.get(), Prenom=self.entry_prenom.get()).first()
        matiere = session.query(Matiere).filter_by(Nom_Matiere=self.combo_matiere.get()).first()

        if eleve is None or matiere is None:
            tk.messagebox.showinfo("Erreur", "Élève ou matière non trouvée.")
            return

        note = Note(
            eleve=eleve,
            matiere=matiere,
            Note=float(self.entry_note_examen.get()),
            ID_Annee=eleve.ID_Annee
        )
        session.add(note)
        session.commit()

        tk.messagebox.showinfo("Succès", "Note d'examen ajoutée avec succès.")

    def calculer_moyenne(self):
        session = Session()
        eleve = session.query(Eleve).filter_by(Nom=self.entry_nom.get(), Prenom=self.entry_prenom.get()).first()

        if eleve is None:
            tk.messagebox.showinfo("Erreur", "Élève non trouvé.")
            return

        notes = session.query(Note).filter_by(ID_Eleve=eleve.ID_Eleve).all()

        if not notes:
            tk.messagebox.showinfo("Erreur", "Aucune note trouvée pour cet élève.")
            return

        total_notes = 0
        nombre_matieres = 0

        for note in notes:
            total_notes += note.Note
            nombre_matieres += 1

        moyenne = total_notes / nombre_matieres

        tk.messagebox.showinfo("Moyenne", f"Moyenne de l'élève: {moyenne:.2f}")

    def creer_bulletin(self):
        session = Session()
        eleve = session.query(Eleve).filter_by(Nom=self.entry_nom.get(), Prenom=self.entry_prenom.get()).first()

        if eleve is None:
            tk.messagebox.showinfo("Erreur", "Élève non trouvé.")
            return

        bulletins = session.query(Bulletin).filter_by(ID_Eleve=eleve.ID_Eleve).all()

        if not bulletins:
            tk.messagebox.showinfo("Erreur", "Aucun bulletin trouvé pour cet élève.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf = canvas.Canvas(file_path)
            pdf.drawString(100, 800, f"BULLETIN DE {eleve.Nom} {eleve.Prenom}")
            pdf.drawString(100, 780, "Notes d'Examens:")

            for bulletin in bulletins:
                examen = session.query(Examen).get(bulletin.ID_Examen)
                if examen:
                    matiere = session.query(Matiere).get(examen.ID_Matiere)
                    pdf.drawString(120, 760, f"{matiere.Nom_Matiere}: {bulletin.Note_Examen}")

            pdf.save()
            tk.messagebox.showinfo("Succès", "Bulletin créé et enregistré avec succès.")
            
    def get_matieres(self):
        session = Session()
        matieres = session.query(Matiere).all()
        return [matiere.Nom_Matiere for matiere in matieres]
    
    def rechercher_eleve(self):
        session = Session()
        nom_prenom = self.entry_recherche.get()

        if not nom_prenom:
            tk.messagebox.showinfo("Erreur", "Veuillez entrer le nom ou prénom de l'élève.")
            return

        eleves = session.query(Eleve).filter(or_(Eleve.Nom.ilike(f"%{nom_prenom}%"), Eleve.Prenom.ilike(f"%{nom_prenom}%"))).all()

        if not eleves:
            tk.messagebox.showinfo("Information", "Aucun élève trouvé.")
            return

        result = "Résultats de la recherche:\n"
        for eleve in eleves:
            result += f"{eleve.Nom} {eleve.Prenom}\n"

        tk.messagebox.showinfo("Résultats", result)



    def ajouter_note(self):
        # Effacez le contenu précédent du main panel
        for widget in self.menu_options_frame.winfo_children():
            widget.destroy()

        # Ajout de la Combobox pour l'année scolaire
        self.label_annee_scolaire = tk.Label(self.menu_options_frame, text="Année Scolaire:")
        self.label_annee_scolaire.grid(row=0, column=0, pady=5)
        self.combo_annee_scolaire = ttk.Combobox(self.menu_options_frame, values=self.get_annees_scolaires())
        self.combo_annee_scolaire.grid(row=0, column=1, pady=5)
        self.combo_annee_scolaire.bind("<<ComboboxSelected>>", self.on_annee_scolaire_selection_change)

        # Ajout de la Combobox pour les contrôles
        self.label_controle = tk.Label(self.menu_options_frame, text="Contrôle:")
        self.label_controle.grid(row=1, column=0, pady=5)
        self.combo_controle = ttk.Combobox(self.menu_options_frame)
        self.combo_controle.grid(row=1, column=1, pady=5)

        # Ajout de la Combobox pour la classe
        self.label_classe = tk.Label(self.menu_options_frame, text="Classe:")
        self.label_classe.grid(row=2, column=0, pady=5)
        self.combo_classe = ttk.Combobox(self.menu_options_frame, values=self.get_classes_in_database())
        self.combo_classe.grid(row=2, column=1, pady=5)
        self.combo_classe.bind("<<ComboboxSelected>>", self.on_classe_selection_change)

        # Ajout de la Combobox pour le fillière (si plusieurs fillières dans la classe)
        self.label_filliere = tk.Label(self.menu_options_frame, text="Filière:")
        self.label_filliere.grid(row=3, column=0, pady=5)
        self.combo_filliere = ttk.Combobox(self.menu_options_frame)
        self.combo_filliere.grid(row=3, column=1, pady=5)

        # Ajout de la Combobox pour la matière
        self.label_matiere = tk.Label(self.menu_options_frame, text="Matière:")
        self.label_matiere.grid(row=4, column=0, pady=5)
        self.combo_matiere = ttk.Combobox(self.menu_options_frame)
        self.combo_matiere.grid(row=4, column=1, pady=5)

        # Ajout de la Liste des élèves et des champs de notes
        self.label_eleves_notes = tk.Label(self.menu_options_frame, text="Liste des élèves et notes:")
        self.label_eleves_notes.grid(row=5, column=0, pady=5)

        self.eleves_notes_frame = tk.Frame(self.menu_options_frame)
        self.eleves_notes_frame.grid(row=6, column=0, columnspan=2, pady=5)

        self.scrollbar_eleves_notes = tk.Scrollbar(self.eleves_notes_frame, orient="vertical")
        self.listbox_eleves_notes = tk.Listbox(self.eleves_notes_frame, yscrollcommand=self.scrollbar_eleves_notes.set,
                                               selectmode=tk.SINGLE)
        self.scrollbar_eleves_notes.config(command=self.listbox_eleves_notes.yview)
        self.listbox_eleves_notes.pack(side="left", fill="both")
        self.scrollbar_eleves_notes.pack(side="right", fill="y")

        # Ajout du champ pour la note
        self.label_note = tk.Label(self.menu_options_frame, text="Note:")
        self.label_note.grid(row=7, column=0, pady=5)
        self.entry_note = tk.Entry(self.menu_options_frame)
        self.entry_note.grid(row=7, column=1, pady=5)

        # Bouton Sauvegarde
        self.button_sauvegarde = tk.Button(self.menu_options_frame, text="Sauvegarder",
                                           command=self.sauvegarder_notes)
        self.button_sauvegarde.grid(row=8, column=0, columnspan=2, pady=5)

    def on_annee_scolaire_selection_change(self, event):
        # Mettre à jour la Combobox des contrôles en fonction de l'année scolaire sélectionnée
        annee_scolaire = self.combo_annee_scolaire.get()
        # Vous devez implémenter la logique pour récupérer les contrôles en fonction de l'année scolaire
        # et les mettre à jour dans la Combobox
        controls = self.get_controls_for_annee_scolaire(annee_scolaire)
        self.combo_controle['values'] = controls

    def on_classe_selection_change(self, event):
        # Mettre à jour la Combobox de la filière (si nécessaire) et la Combobox de la matière
        classe = self.combo_classe.get()
        # Vous devez implémenter la logique pour récupérer les fillières de la classe
        fillieres = self.get_fillieres_for_classe(classe)
        self.combo_filliere['values'] = fillieres

        # Vous devez également implémenter la logique pour récupérer les matières en fonction de la classe
        matieres = self.get_matieres_for_classe(classe)
        self.combo_matiere['values'] = matieres

    def sauvegarder_notes(self):
        # Récupérer les valeurs sélectionnées dans les Combobox et le champ de note
        annee_scolaire = self.combo_annee_scolaire.get()
        controle = self.combo_controle.get()
        classe = self.combo_classe.get()
        filliere = self.combo_filliere.get()
        matiere = self.combo_matiere.get()
        note_value = float(self.entry_note.get())  # Assurez-vous que la valeur de la note est un nombre

        # Récupérer l'objet AnneeScolaire en fonction de l'année scolaire sélectionnée
        annee_obj = self.session.query(AnneeScolaire).filter_by(Annee_Scolaire=annee_scolaire).first()

        # Récupérer l'objet Controle en fonction du nom du contrôle sélectionné
        controle_obj = self.session.query(Controle).filter_by(Nom_Controle=controle).first()

        # Récupérer l'objet Classe en fonction du nom de la classe sélectionnée
        classe_obj = self.session.query(Classe).filter_by(Nom_Classe=classe).first()

        # Récupérer l'objet Matiere en fonction du nom de la matière sélectionnée
        matiere_obj = self.session.query(Matiere).filter_by(Nom_Matiere=matiere).first()

        # Si une filière est sélectionnée, récupérer l'objet Filiere correspondant
        if filliere:
            filiere_obj = self.session.query(Filiere).filter_by(Nom_Filiere=filliere).first()
        else:
            filiere_obj = None

        # Vérifier que toutes les informations nécessaires sont présentes
        if not all([annee_obj, controle_obj, classe_obj, matiere_obj]):
            messagebox.showerror("Erreur", "Veuillez sélectionner toutes les informations nécessaires.")
            return

        # Récupérer la liste des élèves pour la classe
        eleves_classe = (
            self.session.query(Eleve)
            .filter_by(Annee_ID=annee_obj.ID_Annee, Classe_ID=classe_obj.ID_Classe)
            .all()
        )

        # Ajouter une note pour chaque élève
        for eleve in eleves_classe:
            # Ajouter la logique pour récupérer l'ID de l'élève associé à cette note
            # Vous devrez adapter cette partie en fonction de votre modèle de données
            eleve_id = eleve.ID_Eleve

            # Ajouter la nouvelle note à la session et la sauvegarder dans la base de données
            new_note = Note(
                ID_Eleve=eleve_id,
                ID_Matiere=matiere_obj.ID_Matiere,
                ID_Annee=annee_obj.ID_Annee,
                ID_Controle=controle_obj.ID_Controle,
                # Ajouter d'autres colonnes de la table Note au besoin
            )

            # Ajouter la nouvelle note à la session et la sauvegarder dans la base de données
            self.session.add(new_note)

        # Committer les changements à la base de données
        self.session.commit()

        # Mettre à jour l'affichage ou effectuer d'autres actions nécessaires
        messagebox.showinfo("Succès", "Les notes ont été sauvegardées avec succès.")

    def get_controls_for_annee_scolaire(self, annee_scolaire):
        # Récupérer l'objet AnneeScolaire en fonction de l'année sélectionnée
        annee_obj = self.session.query(AnneeScolaire).filter_by(Annee_Scolaire=annee_scolaire).first()

        if annee_obj:
            # Récupérer les contrôles associés à cette année scolaire
            controls = Session().query(Controle). \
                filter_by(ID_Annee=annee_obj.ID_Annee). \
                options(joinedload(Controle.matiere)).all()

            # Retourner les noms des contrôles
            return [control.Nom_Controle for control in controls]

        return []

    def get_classes_in_database(self):
        classes = Session().query(Classe).all()
        filieres = Session().query(Filiere).all()

        # Ajoutez la logique pour récupérer les filières si nécessaire
        # Placeholder : Remplacez cela avec la logique réelle

        return [classe.Nom_Classe for classe in classes]

    def get_classes_from_database(self):
        # Connexion à la base de données
        engine = create_engine(DATABASE_URL, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Exécutez la requête pour obtenir la liste des classes depuis la base de données
        # et incluez le nom de la filière s'il y en a une
        classes_with_filiere = (
            session.query(Classe.Nom_Classe, Filiere.Nom_Filiere)
            .outerjoin(Filiere, Classe.Filiere_ID == Filiere.ID_Filiere)
            .all()
        )

        # Construisez la liste de chaînes pour les classes avec ou sans filière
        classes_list = [
            f"{classe.Nom_Classe} ({filiere.Nom_Filiere})" if filiere.Nom_Filiere else classe.Nom_Classe
            for classe, filiere in classes_with_filiere
        ]

        session.close()
        return classes_list

    # Enfin, modifiez la fonction get_matieres_for_filiere pour spécifier explicitement la clause onclause

    def get_fillieres_for_classe(self, classe):
        classe_obj = self.session.query(Classe).filter_by(Nom_Classe=classe).first()

        if classe_obj:
            fillieres = self.session.query(Filiere).filter_by(Classe_ID=classe_obj.ID_Classe).all()
            return fillieres

        return []

    # Modifier la fonction get_matieres_for_classe dans votre classe GestionScolaireApp
    def get_matieres_for_classe(self, classe):
        # Récupérer la classe depuis la base de données
        classe_db = self.session.query(Classe).filter_by(Nom_Classe=classe).first()

        if classe_db:
            # Si la classe a une filière, récupérer les matières spécifiques à la filière
            if classe_db.Filiere_ID:
                filiere_matieres = self.get_matieres_for_filiere(classe_db.Filiere_ID)
                return filiere_matieres
            else:
                # Sinon, récupérer toutes les matières pour la classe
                matieres = self.session.query(Matiere).all()
                return [matiere.Nom_Matiere for matiere in matieres]

        return []

    def get_matieres_for_filiere(self, filiere_id):
        # Récupérer les matières associées à la filière en utilisant une jointure
        filiere_matieres = (
            self.session.query(Matiere)
            .join(Examen, Matiere.ID_Matiere == Examen.ID_Matiere)
            .join(Classe, Examen.ID_Classe == Classe.ID_Classe)
            .filter(Classe.Filiere_ID == filiere_id)
            .distinct()
            .all()
        )

        return [matiere.Nom_Matiere for matiere in filiere_matieres]

    def supprimer_note(self):
        pass
    def modifier_note(self):
        pass

    def rechercher_bultin(self):
        pass

    def imprimmer_palmareste(self):
        pass

    def imprimer_bultin(self):
        pass

    def configurer_matiere(self):
        pass

    def configurer_bultin(self):
        pass


class FinancialsManagement:
    def __init__(self):
        pass

    def generer_rapport_paiement(self):
        # Logique pour générer le rapport de paiement global
        tk.messagebox.showinfo("Rapport de Paiement", "Génération du rapport de paiement global.")

    def generer_rapport_paiement_eleve(self):
        session = Session()
        eleve = session.query(Eleve).filter_by(Nom=self.entry_nom.get(), Prenom=self.entry_prenom.get()).first()

        if eleve is None:
            tk.messagebox.showinfo("Erreur", "Élève non trouvé.")
            return

        # Logique pour générer le rapport de paiement pour un élève spécifique
        tk.messagebox.showinfo("Rapport de Paiement", f"Génération du rapport de paiement pour {eleve.Nom} {eleve.Prenom}.")

    def ouvrir_fenetre_eleves(self):
        fenetre_eleves = tk.Toplevel(self)
        fenetre_eleves.title("Gérer les élèves")


    def create_button(self, label):
        button = tk.Button(self.main_panel, text=label, command=lambda: self.open_details_window(label))
        button.pack(pady=5)

    def open_details_window(self, label):
        details_window = tk.Toplevel(self)
        details_window.title(f"Details for {label}")
        # Ajoutez ici les champs de saisie ou les informations que vous souhaitez afficher

    def handle_menu_selection(self, event):
        # Obtenez l'élément sélectionné dans le menu
        selected_item = self.menu_panel.get(self.menu_panel.curselection())
        # Appelez la méthode pour créer un bouton dans le main_panel
        self.create_button(selected_item)


class UsersManagement:
    def __init__(self):
        pass

    def ajouter_utilisateur(self):
        # Logique pour ajouter un utilisateur
        tk.messagebox.showinfo("Ajouter Utilisateur", "Fonctionnalité non implémentée.")

    def supprimer_utilisateur(self):
        # Logique pour supprimer un utilisateur
        tk.messagebox.showinfo("Supprimer Utilisateur", "Fonctionnalité non implémentée.")

    def modifier_utilisateur(self):
        # Logique pour modifier un utilisateur
        tk.messagebox.showinfo("Modifier Utilisateur", "Fonctionnalité non implémentée.")

    def rechercher_utilisateur(self):
        # Logique pour rechercher un utilisateur
        tk.messagebox.showinfo("Rechercher Utilisateur", "Fonctionnalité non implémentée.")


class ConfigurationsManagement:
    def __init__(self):
        pass


    def modifier_config_bd(self):
        # Logique pour modifier la configuration de la base de données
        tk.messagebox.showinfo("Modifier Config. BD", "Fonctionnalité non implémentée.")

    def modifier_annee_scolaire(self):
        # Logique pour modifier l'année scolaire
        tk.messagebox.showinfo("Modifier Année Scolaire", "Fonctionnalité non implémentée.")

    def ajouter_classe(self):
        # Logique pour ajouter une classe
        tk.messagebox.showinfo("Ajouter Classe", "Fonctionnalité non implémentée.")


class MessageriesManagement:
    def __init__(self):
        pass


    def afficher_messages_envoyes(self):
        pass

    def afficher_messages_recus(self):
        pass


class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())

        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)

        if _hits != self._hits:
            self._hits = _hits
            self['values'] = self._hits

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift_R', 'Shift_L', 'Control_R', 'Control_L'):
            return

        if event.keysym == 'Return':
            self._hits = []
            return

        if event.keysym in ('Shift_R', 'Shift_L', 'Control_R', 'Control_L'):
            return

        if event.keysym == 'Tab':
            self.autocomplete(1)
            return

        if event.keysym in ('Alt_L', 'Alt_R'):
            return

        if event.keysym == 'Up':
            if self.position > 0:
                self.position -= 1
            else:
                self.position = 0
        elif event.keysym == 'Down':
            if self.position < len(self.get()):
                self.position += 1

        self.autocomplete()

        if event.keysym == 'Tab':
            self.position = 0


app = GestionScolaireApp()
app.master.mainloop()
