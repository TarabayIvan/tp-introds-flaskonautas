from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost/flaskonautas")


@app.route('/get_posts', methods = ['GET'])
def posts():
    connection = engine.connect()
    query = "SELECT * FROM posts;"
    try:
        data = connection.execute(text(query))
        connection.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    posts = []
    for row in data:
        entity = {}
        entity['id_post'] = row.id_post
        entity['id_user'] = row.id_user
        entity['category'] = row.category
        entity['title'] = row.title
        entity['post'] = row.post
        entity['image_link'] = row.image_link
        posts.append(entity)
    return jsonify(posts), 200


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000")