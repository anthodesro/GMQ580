from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import sqlite3
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.debug = True  # Ajouter cette ligne avant de démarrer l'app pour afficher les erreurs détaillées
CORS(app)  # Autoriser les requêtes depuis le frontend
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé secrète
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Afficher la clé secrète dans le terminal
print("JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])

jwt = JWTManager(app)

def init_db():
    # Initialiser la base de données avec la nouvelle structure
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,   -- Nouveau champ pour le prénom
                            last_name TEXT NOT NULL,    -- Nouveau champ pour le nom
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT DEFAULT 'user' NOT NULL)''')
        conn.commit()

# Récupérer un utilisateur
def get_user(email):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
        user = cursor.fetchone()  # Récupérer un seul résultat
        return user

def add_user(first_name, last_name, email, password, role):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO user (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)', 
                           (first_name, last_name, email, password, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

# Route d'accueil
@app.route('/')
def index():
    if 'username' in session:
        return f"Bienvenue, {session['username']}! <a href='/logout'>Déconnexion</a>"
    return redirect(url_for('login'))

# Route de connexion pour JWT avec inclusion du rôle
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user(email)
    if user and user[4] == password:  # Vérifier le mot de passe (user[4] pour le mot de passe)
        role = user[5]  # Récupération du rôle de l'utilisateur (user[5] pour le rôle)
        additional_claims = {"role": role}  # Ajout du rôle dans le JWT
        access_token = create_access_token(identity=email, additional_claims=additional_claims)
        return jsonify(access_token=access_token, role=role)
    return jsonify({"msg": "Identifiants incorrects"}), 401

# Route pour récupérer les infos de l'utilisateur après connexion
@app.route("/user/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()  # Récupère le username et rôle depuis le token
    return jsonify(current_user), 200

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    first_name = data.get("firstName")  # Nouveau champ pour le prénom
    last_name = data.get("lastName")    # Nouveau champ pour le nom
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not first_name or not last_name or not email or not password:
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    if add_user(first_name, last_name, email, password, role):
        return jsonify({"message": "Utilisateur créé avec succès!"}), 201
    else:
        return jsonify({"error": "Ce email est déjà pris"}), 400

@app.route('/api/users', methods=["GET"])
@jwt_required()
def get_users():
    claims = get_jwt()

    # Vérifier si l'utilisateur a les droits d'accès
    if claims.get("role") not in ["admin", "gestio"]:
        return jsonify({"msg": "Accès non autorisé"}), 403

    # Récupération des utilisateurs
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, role FROM user')
        users = cursor.fetchall()

    print(users)

    users_list = [{"id": user[0], "email": user[1], "role": user[2]} for user in users]

    return jsonify(users_list), 200

# Lancer l'application Flask
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
