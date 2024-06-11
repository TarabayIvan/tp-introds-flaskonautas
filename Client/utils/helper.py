from PIL import Image
import secrets #libreria de python para generar nombre random
import os

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

def save_image(image, current_app):
    _, f_ext = os.path.splitext(image.filename) #divide el nombre de la imagen en 2, el nombre puro que no nos interesa y la extension
    if f_ext not in ALLOWED_EXTENSIONS: # verifica que la extension esta permitida
        return None
    random_hex = secrets.token_hex(8) #crea un nombre random para la imagen
    image_fn = random_hex + f_ext #une el nombre random con la extension
    image_path = os.path.join(current_app.root_path, 'static', 'images', 'posts-images', image_fn) #crea la ruta completa de la imagen
    image.save(image_path)
    try:
        Image.open(image_path) #verifica que es una imagen valida
        return image_fn
    except IOError:
        os.remove(image_path)
        return None
