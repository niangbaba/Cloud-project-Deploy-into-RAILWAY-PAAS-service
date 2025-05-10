from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    filiere = db.Column(db.String(100))
    niveau = db.Column(db.String(20))
    date_inscription = db.Column(db.DateTime, default=db.func.current_timestamp())  # Nouveau champ
    
    def __repr__(self):
        return f'<Etudiant {self.prenom} {self.nom}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'filiere': self.filiere,
            'niveau': self.niveau,
            'date_inscription': self.date_inscription.isoformat() if self.date_inscription else None
        }