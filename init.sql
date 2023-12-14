CREATE TABLE "Role" (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    phone_number VARCHAR UNIQUE,
    first_name VARCHAR,
    last_name VARCHAR,
    address VARCHAR,
    password VARCHAR NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER DEFAULT 1,
    FOREIGN KEY (role_id) REFERENCES "Role" (id)
);


INSERT INTO "Role" (name) VALUES
    ('standard user'),
    ('moderator');
