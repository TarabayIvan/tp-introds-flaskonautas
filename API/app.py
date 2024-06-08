from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.security import check_password_hash


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost/flaskonautas", future=True)


@app.route('/register_user', methods = ['POST'])
def register_user():
    conn = engine.connect()
    new_user = request.get_json()
    if not (new_user.get("username") and new_user.get("password") and new_user.get("security_answer_one") and new_user.get("security_answer_two")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400
    query = f"""INSERT INTO users (username, password, security_answer_one, security_answer_two)
    VALUES
    ('{new_user["username"]}', '{new_user["password"]}', '{new_user["security_answer_one"]}', '{new_user["security_answer_two"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'El usuario no pudo ser registrado.' + str(err.__cause__)})
    return jsonify({'message': 'El usuario se registro correctamente.'}), 201

@app.route('/delete_user', methods = ['DELETE'])
def delete_user():
    conn = engine.connect()
    user_data = request.get_json() 
    if not (user_data.get("username") and user_data.get("password")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400
    query_deletion = f"""DELETE FROM users
            WHERE username='{user_data["username"]}';"""
    query_check = f"""SELECT password FROM users
            WHERE username='{user_data["username"]}';"""
    try:
        check = conn.execute(text(query_check))
        conn.commit()
        user_hash = check.fetchone()
        if(check_password_hash(user_hash[0], user_data["password"])):
            result = conn.execute(text(query_deletion))
            conn.commit()
        else:
            return jsonify({'message': 'La contraseña no coincide con la del usuario'}), 403
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'No se pudo borrar la cuenta del usuario' + str(err.__cause__)})
    return jsonify({'message': 'La cuenta del usuario fue borrada correctamente.'}), 200

@app.route('/login_user', methods=['POST'])
def login_user():
    conn = engine.connect()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username y password son requeridos'}), 400

    # Consultar el usuario por nombre de usuario
    query = f"SELECT * FROM users WHERE username = '{username}';"
    try:
        result = conn.execute(text(query))
        user = result.fetchone()
        conn.close()
        if user:
            # Verificar la contraseña
            if check_password_hash(user[2], password):
                return jsonify({'message': 'Login exitoso', 'user': {'username': user[1]}}), 200
            else:
                return jsonify({'message': 'Credenciales incorrectas'}), 401
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error en el servidor: ' + str(err.__cause__)}), 500
    
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = engine.connect()
    query = f"SELECT id_user, username, security_answer_one, security_answer_two FROM users WHERE id_user = {user_id};"
    try:
        result = conn.execute(text(query))
        user = result.fetchone()
        conn.close()
        if user:
            user_data = {
                'id_user': user.id_user,
                'username': user.username,
                'security_answer_one': user.security_answer_one,
                'security_answer_two': user.security_answer_two
                # Excluir el password por razones de seguridad
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except SQLAlchemyError as err:
        return jsonify({"message": "Error en el servidor: " + str(err.__cause__)}), 500

@app.route('/update_password', methods = ['PATCH'])
def update_password():
    conn = engine.connect()
    data = request.get_json() # The function should recieve username, a new *hashed* password, and both security answers
    if not (data.get("username") and data.get("password") and data.get("security_answer_one") and data.get("security_answer_two")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400
    query = f"""UPDATE users
                SET password = '{data['password']}'
                WHERE username = '{data['username']}';
            """
    query_validation = f"SELECT * FROM users WHERE username = '{data['username']}';" # Usernames are unique
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount!=0:
            user = val_result.fetchone()
            if user[3] == data['security_answer_one'] and user[4] == data['security_answer_two']:
                result = conn.execute(text(query))
                print(result)
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({'message': "Las respuestas a las preguntas de seguridad son incorrectas."}), 401
        else:
            conn.close()
            return jsonify({'message': "El usuario no existe."}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'Se cambio la contraseña correctamente.'}), 200

# Basically the same as /get_posts, but gets posts of all categories, with a limit of 6
@app.route('/get_last_posts', methods=['GET'])
def get_last_posts():
    connection = engine.connect()
    query = f"SELECT username, id_post, category, title, post, image_link FROM posts JOIN users ON posts.id_user = users.id_user ORDER BY id_post DESC LIMIT 6"
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


@app.route('/get_posts/<selected_category>', methods = ['GET'])
def get_posts(selected_category):
    connection = engine.connect()
    query = f"SELECT username, id_post, category, title, post, image_link FROM posts JOIN users ON posts.id_user = users.id_user WHERE category LIKE '{selected_category}' ORDER BY id_post DESC"
    try:
        data = connection.execute(text(query))
        connection.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 400
    posts = []
    for row in data:
        entity = {}
        entity['username'] = row.username
        entity['id_post'] = row.id_post # necesario? (ya se ordena en la query)
        entity['category'] = row.category
        entity['title'] = row.title
        entity['post'] = row.post
        entity['image_link'] = row.image_link
        posts.append(entity)
    return jsonify(posts), 200


@app.route('/create_post', methods = ['POST'])
def create_post():
    connection = engine.connect()
    new_post = request.get_json()

    required_fields = ["username", "category", "title", "post", "image_link"] # validar que se reciben los campos necesarios
    for field in required_fields:
        if field not in new_post:
            return jsonify({'message': f'Faltan datos en la solicitud ({field})'}), 400

    query1 = f"SELECT id_user FROM users WHERE username = '{new_post['username']}'" # buscar el id del usuario
    try:
        id_user = connection.execute(text(query1)).scalar() # scalar() para obtener el unico valor de la consulta

        if id_user is None:
            connection.close()
            return jsonify({'message': 'El usuario no existe'}), 400
    except SQLAlchemyError as err:
        connection.close()
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)}), 400

    query2 = f"""INSERT INTO posts (id_user, category, title, post, image_link) VALUES ('{id_user}', '{new_post["category"]}', '{new_post["title"]}', '{new_post["post"]}', '{new_post["image_link"]}');"""
    try:
        connection.execute(text(query2))
        connection.commit()
        connection.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)}), 400
    return jsonify({'message': 'se ha agregado correctamente ' + query2}), 201


@app.route('/get_responses', methods = ['GET']) 

def get_responses (id_post): 

    connection = engine.connect() 

    query = f" SELECT id_response, id_user, id_post, post FROM responses WHERE id_post = {id_post};" 

    try: 

        data = connection.execute(text(query)) 

        connection.close() 

    except SQLAlchemyError as err: 

        return jsonify(str(err.__cause__)), 400 

    posts = [] 

    for row in data: 

        entity = {} 

        entity['id_response'] = row.id_response 

        entity['id_user '] = row.id_user  

        entity['id_post'] = row.id_post 

        entity['post'] = row.post        

        posts.append(entity) 

    return jsonify(posts), 200

@app.route('/create_response', methods = ['POST'])
def create_response():
    connection = engine.connect()
    new_response = request.get_json()
    required_fields = ['username', 'post', 'id_post'] # valido que se reciben los campos necesarios
    for field in required_fields:
        if field not in new_response:
            return jsonify({'message': f'Faltan datos en la solicitud ({field})'}), 400
        
    username = new_response['username']

    query_1 = f"SELECT id_user FROM users WHERE username = '{username}'" # buscar el id del usuario
    try:
        id_user = connection.execute(text(query_1)).scalar() # scalar() para obtener el unico valor de la consulta
        if id_user is None:
            connection.close()
            return jsonify({'message': f'El usuario con nombre ({username}) no existe'}), 400
    except SQLAlchemyError as err:
        connection.close()
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)}), 400
    
    query_2 = f"""INSERT INTO responses (id_user, id_post, post) VALUES ('{id_user}', '{new_response['id_post']}', '{new_response['post']}');"""
    try:
        connection.execute(text(query_2)) 
        connection.commit() #subo la respuesta
        connection.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)}), 400
    return jsonify({'message': 'se ha agregado correctamente ' + query_2}), 201

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)
