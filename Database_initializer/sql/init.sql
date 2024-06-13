CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(250) NOT NULL,
    security_answer_one VARCHAR(50),
    security_answer_two VARCHAR(50),
    UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS posts (
    id_post INT AUTO_INCREMENT PRIMARY KEY,
	id_user INT,
    category VARCHAR(25) NOT NULL,
    title VARCHAR(100) NOT NULL,
	post VARCHAR(255) NOT NULL,
    image_link VARCHAR(50),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS responses (
	id_response INT AUTO_INCREMENT PRIMARY KEY,
	id_user INT,
    id_post INT,
    post VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE
);