-- DROP TABLE tbl_ord;
-- DROP TABLE dish_dsh;
-- DROP TABLE order_ord;
-- DROP TABLE table_tbl;


-- CREATE TABLE IF NOT EXISTS table_tbl (
-- 	id_tbl INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	tbl_num INTEGER,
-- 	fk_tbl_ord INTEGER,
-- 	FOREIGN KEY (fk_tbl_ord) REFERENCES tbl_ord(tbl_id)
-- );

-- CREATE TABLE IF NOT EXISTS tbl_ord (
-- 	tbl_id INTEGER,
-- 	ord_id INTEGER,
-- 	PRIMARY KEY(tbl_id, ord_id)
-- );

-- CREATE TABLE IF NOT EXISTS order_ord (
-- 	id_ord INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	ord_ref VARCHAR, 
-- 	ord_hour DATE,
-- 	fk_ord_tbl INTEGER,
-- 	FOREIGN KEY (fk_ord_tbl) REFERENCES tbl_ord(tbl_ord)
-- );

-- CREATE TABLE IF NOT EXISTS dish_dsh (
-- 	id_dsh INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	dsh_name VARCHAR,
-- 	dsh_price FLOAT,
-- 	fk_dsh_ord INTEGER,
-- 	FOREIGN KEY (fk_dsh_ord) REFERENCES order_tbl(dish_dsh)
-- );

INSERT INTO dish_dsh (dsh_name, dsh_price, fk_dsh_ord) VALUES
('Spaghetti',10.0,1),
('Antispasto',3.0,1),
('PizzaDeMama',14.0,1),
('Tiramisu',8.0,2);

INSERT INTO table_tbl (tbl_num) VALUES
(1),(2),(3),(4),(5),(6);

INSERT INTO order_ord (ord_ref, ord_hour, fk_ord_tbl) VALUES
('REF_123456','2007-01-01 10:00:00',1),
('REF_123457','2007-01-01 10:00:00',2),
('REF_123458','2007-01-01 10:00:00',3);
