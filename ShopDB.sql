-- ShopDB
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, balance REAL NOT NULL DEFAULT 0, date_created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL, sale REAL NOT NULL DEFAULT 0, date_created TEXT NOT NULL);

INSERT INTO users VALUES (1,'Ivan Petrov','ivan.petrov@example.com',15000,'2025-10-01');
INSERT INTO users VALUES (2,'Anna Smirnova','anna.smirnova@example.com',8200.50,'2025-10-02');
INSERT INTO users VALUES (3,'Maxim Ivanov','max.ivanov@example.com',4300.75,'2025-10-03');
INSERT INTO users VALUES (4,'Elena Kuznetsova','elena.k@example.com',12750,'2025-10-04');
INSERT INTO users VALUES (5,'Dmitry Sokolov','d.sokolov@example.com',6500.25,'2025-10-05');

INSERT INTO products VALUES (1,'Laptop',75000,10,'2025-10-01');
INSERT INTO products VALUES (2,'Smartphone',45000,5,'2025-10-02');
INSERT INTO products VALUES (3,'Headphones',8500,15,'2025-10-03');
INSERT INTO products VALUES (4,'Keyboard',6500,7.5,'2025-10-04');
INSERT INTO products VALUES (5,'Mouse',3200,12,'2025-10-05');

SELECT * FROM users;
SELECT * FROM products;
