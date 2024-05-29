from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost/flaskonautas", future=True)


@app.route('/register_user', methods = ['POST'])
def register_user():
    conn = engine.connect()
    new_user = request.get_json()
    hashed_password = generate_password_hash(new_user["password"])
    query = f"""INSERT INTO users (username, password, security_answer_one, security_answer_two)
    VALUES
    ('{new_user["username"]}', '{hashed_password}', '{new_user["security_answer_one"]}', '{new_user["security_answer_two"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'El usuario no pudo ser registrado' + str(err.__cause__)})
    return jsonify({'message': 'El usuario se registro correctamente'}), 201

@app.route('/login', methods=['POST'])
def login():
    conn = engine.connect()
    mod_user = request.get_json()
    username = mod_user['username']
    password = mod_user['password']
    
    # Consultar el usuario por nombre de usuario
    query = f"SELECT * FROM users WHERE username = '{username}';"
    try:
        result = conn.execute(text(query))
        user = result.first()
        conn.close()
        if user:
            # Verificar la contraseña
            stored_password_hash = user.password
            if check_password_hash(stored_password_hash, password):
                return jsonify({'message': 'Login exitoso'}), 200
            else:
                return jsonify({'message': 'Credenciales incorrectas'}), 401
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error en el servidor: ' + str(err.__cause__)}), 500
    
@app.route('/users', methods = ['GET'])
def get_users():
    connection = engine.connect()
    query = "SELECT * FROM users;"
    try:
        data = connection.execute(text(query))
        connection.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 400
    users = []
    for row in data:
        entity = {}
        entity['id_user'] = row.id_user
        entity['password'] = row.password
        entity['security_answer_one'] = row.security_answer_one
        entity['security_answer_two'] = row.security_answer_two
        users.append(entity)
    return jsonify(users), 200

@app.route('/users/<id_user>', methods = ['PATCH'])
def update_user(id_user):
    conn = engine.connect()
    mod_user = request.get_json()
    old_password = mod_user['old_password']
    new_password = mod_user['new_password']
    confirm_new_password = mod_user['confirm_new_password']
    
    if new_password != confirm_new_password:
        return jsonify({'message': 'Las nuevas contraseñas no coinciden'}), 400

    query_validation = f"SELECT * FROM users WHERE id_user = {id_user};"
    
    try:
        val_result = conn.execute(text(query_validation))
        user = val_result.fetchone()
        if user:
            stored_password_hash = user.password
            if check_password_hash(stored_password_hash, old_password):
                hashed_new_password = generate_password_hash(new_password)
                query = f"UPDATE users SET password = '{hashed_new_password}' WHERE id_user = {id_user};"
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
                return jsonify({'message': 'La contraseña ha sido modificada correctamente'}), 200
            else:
                conn.close()
                return jsonify({'message': 'La contraseña antigua es incorrecta'}), 401
        else:
            conn.close()
            return jsonify({'message': 'El usuario no existe'}), 404
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': str(err.__cause__)}), 500
    

@app.route('/verify_identity', methods=['POST'])
def verify_identity():
    conn = engine.connect()
    mod_user = request.get_json()
    username = mod_user['username']
    security_answer_one = mod_user['security_answer_one']
    security_answer_two = mod_user['security_answer_two']
    
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        result = conn.execute(text(query))
        user = result.first()
        conn.close()
        if user:
            if (user.security_answer_one == security_answer_one and 
                user.security_answer_two == security_answer_two):
                return jsonify({'message': 'Identidad verificada', 'username': username}), 200
            else:
                return jsonify({'message': 'Respuestas incorrectas'}), 401
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error en el servidor: ' + str(err.__cause__)}), 500

@app.route('/reset_password/<id_user>', methods=['PATCH'])
def reset_password(id_user):
    conn = engine.connect()
    mod_user = request.get_json()
    new_password = mod_user['password']
    hashed_password = generate_password_hash(new_password)
    
    query = f"""
    UPDATE users SET password = '{hashed_password}'
    WHERE id_user = {id_user};
    """
    query_validation = f"SELECT * FROM users WHERE id_user = {id_user};"
    
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount != 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
            return jsonify({'message': 'La contraseña ha sido modificada correctamente'}), 200
        else:
            conn.close()
            return jsonify({'message': 'El usuario no existe'}), 404
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': str(err.__cause__)}), 500

@app.route('/posts', methods = ['GET'])
def get_posts():
    connection = engine.connect()
    query = "SELECT * FROM posts JOIN users ON posts.id_user = users.id_user"
    try:
        data = connection.execute(text(query))
        connection.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 400
    posts = []
    for row in data:
        entity = {}
        entity['username'] = row.username
        entity['id_post'] = row.id_post
        entity['category'] = row.category
        entity['title'] = row.title
        entity['post'] = row.post
        entity['image_link'] = row.image_link
        posts.append(entity)
    return jsonify(posts), 200

@app.route('/posts/<id_post>', methods = ['GET'])
def get_post(id_post):
    conn = engine.connect()
    query = f"""SELECT *
            FROM posts
            WHERE id_post = {id_post};
            """
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    if result.rowcount !=0:
        data = {}
        row = result.first()
        data['id_post'] = row[0]
        data['id_user'] = row[1]
        data['category'] = row[2]
        data['title'] = row[3]
        data['post'] = row[4]
        data['image_link'] = row[5]
        return jsonify(data), 200
    return jsonify({"message": "El post no existe"}), 404

@app.route('/posts/<id_post>', methods = ['PATCH'])
def update_post(id_post):
    conn = engine.connect()
    mod_post = request.get_json()
    query = f"""UPDATE posts SET post = '{mod_post['post']}'
                {f"category = '{mod_post['category']}'" if "category" in mod_post else ""}
                {f", title = '{mod_post['title']}'" if "title" in mod_post else ""}
                {f", image_link = '{mod_post['image_link']}'" if "image_link" in mod_post else ""}

                WHERE id_post = {id_post};
            """
    query_validation = f"SELECT * FROM posts WHERE id_post = {id_post};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "El post no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'se ha modificado correctamente' + query}), 200


@app.route('/posts/<id_post>', methods = ['DELETE'])
def delete_post(id_post):
    conn = engine.connect()
    query = f"""DELETE FROM posts
            WHERE id_post = {id_post};
            """
    validation_query = f"SELECT * FROM users WHERE id_post = {id_post}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "El post no existe"}), 404
    except SQLAlchemyError as err:
        jsonify(str(err.__cause__))
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000")
