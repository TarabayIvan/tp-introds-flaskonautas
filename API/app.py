from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:123@localhost/flaskonautas")


if __name__ == "__main__":
    app.run("127.0.0.1", port="3306")