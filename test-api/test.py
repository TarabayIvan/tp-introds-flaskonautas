import json
import pytest
import users
import posts
from werkzeug.security import generate_password_hash

def test_register_user(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66",
        "security_answer_two": "importa66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'El usuario se registro correctamente.'

def test_register_multiple_users(client):
    for user in users.users:
        response = client.post('/register_user', data=json.dumps(user), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'] == 'El usuario se registro correctamente.'


#SACAR ESTE TEST Y MODOFICAR SEGUN SE CAMBIE LOS REQUERIMIENTOS DE LA API
def test_register_user_repeat(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66",
        "security_answer_two": "importa66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'El usuario no pudo ser registrado'

#A este test le pasa algo raro probarlo con la base de dastos vacia
def test_user_is_resgistred(client):
    login_data = {
        "username": "guille66",
        "password": "testpassword66"
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')

    assert response.json['message'] == 'Login exitoso'

def test_user_is_not_resgistred(client):
    login_data = {
        "username": "lucass",
        "password": "lucaspass"
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'] == 'Usuario no encontrado'

def test_get_user(client):
    response = client.get('/user/1')
    assert response.status_code == 200
    assert 'username' in response.json

def test_update_password(client):
    update_data = {
        "username": "guille",
        "password": generate_password_hash("aguanteBoquitaa"),
        "security_answer_one": "queti",
        "security_answer_two": "importa"
    }
    response = client.patch('/update_password', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Se cambio la contraseña correctamente.'

def test_update_password_wrong(client):
    update_data = {
        "username": "guille",
        "password": generate_password_hash("aguanteBoquita"),
        "security_answer_one": "importa",
        "security_answer_two": "queti"
    }
    response = client.patch('/update_password', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 401
    assert response.json['message'] == 'Las respuestas a las preguntas de seguridad son incorrectas.'

def test_create_post(client):
    new_post = {
        "username": "guille",
        "category": "ANIMALS",
        "title": "HOLA",
        "post": "test_post",
        "image_link": "test_image_link"
    }
    response = client.post('/create_post', data=json.dumps(new_post), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'].startswith('se ha agregado correctamente')

def test_create_multiple_posts(client):
    for post in posts.posts:
        response = client.post('/create_post', data=json.dumps(post), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'].startswith('se ha agregado correctamente')

def test_get_post_by_categories(client):
    response = client.get('/get_posts/Animalitos')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_last_posts(client):
    response = client.get('/get_last_posts')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert len(response.json) <= 6