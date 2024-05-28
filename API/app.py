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

if __name__ == "__main__":
    app.run("127.0.0.1", port="3307")