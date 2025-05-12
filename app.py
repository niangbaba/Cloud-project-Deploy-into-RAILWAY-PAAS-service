from flask import Flask, request, jsonify, abort
from models import db, Etudiant
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Créer les tables au démarrage
with app.app_context():
    db.create_all()

# Route d'accueil
@app.route('/')
def index():
    return jsonify({
        'message': 'Bienvenue sur l\'API de gestion des étudiants - v1.1',
        'endpoints': {
            'GET /info': 'Informations sur l\'API',
            'GET /etudiants': 'Liste tous les étudiants',
            'GET /etudiants/:id': 'Détails d\'un étudiant',
            'POST /etudiants': 'Créer un nouvel étudiant',
            'PUT /etudiants/:id': 'Mettre à jour un étudiant',
            # 'DELETE /etudiants/:id': 'Supprimer un étudiant'
        }
    })

# Créer un étudiant
@app.route('/etudiants', methods=['POST'])
def creer_etudiant():
    data = request.get_json()
    
    # Validation des données
    required_fields = ['nom', 'prenom', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    # Vérifier si l'email existe déjà
    if Etudiant.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Cet email est déjà utilisé'}), 400
    
    # Créer le nouvel étudiant
    nouvel_etudiant = Etudiant(
        nom=data['nom'],
        prenom=data['prenom'],
        email=data['email'],
        filiere=data.get('filiere', ''),
        niveau=data.get('niveau', '')
    )
    
    db.session.add(nouvel_etudiant)
    db.session.commit()
    
    return jsonify(nouvel_etudiant.to_dict()), 201

# Obtenir tous les étudiants
@app.route('/etudiants', methods=['GET'])
def obtenir_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([etudiant.to_dict() for etudiant in etudiants])

# Obtenir un étudiant par ID
@app.route('/etudiants/<int:etudiant_id>', methods=['GET'])
def obtenir_etudiant(etudiant_id):
    etudiant = Etudiant.query.get_or_404(etudiant_id)
    return jsonify(etudiant.to_dict())

# Mettre à jour un étudiant
@app.route('/etudiants/<int:etudiant_id>', methods=['PUT'])
def mettre_a_jour_etudiant(etudiant_id):
    etudiant = Etudiant.query.get_or_404(etudiant_id)
    data = request.get_json()
    
    # Mise à jour des champs
    if 'nom' in data:
        etudiant.nom = data['nom']
    if 'prenom' in data:
        etudiant.prenom = data['prenom']
    if 'email' in data:
        # Vérifier si le nouvel email est déjà utilisé par un autre étudiant
        if data['email'] != etudiant.email and Etudiant.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400
        etudiant.email = data['email']
    if 'filiere' in data:
        etudiant.filiere = data['filiere']
    if 'niveau' in data:
        etudiant.niveau = data['niveau']
    
    db.session.commit()
    
    return jsonify(etudiant.to_dict())

# Supprimer un étudiant
@app.route('/etudiants/<int:etudiant_id>', methods=['DELETE'])
def supprimer_etudiant(etudiant_id):
    etudiant = Etudiant.query.get_or_404(etudiant_id)
    db.session.delete(etudiant)
    db.session.commit()
    
    return jsonify({'message': f'Étudiant avec ID {etudiant_id} supprimé avec succès'})


# Ajouter cette nouvelle route
@app.route('/info', methods=['GET'])
def api_info():
    return jsonify({
        'nom': 'API Gestion Étudiants',
        'version': '1.1.0',
        'auteur': 'Votre Nom',
        'date': '10 mai 2025',
        'description': 'API CRUD pour la gestion des étudiants',
        'environnement': 'Production' if os.getenv('RAILWAY_ENVIRONMENT') else 'Développement'
    })

# Pour gérer les erreurs 404
@app.errorhandler(404)
def ressource_non_trouvee(e):
    return jsonify({'error': 'Ressource non trouvée'}), 404

if __name__ == '__main__':
    app.run(debug=True)