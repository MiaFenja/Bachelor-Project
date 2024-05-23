BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "event" (
    `eventID` TEXT,
    `eventType` TEXT,
    `timestamp` TIMESTAMP,
    PRIMARY KEY (`eventID`)
);

CREATE TABLE IF NOT EXISTS "eventAttributeValue" (
    `eventAttributeValueID` TEXT,
    `eventID` TEXT,
    `eventAttributeName` TEXT,
    `eventAttributeValue` TEXT,
    PRIMARY KEY (`eventAttributeValueID`)
);

CREATE TABLE IF NOT EXISTS "eventObject" (
    `eventID` TEXT,
    `objectID` TEXT,
    `EOqualifier` TEXT,
    PRIMARY KEY (`eventID`, `objectID`)
);

CREATE TABLE IF NOT EXISTS "objectRelationEvent" (
    `objectObjectID` TEXT,
    `eventID` TEXT,
    `OOEqualifier` TEXT,
    PRIMARY KEY (`objectObjectID`, `eventID`)
);

CREATE TABLE IF NOT EXISTS "object" (
    `objectID` TEXT,
    `objectType` TEXT,
    PRIMARY KEY (`objectID`)
);

CREATE TABLE IF NOT EXISTS "objectObject" (
    `objectObjectID` TEXT,
    `fromObjectID` TEXT,
    `toObjectID` TEXT,
    `objectRelationType` TEXT,
    PRIMARY KEY (`objectObjectID`)
);

CREATE TABLE IF NOT EXISTS "objectAttributeValue" (
    `objectAttributeValueID` TEXT,
    `objectID` TEXT,
    `objectAttributeName` TEXT,
    `objectAttributeValue` TEXT,
    PRIMARY KEY (`objectAttributeValueID`)
);

CREATE TABLE IF NOT EXISTS "objectAttributeValueEvent" (
    `eventID` TEXT,
    `objectAttributeValueID` TEXT,
    `OAEqualifier` TEXT,
    PRIMARY KEY (`eventID`, `objectAttributeValueID`)
);

# Insertion 

INSERT INTO event VALUES
('vacuum1', 'Vacuum', "2024-03-20T10:30:18.000Z"),
('vacuum2', 'Vacuum', "2024-04-01T09:36:51.000Z"),
('make_bed1', 'Make Bed', "2024-03-20T10:40:33.000Z"),
('make_bed2', 'Make Bed', "2024-04-01T09:30:47.000Z"),
('clean_bathroom1', 'Clean Bathroom', "2024-03-20T10:45:03.000Z"),
('clean_bathroom2', 'Clean Bathroom', "2024-04-01T09:15:24.000Z");

INSERT INTO eventAttributeValue VALUES
('EAV-1', 'vacuum1', 'finished', '1'),
('EAV-2', 'vacuum2', 'finished', '0'),
('EAV-3', 'make_bed1', 'finished', '1'),
('EAV-4', 'make_bed2', 'finished', '1'),
('EAV-5', 'make_bed1', 'chocolate', '1'),
('EAV-6', 'make_bed2', 'chocolate', '0'),
('EAV-7', 'clean_bathroom1', 'finished', '1'),
('EAV-8', 'clean_bathroom2', 'finished', '1');

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
('OAV-1', 'hotel_room1', 'do_not_disturb', '0'),
('OAV-2', 'hotel_room2', 'do_not_disturb', '0'),
('OAV-3', 'vacuum_cleaner1', 'in_use', '1'),
('OAV-4', 'cleaner1', 'available', '0'),
('OAV-5', 'cleaner2', 'available', '1'),
('OAV-6', 'cleaner3', 'available', '0'),
('OAV-7', 'cleaner1', 'name', 'Christian'),
('OAV-8', 'cleaner2', 'name', 'Johanne'),
('OAV-9', 'cleaner3', 'name', 'Lise'),
('OAV-10', 'chocolate1', 'amount', '3'),
('OAV-11', 'chocolate2', 'amount', '2');


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
