CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO roles (name) VALUES
    ('STANDARD'),
    ('MANAGER');

CREATE TABLE IF NOT EXISTS users (
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

CREATE TYPE status AS ENUM ('APPROVED', 'CANCELED', 'ON_MODERATION');

CREATE TABLE IF NOT EXISTS moderation_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    manager_id INTEGER REFERENCES users (id) DEFAULT NULL,
    status status DEFAULT 'ON_MODERATION',
    fields_to_change JSONB
);
