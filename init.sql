CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO roles (name) VALUES
    ('STANDARD'),
    ('MANAGER');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    address VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER DEFAULT 1,
    telegram_chat_id VARCHAR(255),
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

