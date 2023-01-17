DROP TABLE order_dish_odh;
DROP TABLE dish_dsh;
DROP TABLE order_ord;
DROP TABLE table_tbl;
DROP TABLE waiter_wtr;

CREATE TABLE IF NOT EXISTS table_tbl (
	id_tbl INTEGER PRIMARY KEY AUTOINCREMENT,
	tbl_num INTEGER
);

CREATE TABLE IF NOT EXISTS waiter_wtr (
	id_wtr INTEGER PRIMARY KEY AUTOINCREMENT,
	wtr_firstname VARCHAR,
	wtr_lastname VARCHAR
);

CREATE TABLE IF NOT EXISTS order_ord (
	id_ord INTEGER PRIMARY KEY AUTOINCREMENT,
	ord_ref VARCHAR, 
	ord_hour DATE,
	id_wtr INTEGER ,
	id_tbl INTEGER,
	FOREIGN KEY (id_wtr) REFERENCES id_wtr(waiter_wtr),
	FOREIGN KEY (id_tbl) REFERENCES id_tbl(table_tbl)
);

CREATE TABLE IF NOT EXISTS dish_dsh (
	id_dsh INTEGER PRIMARY KEY AUTOINCREMENT,
	dsh_name VARCHAR,
	dsh_price FLOAT
);

CREATE TABLE IF NOT EXISTS order_dish_odh (
	id_odh INTEGER PRIMARY KEY AUTOINCREMENT,
	id_dsh INTEGER,
	id_ord INTEGER,
	FOREIGN KEY (id_dsh) REFERENCES id_dsh(dish_dsh),
	FOREIGN KEY (id_ord) REFERENCES id_ord(order_ord)
);


INSERT INTO dish_dsh (dsh_name, dsh_price) VALUES
('Spaghetti',10.0),
('Antispasto',3.0),
('PizzaDeMama',14.0),
('Tiramisu',8.0);

INSERT INTO table_tbl (tbl_num) VALUES
(1),(2),(3),(4),(5),(6);

INSERT INTO waiter_wtr(wtr_firstname, wtr_lastname) VALUES
("jean","bon");

