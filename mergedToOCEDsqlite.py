def create_new_event_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "event" (
                    `eventID` TEXT,
                    `eventType` TEXT,
                    `timestamp` TIMESTAMP,
                    PRIMARY KEY (`eventID`)
              );""")
    
    c.execute("""INSERT INTO event SELECT merged.event.eventID, merged.eventType.eventType, merged.event.eventTime FROM merged.event 
                 NATURAL JOIN merged.eventType""")
    connect.commit()

def create_new_eventAttributeValue_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "eventAttributeValue" (
                    `eventID` TEXT,
                    `eventAttributeName` TEXT,
                    `eventAttributeValue` TEXT,
                    PRIMARY KEY (`eventID`, `eventAttributeName`)
              );""")
    
    c.execute(f"""INSERT INTO eventAttributeValue SELECT eventID, eventAttributeName, eventAttributeValue FROM merged.eventAttributeValue NATURAL JOIN merged.eventAttribute """)
    connect.commit()

def create_new_eventObject_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "eventObject" (
                    `eventID` TEXT,
                    `objectID` TEXT,
                    `EOqualifier` TEXT,
                    PRIMARY KEY (`eventID`, `objectID`)
              );""")
    
    c.execute("""INSERT INTO eventObject SELECT * FROM merged.eventObject""")
    connect.commit()

def create_new_object_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "object" (
                    `objectID` TEXT,
                    `objectType` TEXT,
                    PRIMARY KEY (`objectID`)
              );""")
    
    c.execute("""INSERT INTO object SELECT merged.object.objectID, merged.objectType.objectType FROM merged.object NATURAL JOIN merged.objectType""")
    connect.commit()

def create_new_objectObject_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectObject" (
                    `objectObjectID` TEXT,
                    `fromObjectID` TEXT,
                    `toObjectID` TEXT,
                    `objectRelationType` TEXT,
                    PRIMARY KEY (`objectObjectID`)
              );""")
    
    c.execute("""INSERT INTO objectObject SELECT * FROM merged.objectObject""")
    connect.commit()

def create_new_objectRelationEvent_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectRelationEvent" (
                    `objectObjectID` TEXT,
                    `eventID` TEXT,
                    `OOEqualifier` TEXT,
                    PRIMARY KEY (`objectObjectID`, `eventID`)
              );""")
    
    c.execute("""INSERT INTO objectRelationEvent SELECT merged.objectRelationEvent.objectObjectID, merged.objectRelationEvent.eventID, 
                 merged.objectRelationEvent.OOEqualifier FROM merged.objectRelationEvent""")
    connect.commit()

def create_new_objectAttributeValue_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectAttributeValue" (
                    `instanceID` TEXT,
                    `objectAttributeValueID` TEXT,
                    `objectID` TEXT,
                    `objectAttributeName` TEXT,
                    `objectAttributeValue` TEXT,
                    PRIMARY KEY (`objectAttributeValueID`)
              );""")
    
    c.execute(f"""INSERT INTO objectAttributeValue SELECT instanceID, valueID AS objectAttributeValueID, objectID,
                  objectAttributeName, attributeValue FROM merged.objectAttributeValue NATURAL JOIN merged.objectAttribute """)
    connect.commit()

def create_new_objectAttributeValueEvent_OCED(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectAttributeValueEvent" (
                    `eventID` TEXT,
                    `objectAttributeValueID` TEXT,
                    `OAEqualifier` TEXT,
                    PRIMARY KEY (`eventID`, `objectAttributeValueID`)
              );""")
    
    c.execute("""INSERT INTO objectAttributeValueEvent SELECT eventID, valueID AS objectAttributeValueID, OAEqualifier FROM merged.objectAttributeValueEvent""")
    connect.commit()


