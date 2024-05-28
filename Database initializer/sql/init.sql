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