-- Create tables for Café WatSPEED database

CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    table_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    people_count INT NOT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (table_id) REFERENCES tables(id)
);

CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    size VARCHAR(50) NOT NULL,
    price DECIMAL(5,2) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    menu_id INT NOT NULL,
    quantity INT NOT NULL,
    order_time TIMESTAMP NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(id)
);