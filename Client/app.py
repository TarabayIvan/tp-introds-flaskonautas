from flask import Flask, jsonify, request, url_for, redirect, render_template, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

API_URL = 'http://localhost:5001'

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        security_answer_one = request.form.get('security_answer_one')
        security_answer_two = request.form.get('security_answer_two')
        passhash = generate_password_hash(password)
        user = {'username': username, 'password': passhash, 'security_answer_one': security_answer_one, 'security_answer_two': security_answer_two}
        if (username and password and security_answer_one and security_answer_two):
            response = requests.post(API_URL + "/register_user", json=user)
            if response.status_code == 201:
                return redirect(url_for('login'))  # Redirige a login luego del registro exitoso.
            else:
                error_message = "Registro fallido"
                return render_template('signup.html', error=error_message)
    return render_template('signup.html')  # Renderiza el form de registro


@app.route("/")
def index():
    if 'user' in session:
        username = session['user']['user']['username']
        return render_template("index.html", username = username)
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_credentials = {'username': username, 'password': password}
        if username and password:
            response = requests.post(API_URL + "/login_user", json=user_credentials)
            if response.status_code == 200:
                user_data = response.json()
                session['user'] = user_data  # Guarda la data de usuario en session
                return redirect(url_for('index'))
            else:
                error_message = "Login fallido"
                return render_template('index.html', error=error_message)
    return render_template('login.html')


@app.route("/delete-account", methods=['GET', 'POST'])
def delete_account():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_credentials = {'username': username, 'password': password}
        if username and password:
            response = requests.post(API_URL + "/delete_user", json=user_credentials)
            if response.status_code == 200:
                session.pop('user', None)
                return redirect(url_for('index'))
            else:
                error_message = "No se pudo eliminar la cuenta."
                return render_template('user.html', error=error_message)
    return render_template('delete-account.html')


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == "POST":
        username = request.form.get('user')
        new_password = request.form.get('newpword')
        security_answer_1 = request.form.get('secquestions1')
        security_answer_2 = request.form.get('secquestions2')
        new_password_hashed = generate_password_hash(new_password)
        user_credentials = {'username': username, 'password': new_password_hashed, 'security_answer_one': security_answer_1 , 'security_answer_two': security_answer_2 }
        if username and new_password and security_answer_1 and security_answer_2:
            respone = requests.patch(API_URL + '/update_password', json = user_credentials)
            if respone.status_code == 200:
                return redirect(url_for('login')) # Redirige a login si se cambio la contraseña
            elif respone.status_code == 401:
                error_msj = "Las respuestas a las preguntas de seguridad son incorrectas."
                return render_template('recovery.html', error = error_msj)
            elif respone.status_code == 404:
                error_msj = "El usuario no existe."
                return render_template('recovery.html', error = error_msj)
            else:
                error_msj = "Hubo un problema al cambiar la contraseña"
                return render_template('recovery.html', error = error_msj)
    return render_template('recovery.html')


@app.route('/modificar-password', methods=['GET', 'POST'])
def modificar_password():
    if request.method == "POST":
        username = request.form.get('user')
        new_password = request.form.get('newpword')
        security_answer_1 = request.form.get('secquestions1')
        security_answer_2 = request.form.get('secquestions2')
        new_password_hashed = generate_password_hash(new_password)
        user_credentials = {'username': username, 'password': new_password_hashed, 'security_answer_one': security_answer_1 , 'security_answer_two': security_answer_2 }
        if username and new_password and security_answer_1 and security_answer_2:
            respone = requests.patch(API_URL + '/update_password', json = user_credentials)
            if respone.status_code == 200:
                return redirect(url_for('login')) # Redirige a login si se cambio la contraseña
            elif respone.status_code == 401:
                error_msj = "Las respuestas a las preguntas de seguridad son incorrectas."
                return render_template('refactor_password.html', error = error_msj)
            elif respone.status_code == 404:
                error_msj = "El usuario no existe."
                return render_template('refactor_password.html', error = error_msj)
            else:
                error_msj = "Hubo un problema al cambiar la contraseña"
                return render_template('refactor_password.html', error = error_msj)
    return render_template('refactor_password.html')


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route("/user_data", methods=['GET'])
def get_user_data():
    if 'user' in session:
        user_id = session['user']['id']  # Suponiendo que tienes el ID del usuario en la sesión
        response = requests.get(API_URL + f"/user/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            return render_template("user.html", user_data=user_data)
        else:
            return render_template("user.html", user_data={"username": "Usuario no autenticado", "password": "Usuario no autenticado"})
    else:
        return render_template("user.html", user_data={"username": "Usuario no autenticado", "password": "Usuario no autenticado"})


@app.route("/latest_posts", methods=['GET'])
def latest_posts():
    response = requests.get(API_URL + "/get_last_posts")
    if response.status_code == 200:
        posts = response.json()
        return render_template("latest_posts.html", posts=posts)
    else:
        return jsonify({"error": "No se pudieron obtener los posts"}), 400
    

@app.route("/categories", methods=['GET'])
def categories():
    return render_template("categories.html")


@app.route("/c/<selected_category>")
def category(selected_category):
    categorias_elegibles = {'Technology', 'Science', 'Health', 'Music', 'Politics', 'Sports', 'Entertainment', 'Travel', 'Art'}
    if selected_category not in categorias_elegibles:
        return page_not_found(404)
    response = requests.get(API_URL + f"/get_posts/{selected_category}")
    posts = response.json()
    return render_template("category.html", posts=posts, category=selected_category)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)
