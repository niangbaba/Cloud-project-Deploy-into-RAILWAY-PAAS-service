# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Configuration de la base de données
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///etudiants.db')
    
#     # Remplacer postgres:// par postgresql:// pour éviter les avertissements
#     if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
#         SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv('SECRET_KEY', 'cle-secrete-par-defaut')


# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///etudiants.db')
    
    # Remplacer postgres:// par postgresql:// pour éviter les avertissements
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # En production, générez une clé secrète forte et définissez-la
    # comme variable d'environnement sur Railway
    SECRET_KEY = os.getenv('SECRET_KEY', 'cle-secrete-par-defaut')
    
    # Autres configurations importantes pour Railway
    PORT = int(os.getenv('PORT', 8080))