BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "event" (
	`eventID` TEXT,
    `eventTypeID` TEXT,
    `eventTime` TIMESTAMP,
    PRIMARY KEY (`eventID`),
    FOREIGN KEY (`eventTypeID`) REFERENCES eventType (`eventTypeID`)
);


CREATE TABLE IF NOT EXISTS "object" (
	`objectID` TEXT,
    `objectTypeID` TEXT,
    PRIMARY KEY (`objectID`),
    FOREIGN KEY (`objectTypeID`) REFERENCES objectType (`objectTypeID`)
);


CREATE TABLE IF NOT EXISTS "objectObject" (
	`objectObjectID` TEXT,
    `fromObjectID` TEXT,
    `toObjectID` TEXT,
    `objectRelationType` TEXT,
    PRIMARY KEY (`objectObjectID`),
    FOREIGN KEY (`fromObjectID`,`toObjectID`) REFERENCES object (`objectID`)
);

CREATE TABLE IF NOT EXISTS "eventObject" (
	`eventID` TEXT,
    `objectID` TEXT,
    `EOqualifier` TEXT,
    PRIMARY KEY (`eventID`, `objectID`, `EOqualifier`)
);

CREATE TABLE IF NOT EXISTS "eventType" (
	`eventTypeID` TEXT,
    `eventType` TEXT,
    PRIMARY KEY (`eventTypeID`)
);

CREATE TABLE IF NOT EXISTS "objectType" (
	`objectTypeID` TEXT,
    `objectType` TEXT,
    PRIMARY KEY (`objectTypeID`)
);


CREATE TABLE IF NOT EXISTS "eventAttributeValue" (
	`eventID` TEXT,
    `eventAttributeID` TEXT,
    `eventAttributeValue` TEXT,
    PRIMARY KEY (`eventID`, `eventAttributeID`)
);

CREATE TABLE IF NOT EXISTS "eventAttribute" (
	`eventAttributeID` TEXT,
    `eventTypeID` TEXT,
    `eventAttributeName` TEXT,
    PRIMARY KEY (`eventAttributeID`),
    FOREIGN KEY (`eventTypeID`) REFERENCES eventType (`eventTypeID`)
);

CREATE TABLE IF NOT EXISTS "objectAttribute" (
	`objectAttributeID` TEXT,
    `objectTypeID` TEXT,
    `objectAttributeName` TEXT,
    PRIMARY KEY (`objectAttributeID`),
    FOREIGN KEY (`objectTypeID`) REFERENCES objectType (`objectTypeID`)
);

CREATE TABLE IF NOT EXISTS "objectAttributeValue" (
	`valueID` TEXT,
    `objectID` TEXT,
    `objectAttributeValTime` TIMESTAMP,
    `objectAttributeID` TEXT,
    `objectAttributeValue`TEXT,
    PRIMARY KEY (`valueID`),
    FOREIGN KEY (`objectID`) REFERENCES object (`objectID`), FOREIGN KEY (`objectAttributeID`) REFERENCES objectAttribute (`objectAttributeID`)
);

CREATE TABLE IF NOT EXISTS "objectRelationEvent" (
	`objectRelationEventID` TEXT,
    `objectObjectID` TEXT,
    `eventID` TEXT,
    `OOEqualifier` TEXT
    PRIMARY KEY (`objectRelationEventID`), FOREIGN KEY (`eventID`) REFERENCES event (`eventID`), FOREIGN KEY (`objectObjectID`) REFERENCES objectObject (`objectObjectID`)
);

CREATE TABLE IF NOT EXISTS "objectAttributeValueEvent" (
	`valueID` TEXT,
    `eventID` TEXT,
    `OAEqualifier` TEXT,
    PRIMARY KEY (`valueID`, `eventID`)
);







