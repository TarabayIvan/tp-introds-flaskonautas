import json
import users
import posts
from werkzeug.security import generate_password_hash

def test_register_user_success(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66",
        "security_answer_two": "importa66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'El usuario se registro correctamente.'


def test_register_multiple_users_success(client):
    for user in users.users:
        response = client.post('/register_user', data=json.dumps(user), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'] == 'El usuario se registro correctamente.'


def test_register_user_incomplete_data(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'No se enviaron todos los datos necesarios por JSON'


def test_register_user_empy_data_password(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash(""),
        "security_answer_one": "queti66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'No se enviaron todos los datos necesarios por JSON'


def test_register_duplicate_users(client):
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66",
        "security_answer_two": "importa66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'].startswith('El usuario no pudo ser registrado.')


def test_user_empty_credenciales(client):
    login_data = {
        "username": "",
        "password": generate_password_hash(""),
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')

    assert response.json['message'] == 'Username y password son requeridos'


def test_user_login_success(client):
    login_data = {
        "username": "guille",
        "password": "aguanteBoquita",
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'].startswith('Login exitoso')



def test_user_login_user_not_found(client):
    login_data = {
        "username": "lucass",
        "password": "lucaspass"
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'] == 'Usuario no encontrado'


# si la base de datos esta vacia todo ok,si ya tiene gente fijarse en una id valido.
def test_get_user(client):
    response = client.get('/user/1')
    assert response.status_code == 200
    assert 'username' in response.json

# si la base de datos esta vacia todo ok,si ya tiene gente fijarse en una id valido.
def test_get_user_not_found(client):
    response = client.get('/user/1')
    assert response.status_code == 404
    assert 'username' not in response.json

def test_update_password_success(client):
    update_data = {
        "username": "guille",
        "password": generate_password_hash("aguanteBoquitaa"),
        "security_answer_one": "queti",
        "security_answer_two": "importa"
    }
    response = client.patch('/update_password', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Se cambio la contraseña correctamente.'

def test_update_password_user_not_found(client):
    update_data = {
        "username": "guille50",
        "password": generate_password_hash("aguanteBoquitaa"),
        "security_answer_one": "queti",
        "security_answer_two": "importa"
    }
    response = client.patch('/update_password', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'] == 'El usuario no existe.'

def test_update_password_security_answers_incorrect(client):
    update_data = {
        "username": "guille",
        "password": generate_password_hash("aguanteBoquita"),
        "security_answer_one": "importa",
        "security_answer_two": "queti"
    }
    response = client.patch('/update_password', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 401
    assert response.json['message'] == 'Las respuestas a las preguntas de seguridad son incorrectas.'


def test_create_post_success(client):
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

def test_create_post_incomplete_data(client):
    new_post = {
        "username": "guille",
        "category": "ANIMALS",
        "title": "HOLA"
    }
    response = client.post('/create_post', data=json.dumps(new_post), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Faltan datos en la solicitud')

def test_create_post_user_not_found(client):
    new_post = {
        "username": "guille5555",
        "category": "ANIMALS",
        "title": "HOLA",
        "post": "test_post",
        "image_link": "test_image_link"
    }
    response = client.post('/create_post', data=json.dumps(new_post), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('El usuario no existe')

def test_create_multiple_posts_success(client):
    for post in posts.posts:
        response = client.post('/create_post', data=json.dumps(post), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'].startswith('se ha agregado correctamente')


def test_get_post_by_category(client):
    response = client.get('/get_posts/Animalitos')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_last_posts(client):
    response = client.get('/get_last_posts')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert len(response.json) <= 6

#lo mismo que en otros test, debe verificarse que el id del post a probar sea valido
def test_create_response_incomplete_data(client):
    new_response = {
        "username": "guille",
        "post": "test_post",
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Faltan datos en la solicitud')

#lo mismo que en otros test, debe verificarse que el id del post a probar sea valido
def test_create_response_user_not_found(client):
    new_response = {
        "username": "guille5555",
        "post": "test_post",
        "id_post": 1,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('El usuario con nombre')

#lo mismo que en otros test, debe verificarse que el id del post a probar sea valido
def test_create_response_success(client):
    new_response = {
        "username": "guille",
        "post": "test_post",
        "id_post": 42,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'].startswith('se ha agregado correctamente')

#lo mismo que en otros test, debe verificarse que el id del post a probar sea valido
def test_create_response_post_not_found(client):
    new_response = {
        "username": "guille",
        "post": "test_post",
        "id_post": 1,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Se ha producido un error')
#lo mismo que en otros test, debe verificarse que el id del post a probar sea valido
def test_get_responses_success(client):
    response = client.get('/get_responses/42')
    assert response.status_code == 200
    assert len(response.json) > 0

