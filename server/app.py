from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import sqlite3
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.debug = True  # Pour afficher les erreurs détaillées
CORS(app)  # Autoriser les requêtes depuis le frontend

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé secrète
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Afficher la clé secrète dans le terminal
print("JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])

jwt = JWTManager(app)


# ===============================
# 1. Initialisation de la base de données
# ===============================
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT DEFAULT 'user' NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS project (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS user_projects (
                            user_id INTEGER,
                            project_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user(id),
                            FOREIGN KEY (project_id) REFERENCES project(id),
                            PRIMARY KEY (user_id, project_id))''')

        conn.commit()


# ===============================
# 2. Fonctions Utilisateurs
# ===============================

def get_user(email):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, first_name, last_name, role FROM user WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            user_data = {
                "id": user[0],
                "email": user[1],
                "first_name": user[2],
                "last_name": user[3],
                "role": user[4]
            }

            # Récupérer les projets associés
            cursor.execute('''SELECT project.id, project.name, project.description
                              FROM project
                              JOIN user_projects ON project.id = user_projects.project_id
                              WHERE user_projects.user_id = ?''', (user[0],))
            projects = cursor.fetchall()
            user_data["projects"] = [{"id": project[0], "name": project[1], "description": project[2]} for project in projects]
            
            return user_data
        return None


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


# ===============================
# 3. Fonctions Projets
# ===============================

def get_projects():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description FROM project')
        projects = cursor.fetchall()
    return [{"id": project[0], "name": project[1], "description": project[2]} for project in projects]


def add_project(name, description):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO project (name, description) VALUES (?, ?)', (name, description))
        conn.commit()


# ===============================
# 4. Authentification et gestion de session JWT
# ===============================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user(email)
    if user and user["password"] == password:
        additional_claims = {"role": user["role"]}
        access_token = create_access_token(identity=email, additional_claims=additional_claims)
        return jsonify(access_token=access_token, role=user["role"])
    return jsonify({"msg": "Identifiants incorrects"}), 401


@app.route("/user/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user_data = get_user(current_user)
    if user_data:
        return jsonify(user_data), 200
    return jsonify({"msg": "Utilisateur non trouvé"}), 404


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# ===============================
# 5. Routes API Utilisateurs
# ===============================

@app.route('/api/users', methods=["GET"])
@jwt_required()
def get_users():
    claims = get_jwt()
    if claims.get("role") not in ["admin", "gestio"]:
        return jsonify({"msg": "Accès non autorisé"}), 403

    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, role FROM user')
        users = cursor.fetchall()

    users_list = []
    for user in users:
        user_id = user[0]
        user_data = {
            "id": user[0],
            "email": user[1],
            "role": user[2]
        }

        cursor.execute('''SELECT project.id, project.name, project.description
                          FROM project
                          JOIN user_projects ON project.id = user_projects.project_id
                          WHERE user_projects.user_id = ?''', (user_id,))
        projects = cursor.fetchall()

        user_data["projects"] = [{"id": project[0], "name": project[1], "description": project[2]} for project in projects]
        users_list.append(user_data)

    return jsonify(users_list), 200


@app.route('/api/user/<string:email>', methods=["GET"])
@jwt_required()
def get_user_by_email(email):
    user_data = get_user(email)
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "Utilisateur non trouvé"}), 404


@app.route('/api/user/<int:user_id>/projects/<int:project_id>', methods=["POST"])
@jwt_required()
def assign_project_to_user(user_id, project_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        cursor.execute('SELECT id FROM project WHERE id = ?', (project_id,))
        project = cursor.fetchone()

        if not user or not project:
            return jsonify({"error": "Utilisateur ou projet non trouvé"}), 404

        cursor.execute('SELECT * FROM user_projects WHERE user_id = ? AND project_id = ?', (user_id, project_id))
        existing_association = cursor.fetchone()

        if existing_association:
            return jsonify({"message": "Ce projet est déjà associé à cet utilisateur"}), 400

        cursor.execute('INSERT INTO user_projects (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
        conn.commit()
        return jsonify({"message": "Projet associé à l'utilisateur avec succès!"}), 201


# ===============================
# 6. Routes API Projets
# ===============================

@app.route('/api/projects', methods=["GET"])
@jwt_required()
def get_all_projects():
    projects = get_projects()
    return jsonify(projects), 200


@app.route('/api/projects', methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    if not name or not description:
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400
    add_project(name, description)
    return jsonify({"message": "Projet ajouté avec succès!"}), 201


# Lancer l'application Flask
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
