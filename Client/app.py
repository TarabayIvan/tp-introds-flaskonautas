from flask import Flask, jsonify, request, url_for, redirect, render_template
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
API_URL = 'http://localhost:3307/'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        security_answer_one = request.form.get('security_answer_one')
        security_answer_two = request.form.get('security_answer_two')
        passhash = generate_password_hash(password)
        user = {'username': username, 'password': passhash, 'security_answer_one': security_answer_one, 'security_answer_two': security_answer_two}
        if (username and password and security_answer_one and security_answer_two):
            response = requests.post(API_URL + "register_user", json=user)
            return redirect('index') # Redirect a index, o a login, o a donde se necesite
    # Crear el funcionamiento con metodo GET

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000")