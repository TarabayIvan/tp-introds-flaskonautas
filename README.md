# Foro "Los Flaskonautas"

Trabajo práctico para la materia "Introducción al desarrollo de software" de la Facultad de Ingeniería de la Universidad de Buenos Aires.

## Presentation

This project is a practical work for the "Introduction to Software Development" course at the Faculty of Engineering, University of Buenos Aires. It involves creating a full-fledged web application using Flask.

## Features

- Complete API functionality
- User-friendly client interface
- Database initialization and management

## Front End Installation Guide

1. Clone the repository:
    ```bash
    git clone https://github.com/TarabayIvan/tp-introds-flaskonautas.git
    cd tp-introds-flaskonautas
    cd Client
    ```

2. Create a virtual environment for the front end and activate it:
    ```bash
    pipenv shell
    ```

3. Install the required dependencies:
    ```bash
    pipenv install -r requirements_front.txt
    ```

4. Run the frontend:
    ```bash
    flask run
    ```

## Back End Installation Guide

1. Clone the repository:
    ```bash
    git clone https://github.com/TarabayIvan/tp-introds-flaskonautas.git
    cd tp-introds-flaskonautas
    cd API
    ```

2. Create a virtual environment for the back end and activate it:
    ```bash
    pipenv shell
    ```

3. Install the required dependencies:
    ```bash
    pipenv install -r requirements_api.txt
    ```

4. Run the back end:
    ```bash
    flask run -p 5001
    ```

5. Initialize the database:
    ```bash
    python database_initializer/init_db.py
    ```

## DB Installation Guide

1. Create the container:
    ```bash
    cd Database_initializer
    cd docker
    docker-compose up --build -d
    ```

2. Connect to the MySQL database:
    ```bash
    docker exec -it docker-db-1 mysql -u root -p
    ```

## Dependencies

- Flask
- SQLAlchemy
- Pillow
- Werkzeug
- dotenv
- requests

## API Endpoints

- `POST /register_user`: Registrar un nuevo usuario.
- `POST /login_user`: Iniciar sesión de usuario.
- `POST /get_user`: Obtener información de usuario.
- `POST /update-password`: Actualizar la contraseña del usuario.
- `POST /create_post`: Crear una nueva publicación.
- `POST /get_posts`: Obtener todas las publicaciones.
- `POST /get_last_posts`: Obtener las publicaciones más recientes.
- `POST /create_response`: Crear una nueva respuesta a una publicación.
- `POST /get_complete_post`: Obtener una publicación con todas sus respuestas.(corregir no envia un erorr si un post es invalido).
- `POST /delete_user`: Eliminar un usuario.
- `PUT /update_post`: Actualizar una publicación.
- `PATCH /update_response`: Actualizar una respuesta.
- `DELETE /delete_post`: Eliminar una publicación.
- `DELETE /delete_response`: Eliminar una respuesta.