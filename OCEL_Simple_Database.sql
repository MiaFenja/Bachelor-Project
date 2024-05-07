BEGIN TRANSACTION;


CREATE TABLE IF NOT EXISTS "event_map_type" (
	`ocel_type` TEXT,
    `ocel_type_map` TEXT,
    PRIMARY KEY (`ocel_type`)
);

CREATE TABLE IF NOT EXISTS "event" (
	`ocel_id` TEXT,
    `ocel_type` TEXT,
    PRIMARY KEY (`ocel_id`),
    FOREIGN KEY (`ocel_type`) REFERENCES event_map_type (`ocel_type`)
);

CREATE TABLE IF NOT EXISTS "object_map_type" (
	`ocel_type` TEXT,
    `ocel_type_map` TEXT,
    PRIMARY KEY (`ocel_type`)
);

CREATE TABLE IF NOT EXISTS "object" (
	`ocel_id` TEXT,
    `ocel_type` TEXT,
    PRIMARY KEY (`ocel_id`),
    FOREIGN KEY (`ocel_type`) REFERENCES object_map_type (`ocel_type`)
);


CREATE TABLE IF NOT EXISTS "object_object" (
	`ocel_source_id` TEXT,
    `ocel_target_id` TEXT,
    `ocel_qualifier` TEXT,
    PRIMARY KEY (`ocel_source_id`, `ocel_target_id`, `ocel_qualifier`)
);

CREATE TABLE IF NOT EXISTS "event_object" (
	`ocel_event_id` TEXT,
    `ocel_object_id` TEXT,
    `ocel_qualifier` TEXT,
    PRIMARY KEY (`ocel_event_id`, `ocel_object_id`, `ocel_qualifier`)
);

CREATE TABLE IF NOT EXISTS "event_ReceiveOrder" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "event_PackOrder" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "event_SendOrder" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    `completed` BOOLEAN,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "event_ReturnOrder" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "object_OrderForm" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    `number_of_items` INT,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "object_Book" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    `weight` INT,
    `price` INT,
    PRIMARY KEY (`ocel_id`)
);

CREATE TABLE IF NOT EXISTS "object_Package" (
	`ocel_id` TEXT,
    `ocel_time` TIMESTAMP,
    `delivered` BOOLEAN,
    PRIMARY KEY (`ocel_id`)
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
('rec_order1',"2023-08-15T19:30:10.000Z"),
('rec_order2', "2023-08-16T07:22:36.000Z");

insert INTO event_PackOrder  values
('pack_order1',"2023-08-16T12:02:01.000Z"),
('pack_order2',"2023-08-16T12:07:59.000Z");

insert INTO event_SendOrder values
('send_order1',"2023-08-16T12:11:14.000Z", 1),
('send_order2', "2023-08-16T12:12:03.000Z",0);

insert INTO object_OrderForm values
('order_form1', "2023-08-16T12:00:09.000Z",1),
('order_form2',"2023-08-16T11:33:17.000Z",3);

insert INTO object_Book values
('book1',"2023-08-16T13:59:41.000Z",1,99),
('book2', "2023-08-16T12:27:29.000Z", 1,99);

insert INTO object_Package values
('pack1',"2023-08-16T15:54:37.000Z",1),
('pack2',"2023-08-16T16:13:58.000Z",0);


COMMIT;







