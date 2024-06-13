# Proyecto de API Flask

## Guía de Uso

### Instalación de Requerimientos

1. Instala los requerimientos necesarios con el siguiente comando:

    ```bash
    pip install -r requirements.txt
    ```

### Pruebas

2. Puedes probar cada test por separado en tu IDE. Asegúrate de que los IDs utilizados en los tests que los requieran sean válidos.

3. Para ejecutar todos los tests juntos, utiliza el siguiente comando:

    ```bash
    pytest
    ```

### Endpoints Disponibles

- `POST /register_user`: Registrar un nuevo usuario.
- `POST /login_user`: Iniciar sesión de usuario.
- `GET /get_user`: Obtener información de usuario.
- `PATCH /update-password`: Actualizar la contraseña del usuario.
- `POST /create_post`: Crear una nueva publicación.
- `GET /get_posts`: Obtener todas las publicaciones.
- `GET /get_last_posts`: Obtener las publicaciones más recientes.
- `POST /create_response`: Crear una nueva respuesta a una publicación.
- `GET /get_complete_post`: Obtener una publicación con todas sus respuestas.(corregir no envia un erorr si un post es invalido)
- `DELETE /delete_user`: Eliminar un usuario.
---

### Enpoints que no funcionan
- `PUT /update_post`: Actualizar una publicación.
- `PATCH /update_response`: Actualizar una respuesta.
- `DELETE /delete_post`: Eliminar una publicación.
- `DELETE /delete_response`: Eliminar una respuesta.

¡Gracias por usar nuestra API Flask! Si tienes alguna pregunta o encuentras algún problema, no dudes en contactarnos.
```
The Flaskonauts
```