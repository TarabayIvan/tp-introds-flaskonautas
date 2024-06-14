import json
from werkzeug.security import generate_password_hash
import users
import posts


def test_register_user_success(client):
    """
    Test para registrar un usuario correctamente.
    """
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
    """
    Test para registrar multiples usuarios correctamente.
    """
    for user in users.users:
        response = client.post('/register_user', data=json.dumps(user), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'] == 'El usuario se registro correctamente.'


def test_register_user_incomplete_data(client):
    """
    Test para registrar un usuario con datos incompletos.
    """
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'No se enviaron todos los datos necesarios por JSON'


def test_register_user_empy_data_password(client):
    """
    Test para registrar un usuario con datos vacios.
    """
    new_user = {
        "username": "guille66",
        "password": generate_password_hash(""),
        "security_answer_one": "queti66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'No se enviaron todos los datos necesarios por JSON'


def test_register_duplicate_users(client):
    """
    Test para registrar un usuario ya registrado.
    """
    new_user = {
        "username": "guille66",
        "password": generate_password_hash("testpassword66"),
        "security_answer_one": "queti66",
        "security_answer_two": "importa66"
    }
    response = client.post('/register_user', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('El usuario no pudo ser registrado.')


def test_user_empty_credenciales(client):
    """
    Test para loguear un usuario con credenciales vacias.

    """
    login_data = {
        "username": "",
        "password": generate_password_hash(""),
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')

    assert response.json['message'] == 'Username y password son requeridos'


def test_user_login_success(client):
    """
    Test para loguear un usuario correctamente.
    """
    login_data = {
        "username": "guille",
        "password": "aguanteBoquita",
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200


def test_user_login_user_not_found(client):
    """
    Test para loguear un usuario que no existe.
    """
    login_data = {
        "username": "lucass",
        "password": "lucaspass"
    }
    response = client.post('/login_user', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'] == 'Usuario no encontrado'


def test_get_user(client):
    """
    Test para obtener un usuario registrado en la BBDD.
    """
    response = client.get('/user/222')
    assert response.status_code == 200
    assert 'username' in response.json


def test_get_user_not_found(client):
    """
    Test para obtener un usuario que no existe en la BBDD.
    """
    response = client.get('/user/1')
    assert response.status_code == 404
    assert 'username' not in response.json


def test_update_password_success(client):
    """
    Test para actualizar la contraseña de un usuario correctamente.
    """
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
    """
    Test para actualizar la contraseña de un usuario que no existe.
    """
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
    """
    Test para actualizar la contraseña de un usuario con respuestas de seguridad incorrectas.
    """
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
    """
    Test para crear un post correctamente.
    """
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
    """
    Test para crear un post con datos incompletos.
    """
    new_post = {
        "username": "guille",
        "category": "ANIMALS",
        "title": "HOLA"
    }
    response = client.post('/create_post', data=json.dumps(new_post), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Faltan datos en la solicitud')


def test_create_post_user_not_found(client):
    """
    Test para crear un post con un usuario que no existe en la BBDD.
    """
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
    """
    Test para crear multiples posts correctamente.
    """
    for new_post in posts.posts:
        response = client.post('/create_post', data=json.dumps(new_post), content_type='application/json')
        assert response.status_code == 201
        assert response.json['message'].startswith('se ha agregado correctamente')


def test_get_post_by_category(client):
    """
    Test para obtener posts por categoria.
    """
    response = client.get('/get_posts/Animalitos')
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_last_posts(client):
    """
    Test para obtener los ultimos posts.
    """
    response = client.get('/get_last_posts')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert len(response.json) <= 6


def test_create_response_incomplete_data(client):
    """
    Test para crear una respuesta con datos incompletos.
    """
    new_response = {
        "username": "guille",
        "post": "test_post",
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Faltan datos en la solicitud')


def test_create_response_user_not_found(client):
    """
    Test para crear una respuesta con un usuario que no existe.
    """
    new_response = {
        "username": "guille5555",
        "post": "test_post",
        "id_post": 1,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('El usuario con nombre')


def test_create_response_success(client):
    """
    Test para crear una respuesta correctamente.
    """
    new_response = {
        "username": "guille",
        "post": "test_post",
        "id_post": 52,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'].startswith('se ha agregado correctamente')


def test_create_response_post_not_found(client):
    """
    Test para crear una respuesta con un post que no existe.
    """
    new_response = {
        "username": "guille",
        "post": "test_post",
        "id_post": 1,
    }
    response = client.post('/create_response', data=json.dumps(new_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Se ha producido un error')


def test_get_responses_success(client):
    """
    Test para obtener el post con sus respuestas correctamente.
    """
    response = client.get('/get_complete_post/52')
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_responses_post_incorrect(client):
    """
    Test para obtener el post con sus respuestas sin un id de post.
    """
    response = client.get('/get_complete_post/')
    assert response.status_code == 404


def test_get_responses_post_not_found(client):
    """
    Test para obtener el post con sus respuestas con un id de post que no existe.
    """
    response = client.get('/get_complete_post/1')
    assert response.status_code == 404
    assert response.json['message'].startswith('No se ha encontrado el post')


def test_delete_user_success(client):
    """
    Test para borrar un usuario correctamente.
    """
    user_delete_data = {
        "username": "guille66",
        "password": "testpassword66",
    }
    response = client.delete('/delete_user', data=json.dumps(user_delete_data), content_type='application/json')
    assert response.status_code == 200


def test_delete_user_user_incomplete(client):
    """
    Test para borrar un usuario con datos incompletos.
    """
    user_delete_data = {
        "username": "guille",
    }
    response = client.delete('/delete_user', data=json.dumps(user_delete_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('No se enviaron todos los datos necesarios por JSON')


def test_delete_user_password_invalid(client):
    """
    Test para borrar un usuario con una contraseña inválida.
    """
    user_delete_data = {
        "username": "guille",
        "password": "aguanteBoquita1",
    }
    response = client.delete('/delete_user', data=json.dumps(user_delete_data), content_type='application/json')
    assert response.status_code == 403
    assert response.json['message'].startswith('La contraseña no coincide con la del usuario')


def test_update_post_success(client):
    """
    Test para actualizar un post correctamente.
    """
    update_post = {
        "title": "HOLA",
        "post": "test_post",
        "username": "guille",
    }
    response = client.patch('/update_post/52', data=json.dumps(update_post), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'].startswith('Esta actualizado correctamente')


def test_update_post_incomplete_data(client):
    """
    Test para actualizar un post con datos incompletos.
    """
    update_post = {
        "title": "HOLA",
    }
    response = client.patch('/update_post/1', data=json.dumps(update_post), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Se deben proporcionar el title y el post')


def test_update_post_user_not_found(client):
    """
    Test para actualizar un post con un usuario que no existe.
    """
    update_post = {
        "title": "HOLA",
        "post": "test_post",
        "username": "guille5555s",
    }
    response = client.patch('/update_post/52', data=json.dumps(update_post), content_type='application/json')
    assert response.status_code == 403
    assert response.json['message'].startswith('No es el usuario correcto')


def test_update_response_success(client):
    """
    Test para actualizar una respuesta correctamente.
    """
    update_response = {
        "id_response": 7,
        "post": "test_post 666",
    }
    response = client.patch('/update_response', data=json.dumps(update_response), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'].startswith('se ha actualizado correctamente')


def test_update_response_incomplete_data(client):
    """
    Test para actualizar una respuesta con datos incompletos.
    """
    update_response = {
        "post": "test_post",
    }
    response = client.patch('/update_response', data=json.dumps(update_response), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'].startswith('Faltan datos en la solicitud')


def test_update_response_not_found(client):
    """
    Test para actualizar una respuesta que no existe.
    """
    update_response = {
        "id_response": 100,
        "post": "test_post",
    }
    response = client.patch('/update_response', data=json.dumps(update_response), content_type='application/json')

    assert response.json['message'].startswith('Se ha producido un error')


def test_delete_response_success(client):
    """
    Test para borrar una respuesta correctamente.
    """
    delete_response = {
        "username": "guille"
    }
    response = client.delete('/delete_response/7', data=json.dumps(delete_response), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'].startswith('La respuesta ha sido eliminada correctamente')


def test_delete_response_not_found(client):
    """
    Test para borrar una respuesta que no existe.
    """
    delete_response = {
        "username": "guille"
    }
    response = client.delete('/delete_response/70', data=json.dumps(delete_response), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'].startswith('La respuesta no existe')


def test_delete_response_incorrect(client):
    """
    Test para borrar una respuesta con un usuario incorrecto.
    """
    delete_response = {
        "username": "guille5"
    }
    response = client.delete('/delete_response/10', data=json.dumps(delete_response), content_type='application/json')
    assert response.status_code == 403
    assert response.json['message'].startswith('No tienes permiso para borrar esta respuesta')


def test_delete_post_success(client):
    """
    Test para borrar un post correctamente.
    """
    delete_post = {
        "username": "guille"
    }
    response = client.delete('/delete_post/55', data=json.dumps(delete_post), content_type='application/json')
    assert response.status_code == 200


def test_delete_post_not_found(client):
    """
    Test para borrar un post que no existe.
    """
    delete_post = {
        "username": "guille"
    }
    response = client.delete('/delete_post/10000', data=json.dumps(delete_post), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'].startswith('El post no existe')


def test_delete_post_incorrect_user(client):
    """
    Test para borrar un post con un usuario incorrecto.
    """
    delete_post = {
        "username": "guillert"
    }
    response = client.delete('/delete_post/52', data=json.dumps(delete_post), content_type='application/json')
    assert response.status_code == 403
    assert response.json['message'].startswith('No tienes permiso para borrar este post')
