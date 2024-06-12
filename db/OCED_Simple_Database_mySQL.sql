CREATE DATABASE timeTester;
USE timeTester;

CREATE TABLE IF NOT EXISTS event (
    eventID VARCHAR(50),
    eventType VARCHAR(50),
    timestamp DATETIME,
    PRIMARY KEY (eventID)
);

CREATE TABLE IF NOT EXISTS eventAttributeValue (
    eventID VARCHAR(50),
    eventAttributeName VARCHAR(50),
    eventAttributeValue VARCHAR(50),
    PRIMARY KEY (eventID, eventAttributeName)
);

CREATE TABLE IF NOT EXISTS eventObject (
    eventID VARCHAR(50),
    objectID VARCHAR(50),
    EOqualifier VARCHAR(50),
    PRIMARY KEY (eventID, objectID)
);

CREATE TABLE IF NOT EXISTS objectRelationEvent (
    objectObjectID VARCHAR(50),
    eventID VARCHAR(50),
    OOEqualifier VARCHAR(50),
    PRIMARY KEY (objectObjectID, eventID)
);

CREATE TABLE IF NOT EXISTS object (
    objectID VARCHAR(50),
    objectType VARCHAR(50),
    PRIMARY KEY (objectID)
);

CREATE TABLE IF NOT EXISTS objectObject (
    objectObjectID VARCHAR(50),
    fromObjectID VARCHAR(50),
    toObjectID VARCHAR(50),
    objectRelationType VARCHAR(50),
    PRIMARY KEY (objectObjectID)
);

CREATE TABLE IF NOT EXISTS objectAttributeValue (
    objectAttributeValueID VARCHAR(50),
    instanceID VARCHAR(50),
    objectID VARCHAR(50),
    objectAttributeName VARCHAR(50),
    objectAttributeValue VARCHAR(50),
    PRIMARY KEY (objectAttributeValueID)
);

CREATE TABLE IF NOT EXISTS objectAttributeValueEvent (
    eventID VARCHAR(50),
    objectAttributeValueID VARCHAR(50),
    OAEqualifier VARCHAR(50),
    PRIMARY KEY (eventID, objectAttributeValueID)
);

# Insertion 

INSERT INTO event VALUES
('vacuum1', 'Vacuum', '2024-03-20 10:30:18'),
('vacuum2', 'Vacuum', '2024-04-01 09:36:51'),
('make_bed1', 'Make Bed', '2024-03-20 10:40:33'),
('make_bed2', 'Make Bed', '2024-04-01 09:30:47'),
('clean_bathroom1', 'Clean Bathroom', '2024-03-20 10:45:03'),
('clean_bathroom2', 'Clean Bathroom', '2024-04-01 09:15:24');

INSERT INTO eventAttributeValue VALUES
('vacuum1', 'finished', '1'),
('vacuum2', 'finished', '0'),
('make_bed1', 'finished', '1'),
('make_bed2', 'finished', '1'),
('make_bed1', 'chocolate', '1'),
('make_bed2', 'chocolate', '0'),
('clean_bathroom1', 'finished', '1'),
('clean_bathroom2', 'finished', '1');

INSERT INTO object VALUES
('hotel_room1', 'Hotel Room'),
('hotel_room2', 'Hotel Room'),
('vacuum_cleaner1', 'Vacuum Cleaner'),
('cleaner1', 'Cleaner'),
('cleaner2', 'Cleaner'),
('cleaner3', 'Cleaner'),
('chocolate1', 'Chocolate'),
('chocolate2', 'Chocolate');

INSERT INTO eventObject VALUES
('vacuum1', 'vacuum_cleaner1', 'vacuum room'),
('vacuum2', 'vacuum_cleaner2', 'vacuum room'),
('make_bed1', 'chocolate1', 'give chocolate'),
('make_bed1', 'hotel_room1', 'make bed in room'),
('make_bed2', 'hotel_room2', 'make bed in room'),
('vacuum1', 'hotel_room1', 'vacuum in room'),
('vacuum2', 'hotel_room2', 'vacuum in room'),
('clean_bathroom1', 'hotel_room1', 'clean bathroom in room'),
('clean_bathroom2', 'hotel_room2', 'clean bathroom in room');

INSERT INTO objectObject VALUES
('OO-1', 'cleaner1', 'hotel_room1', 'cleaner cleans room'),
('OO-2', 'cleaner3', 'hotel_room2', 'cleaner cleans room');

INSERT INTO objectRelationEvent VALUES
('OO-1', 'vacuum1', 'cleaner vacuums in room'),
('OO-1', 'make_bed1', 'cleaner makes bed in room'),
('OO-1', 'clean_room1', 'cleaner cleans bathroom in room'),
('OO-2', 'vacuum2', 'cleaner vacuums in room'),
('OO-2', 'make_bed2', 'cleaner makes bed in room'),
('OO-2', 'clean_room2', 'cleaner cleans bathroom in room');

INSERT INTO objectAttributeValue VALUES
('OAV-1', 'OG-1', 'hotel_room1', 'do_not_disturb', '0'),
('OAV-2', 'OG-2', 'hotel_room2', 'do_not_disturb', '0'),
('OAV-3', 'OG-3', 'vacuum_cleaner1', 'in_use', '1'),
('OAV-4', 'OG-4', 'cleaner1', 'available', '0'),
('OAV-5', 'OG-5', 'cleaner2', 'available', '1'),
('OAV-6', 'OG-6', 'cleaner3', 'available', '0'),
('OAV-7', 'OG-4', 'cleaner1', 'name', 'Christian'),
('OAV-8', 'OG-5', 'cleaner2', 'name', 'Johanne'),
('OAV-9', 'OG-6', 'cleaner3', 'name', 'Lise'),
('OAV-10', 'OG-7', 'chocolate1', 'amount', '3'),
('OAV-11', 'OG-8', 'chocolate2', 'amount', '2');


INSERT INTO objectAttributeValueEvent VALUES
('vacuum1', 'OAV-3', 'vacuum cleaner in use'),
('vaccum2', 'OAV-3', 'vacuum cleaner in use'),
('vacuum1', 'OAV-4', 'cleaner availability for room'),
('vacuum2', 'OAV-6', 'cleaner availability for room'),
('make_bed1', 'OAV-4', 'cleaner availability for room'),
('make_bed2', 'OAV-6', 'cleaner availability for room'),
('clean_bathroom1', 'OAV-4', 'cleaner availability for room'),
('clean_bathroom2', 'OAV-6', 'cleaner availability for room');

COMMIT;