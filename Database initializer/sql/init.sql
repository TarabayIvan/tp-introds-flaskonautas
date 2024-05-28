CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(25) NOT NULL,
    password VARCHAR(60) NOT NULL,
    security_answer_one VARCHAR(50),
    security_answer_two VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS threads (
    id_post INT AUTO_INCREMENT PRIMARY KEY,
	id_user INT,
    category VARCHAR(25) NOT NULL,
    title VARCHAR(100) NOT NULL,
	post VARCHAR(255) NOT NULL,
    image_link VARCHAR(50),
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);

CREATE TABLE IF NOT EXISTS responses (
	id_comment INT AUTO_INCREMENT PRIMARY KEY,
	id_user INT,
    id_post INT,
    post VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_post) REFERENCES threads(id_post)
);

INSERT INTO users VALUES (NULL, 'usuario 1', 'contra123', 'respuesta uno', 'respuesta 2');
INSERT INTO users VALUES (NULL, 'usuario 2', 'contra123', 'respuesta uno', 'respuesta 2');

INSERT INTO threads VALUES (NULL, 1, 'comida', 'RECETA 1', 'texto post', '/image.png');

INSERT INTO responses VALUES (NULL, 2, 1, 'respuesta a thread 1');
