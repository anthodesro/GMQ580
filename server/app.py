from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes depuis le frontend
load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Clé secrète pour JWT
jwt = JWTManager(app)

# Clé secrète pour la gestion des sessions
app.secret_key = 'votre_cle_secrete'

# Initialisation de la base de données avec le champ role
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT DEFAULT 'user' NOT NULL)''')
        conn.commit()

# Récupérer un utilisateur
def get_user(username):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        return cursor.fetchone()

# Ajouter un utilisateur avec un rôle par défaut
def add_user(username, password, role='user'):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO user (username, password, role) VALUES (?, ?, ?)', (username, password, role))
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
    username = data.get("username")
    password = data.get("password")

    user = get_user(username)
    if user and user[2] == password:
        role = user[3]  # Récupération du rôle depuis la DB
        access_token = create_access_token(identity={"username": username, "role": role})
        return jsonify(access_token=access_token, role=role), 200
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

# Route d'inscription avec possibilité de définir un rôle
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'Utilisateur')  # Par défaut, rôle "user"
        
        if add_user(username, password, role):
            return "Utilisateur créé avec succès! <a href='/login'>Connexion</a>"
        else:
            return "Ce nom d'utilisateur est déjà pris. <a href='/register'>Réessayer</a>"
    
    return '''
        <form method='post'>
            Identifiant: <input type='text' name='username'><br>
            Mot de passe: <input type='password' name='password'><br>
            Rôle: <select name='role'>
                <option value='user'>Utilisateur</option>
                <option value='gestio'>Gestionnaire</option>
                <option value='admin'>Administrateur</option>
            </select><br>
            <input type='submit' value='S'inscrire'>
        </form>
    '''

# Route protégée nécessitant un token
@app.route('/api/data', methods=["GET"])
@jwt_required()
def api_data():
    current_user = get_jwt_identity()
    data = ["data1", "data2", "data3"]
    return jsonify({'data': data, 'user': current_user})

# Lancer l'application Flask
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
