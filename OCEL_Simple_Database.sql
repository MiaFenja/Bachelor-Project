#CREATE DATABASE OCEL;
USE OCEL;

DROP TABLE IF EXISTS event_;
DROP TABLE IF EXISTS event_map_type;
DROP TABLE IF EXISTS object;
DROP TABLE IF EXISTS object_map_type;
DROP TABLE IF EXISTS object_object;
DROP TABLE IF EXISTS event_object;
DROP TABLE IF EXISTS event_ReceiveOrder;
DROP TABLE IF EXISTS event_PackOrder;
DROP TABLE IF EXISTS event_SendOrder;
DROP TABLE IF EXISTS event_ReturnOrder;
DROP TABLE IF EXISTS object_OrderForm;
DROP TABLE IF EXISTS object_Book;
DROP TABLE IF EXISTS object_Package;




CREATE TABLE event_map_type (
	ocel_type varchar(50),
    ocel_type_map varchar(50),
    PRIMARY KEY (ocel_type)
);

CREATE TABLE event_ (
	ocel_id varchar(50),
    ocel_type varchar(50),
    PRIMARY KEY (ocel_id),
    FOREIGN KEY (ocel_type) REFERENCES event_map_type (ocel_type)
);

CREATE TABLE object_map_type (
	ocel_type varchar(50),
    ocel_type_map varchar(50),
    PRIMARY KEY (ocel_type)
);

CREATE TABLE object (
	ocel_id varchar(50),
    ocel_type varchar(50),
    PRIMARY KEY (ocel_id),
    FOREIGN KEY (ocel_type) REFERENCES object_map_type (ocel_type)
);


CREATE TABLE object_object (
	ocel_source varchar(50),
    ocel_target varchar(50),
    ocel_qualifier varchar(50),
    PRIMARY KEY (ocel_source, ocel_target, ocel_qualifier)
);

CREATE TABLE event_object (
	ocel_event varchar(50),
    ocel_object varchar(50),
    ocel_qualifier varchar(50),
    PRIMARY KEY ( ocel_event, ocel_object, ocel_qualifier)
);

CREATE TABLE event_ReceiveOrder (
	ocel_id varchar(50),
    ocel_time DATETIME,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE event_PackOrder (
	ocel_id varchar(50),
    ocel_time DATETIME,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE event_SendOrder (
	ocel_id varchar(50),
    ocel_time DATETIME,
    completed BOOLEAN,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE event_ReturnOrder (
	ocel_id varchar(50),
    ocel_time DATETIME,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE object_OrderForm (
	ocel_id varchar(50),
    ocel_time DATETIME,
    number_of_items INT,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE object_Book (
	ocel_id varchar(50),
    ocel_time DATETIME,
    wight INT,
    price INT,
    PRIMARY KEY (ocel_id)
);

CREATE TABLE object_Package (
	ocel_id varchar(50),
    ocel_time DATETIME,
    delivered BOOLEAN,
    PRIMARY KEY (ocel_id)
);

# Insertion 

INSERT event_map_type VALUES
('Receive Order','ReceiveOrder'),
('Pack Order','PackOrder'),
('Send Order','SendOrder'),
('Return Order','ReturnOrder');

INSERT event_ VALUES
('rec_order1 ','Receive Order'),
('rec_order2','Receive order'),
('pack_order1','Pack order'),
('pack_order2','Pack order'),
('send_order1','send order'),
( 'send_order2','send order');

Insert object_map_type values
('Order Form','OrderForm'),
('Book','Book'),
('Package','Package');

Insert object values
('pack1','package'),
('pack2','package'),
('book1','book'),
('book2','book'),
('order_form1','Order Form'),
('order_form2','Order Form');

Insert object_object values

('book1','pack1','book in package'),

('book2','pack2','book in package');


Insert event_object values
('pack_order1'
,'pack1', 'create package'),
('pack_order2',
'pack2','create package');

insert event_ReceiveOrder values
('rec_order1',"2023-08-15 19:30:10"),
('rec_order2', "2023-08-16 07:22:36");

insert event_PackOrder  values
('pack_order1',"2023-08-16 12:02:01"),
('pack_order2',"2023-08-16 12:07:59");

insert event_SendOrder values
('send_order1',"2023-08-16 12:11:14", true),
('end_order2', "2023-08-16 12:12:03",false);

insert object_OrderForm values
('order_form1', "2023-08-16 12:00:09",1),
('order_form2',"2023-08-16 11:33:17",3);

insert object_Book values
('book1',"2023-08-16 13:59:41",1,99),
('book2', "2023-08-16 12:27:29", 1,99);

insert object_Package values
('pack1',"2023-08-16 15:54:37",true),
('pack2',"2023-08-16 16:13:58",false);










