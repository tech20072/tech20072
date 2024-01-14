from sqlalchemy import Enum, create_engine, Column, Integer, String, Float, LargeBinary, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker
import uuid
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql://root:av604609@localhost/jac_official_dataset"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

class AnneeScolaire(Base):
    __tablename__ = 'Annees_Scolaires'

    ID_Annee = Column(Integer, primary_key=True)
    Annee_Scolaire = Column(String(10), nullable=False)
    Statut = Column(String(20), nullable=False)
    eleves = relationship("Eleve", back_populates="annee")
    controles = relationship("Controle", back_populates="annee_scolaire")

class Filiere(Base):
    __tablename__ = 'Filieres'

    ID_Filiere = Column(Integer, primary_key=True)
    Nom_Filiere = Column(String(50), nullable=False)
    Code_Filiere = Column(String(10), nullable=False, unique=True)
    ID_Classe = Column(Integer, ForeignKey('Classes.ID_Classe'))
    classe = relationship("Classe", back_populates="filieres", foreign_keys=[ID_Classe])

class Classe(Base):
    __tablename__ = 'Classes'

    ID_Classe = Column(Integer, primary_key=True)
    Nom_Classe = Column(String(50), nullable=False)
    ID_Section = Column(Integer, ForeignKey('Sections.ID_Section'))
    Filiere_ID = Column(Integer, ForeignKey('Filieres.ID_Filiere'))
    eleves = relationship("Eleve", back_populates="classe")
    section = relationship('Section', back_populates='classes')
    filiere = relationship('Filiere', back_populates='classes', foreign_keys=[Filiere_ID],primaryjoin="Filiere.ID_Classe == Classe.Filiere_ID")
    controles = relationship("Controle", back_populates="classe")


class Section(Base):
    __tablename__ = 'Sections'

    ID_Section = Column(Integer, primary_key=True)
    Nom_Section = Column(String(50), nullable=False)
    classes = relationship("Classe", back_populates="section")

class Eleve(Base):
    __tablename__ = 'Eleves'

    ID_Eleve = Column(Integer, primary_key=True, autoincrement=True)
    Identifiant_Eleve = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True)
    Nom = Column(String(50), nullable=False)
    Prenom = Column(String(50), nullable=False)
    Date_Naissance = Column(Date)
    Photo_Identite = Column(LargeBinary)
    Sexe = Column(Enum('male', 'female'), nullable=False)
    Annee_ID = Column(Integer, ForeignKey('Annees_Scolaires.ID_Annee'))
    Classe_ID = Column(Integer, ForeignKey('Classes.ID_Classe'))
    annee = relationship("AnneeScolaire", back_populates="eleves")
    classe = relationship("Classe", back_populates="eleves")
    notes = relationship("Note", back_populates="eleve")

class Cours(Base):
    __tablename__ = 'Cours'

    ID_Cours = Column(Integer, primary_key=True)
    Nom_Cours = Column(String(100), nullable=False)
    Code_Cours = Column(String(20), nullable=False)
    Enseignant_Responsable = Column(Integer, ForeignKey('Enseignants.ID_Enseignant'))
    enseignant = relationship("Enseignant", back_populates="cours")

# Ajouter la table des matières
class Matiere(Base):
    __tablename__ = 'Matieres'

    ID_Matiere = Column(Integer, primary_key=True, autoincrement=True)
    Nom_Matiere = Column(String(100), nullable=False)
    Code_Matiere = Column(String(20), nullable=False)
    controles = relationship("Controle", back_populates="matiere")
    examens = relationship("Examen", back_populates="matiere")
    notes = relationship("Note", back_populates="matiere")

class Note(Base):
    __tablename__ = 'Notes'

    ID_Note = Column(Integer, primary_key=True)
    ID_Eleve = Column(Integer, ForeignKey('Eleves.ID_Eleve'))
    ID_Matiere = Column(Integer, ForeignKey('Matieres.ID_Matiere'))
    ID_Annee = Column(Integer, ForeignKey('Annees_Scolaires.ID_Annee'))
    ID_Controle = Column(Integer, ForeignKey('Controles.ID_Controle'))
    eleve = relationship("Eleve", back_populates="notes")
    matiere = relationship("Matiere", back_populates="notes")
    controle = relationship("Controle", back_populates="notes")

class Enseignant(Base):
    __tablename__ = 'Enseignants'

    ID_Enseignant = Column(Integer, primary_key=True)
    Nom = Column(String(50), nullable=False)
    Prenom = Column(String(50), nullable=False)
    Matiere_Principale = Column(String(100))
    cours = relationship("Cours", back_populates="enseignant")

# Ajouter la table des examens
class Examen(Base):
    __tablename__ = 'Examens'

    ID_Examen = Column(Integer, primary_key=True)
    Nom_Examen = Column(String(100), nullable=False)
    Date_Examen = Column(Date)
    ID_Matiere = Column(Integer, ForeignKey('Matieres.ID_Matiere'))
    matiere = relationship("Matiere", back_populates="examens")

# Ajouter la table des bulletins
class Bulletin(Base):
    __tablename__ = 'Bulletins'

    ID_Bulletin = Column(Integer, primary_key=True)
    ID_Eleve = Column(Integer, ForeignKey('Eleves.ID_Eleve'))
    ID_Examen = Column(Integer, ForeignKey('Examens.ID_Examen'))
    Note_Examen = Column(Float)

class Controle(Base):
    __tablename__ = 'Controles'

    ID_Controle = Column(Integer, primary_key=True)
    Nom_Controle = Column(String(100), nullable=False)
    Date_Controle = Column(Date)
    ID_Matiere = Column(Integer, ForeignKey('Matieres.ID_Matiere'))
    ID_Classe = Column(Integer, ForeignKey('Classes.ID_Classe'))
    ID_Annee = Column(Integer, ForeignKey('Annees_Scolaires.ID_Annee'))
    matiere = relationship("Matiere", back_populates="controles")
    classe = relationship("Classe", back_populates="controles")
    notes = relationship("Note", back_populates="controle")
    annee_scolaire = relationship("AnneeScolaire", back_populates="controles")

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)