DROP DATABASE timeTester;
CREATE DATABASE timeTester;
USE timeTester;

CREATE TABLE IF NOT EXISTS event_map_type (
	ocel_type VARCHAR(50),
    ocel_type_map VARCHAR(50),
    PRIMARY KEY (ocel_type)
);

CREATE TABLE IF NOT EXISTS event (
	ocel_id VARCHAR(50),
    ocel_type VARCHAR(50),
    PRIMARY KEY (ocel_id),
    FOREIGN KEY (ocel_type) REFERENCES event_map_type (ocel_type)
);

CREATE TABLE IF NOT EXISTS object_map_type (
	ocel_type VARCHAR(50),
    ocel_type_map VARCHAR(50),
    PRIMARY KEY (ocel_type)
);

CREATE TABLE IF NOT EXISTS object (
	ocel_id VARCHAR(50),
    ocel_type VARCHAR(50),
    PRIMARY KEY (ocel_id),
    FOREIGN KEY (ocel_type) REFERENCES object_map_type (ocel_type)
);


CREATE TABLE IF NOT EXISTS object_object (
	ocel_source_id VARCHAR(50),
    ocel_target_id VARCHAR(50),
    ocel_qualifier VARCHAR(50),
    PRIMARY KEY (ocel_source_id, ocel_target_id, ocel_qualifier)
);

CREATE TABLE IF NOT EXISTS event_object (
	ocel_event_id VARCHAR(50),
    ocel_object_id VARCHAR(50),
    ocel_qualifier VARCHAR(50),
    PRIMARY KEY (ocel_event_id, ocel_object_id, ocel_qualifier)
);

CREATE TABLE IF NOT EXISTS event_ReceiveOrder (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    FOREIGN KEY (ocel_id) REFERENCES event(ocel_id)
);

CREATE TABLE IF NOT EXISTS event_PackOrder (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    FOREIGN KEY (ocel_id) REFERENCES event(ocel_id)
);

CREATE TABLE IF NOT EXISTS event_SendOrder (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    completed BOOLEAN,
    FOREIGN KEY (ocel_id) REFERENCES event(ocel_id)
);

CREATE TABLE IF NOT EXISTS event_ReturnOrder (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    FOREIGN KEY (ocel_id) REFERENCES object(ocel_id)
);

CREATE TABLE IF NOT EXISTS object_OrderForm (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    number_of_items INT,
    FOREIGN KEY (ocel_id) REFERENCES object(ocel_id)
);

CREATE TABLE IF NOT EXISTS object_Book (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    weight INT,
    price INT,
    FOREIGN KEY (ocel_id) REFERENCES object(ocel_id)
);

CREATE TABLE IF NOT EXISTS object_Package (
	ocel_id VARCHAR(50),
    ocel_time DATETIME,
    delivered BOOLEAN,
    FOREIGN KEY (ocel_id) REFERENCES object(ocel_id)
);

# Insertion 

INSERT INTO event_map_type VALUES
('Receive Order','ReceiveOrder'),
('Pack Order','PackOrder'),
('Send Order','SendOrder'),
('Return Order','ReturnOrder');

INSERT INTO event VALUES
('rec_order1','Receive Order'),
('rec_order2','Receive Order'),
('pack_order1','Pack Order'),
('pack_order2','Pack Order'),
('send_order1','Send Order'),
( 'send_order2','Send Order');

Insert INTO object_map_type values
('Order Form','OrderForm'),
('Book','Book'),
('Package','Package');

Insert INTO object values
('pack1','Package'),
('pack2','Package'),
('book1','Book'),
('book2','Book'),
('order_form1','Order Form'),
('order_form2','Order Form');

Insert INTO object_object values

('book1','pack1','book in package'),

('book2','pack2','book in package');


Insert INTO event_object values
('pack_order1'
,'pack1', 'create package'),
('pack_order2',
'pack2','create package');

insert INTO event_ReceiveOrder values
('rec_order1','2023-08-15 19:30:10'),
('rec_order2', '2023-08-16 07:22:36');

insert INTO event_PackOrder  values
('pack_order1','2023-08-16 12:02:01'),
('pack_order2','2023-08-16 12:07:59');

insert INTO event_SendOrder values
('send_order1','2023-08-16 12:11:14', 1),
('send_order2', '2023-08-16 12:12:03',0);

insert INTO object_OrderForm values
('order_form1', '2023-08-15 19:30:10',1),
('order_form2','2023-08-16 07:22:36',3);

insert INTO object_Book values
('book1','2023-08-16 13:59:41',1,99),
('book2', '2023-08-16 12:27:29', 1,99);

insert INTO object_Package values
('pack1','2023-08-16 12:02:01',1),
('pack2','2023-08-16 12:07:59',0);


COMMIT;


