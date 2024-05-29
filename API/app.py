from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost/flaskonautas", future=True)


@app.route('/register_user', methods = ['POST'])
def register_user():
    conn = engine.connect()
    new_user = request.get_json()
    query = f"""INSERT INTO users (username, password, security_answer_one, security_answer_two)
    VALUES
    ('{new_user["username"]}', '{new_user["password"]}', '{new_user["security_answer_one"]}', '{new_user["security_answer_two"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'El usuario no pudo ser registrado' + str(err.__cause__)})
    return jsonify({'message': 'El usuario se registro correctamente'}), 201


@app.route('/get_posts', methods = ['GET'])
def get_posts():
    connection = engine.connect()
    query = "SELECT username, id_post, category, title, post, image_link FROM posts JOIN users ON posts.id_user = users.id_user"
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


if __name__ == "__main__":
    app.run("127.0.0.1", port="5001")
