import sqlite3

connect = sqlite3.connect("newOCED.sqlite")
c = connect.cursor()
c.execute(f"ATTACH DATABASE 'merged.sqlite' as 'merged'")

def create_new_event_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "event_OCED" (
                    `eventID` TEXT,
                    `eventType` TEXT,
                    `timestamp` TIMESTAMP,
                    PRIMARY KEY (`eventID`)
              );""")
    
    c.execute("""INSERT INTO event_OCED SELECT merged.event.eventID, merged.eventType.eventType, merged.event.eventTime FROM merged.event 
                 NATURAL JOIN merged.eventType""")
    connect.commit()

def create_new_eventAttributeValue_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "eventAttributeValue_OCED" (
                    `eventID` TEXT,
                    `eventAttributeName` TEXT,
                    `eventAttributeValue` TEXT,
                    PRIMARY KEY (`eventID`, `eventAttributeName`)
              );""")
    
    c.execute(f"""INSERT INTO eventAttributeValue_OCED SELECT eventID, eventAttributeName, eventAttributeValue FROM merged.eventAttributeValue NATURAL JOIN merged.eventAttribute """)
    connect.commit()

def create_new_eventObject_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "eventObject_OCED" (
                    `eventID` TEXT,
                    `objectID` TEXT,
                    `EOqualifier` TEXT,
                    PRIMARY KEY (`eventID`, `objectID`)
              );""")
    
    c.execute("""INSERT INTO eventObject_OCED SELECT * FROM merged.eventObject""")
    connect.commit()

def create_new_object_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "object_OCED" (
                    `objectID` TEXT,
                    `objectType` TEXT,
                    PRIMARY KEY (`objectID`)
              );""")
    
    c.execute("""INSERT INTO object_OCED SELECT merged.object.objectID, merged.objectType.objectType FROM merged.object NATURAL JOIN merged.objectType""")
    connect.commit()

def create_new_objectObject_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectObject_OCED" (
                    `objectObjectID` TEXT,
                    `fromObjectID` TEXT,
                    `toObjectID` TEXT,
                    `objectRelationType` TEXT,
                    PRIMARY KEY (`objectObjectID`)
              );""")
    
    c.execute("""INSERT INTO objectObject_OCED SELECT * FROM merged.objectObject""")
    connect.commit()

def create_new_objectRelationEvent_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectRelationEvent_OCED" (
                    `objectObjectID` TEXT,
                    `eventID` TEXT,
                    `OOEqualifier` TEXT,
                    PRIMARY KEY (`objectObjectID`, `eventID`)
              );""")
    
    c.execute("""INSERT INTO objectRelationEvent_OCED SELECT merged.objectRelationEvent.objectObjectID, merged.objectRelationEvent.eventID, 
                 merged.objectRelationEvent.OOEqualifier FROM merged.objectRelationEvent""")
    connect.commit()

def create_new_objectAttributeValue_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectAttributeValue_OCED" (
                    `objectAttributeValueID` TEXT,
                    `objectID` TEXT,
                    `objectAttributeName` TEXT,
                    `objectAttributeValue` TEXT,
                    PRIMARY KEY (`objectAttributeValueID`)
              );""")
    
    c.execute(f"""INSERT INTO objectAttributeValue_OCED SELECT valueID AS objectAttributeValueID, objectID,
                  objectAttributeName, attributeValue FROM merged.objectAttributeValue NATURAL JOIN merged.objectAttribute """)
    connect.commit()

def create_new_objectAttributeValueEvent_OCED(c):
    c.execute("""CREATE TABLE IF NOT EXISTS "objectAttributeValueEvent_OCED" (
                    `eventID` TEXT,
                    `objectAttributeValueID` TEXT,
                    `OAEqualifier` TEXT,
                    PRIMARY KEY (`eventID`, `objectAttributeValueID`)
              );""")
    
    c.execute("""INSERT INTO objectAttributeValueEvent_OCED SELECT eventID, valueID AS objectAttributeValueID, OAEqualifier FROM merged.objectAttributeValueEvent""")
    connect.commit()

create_new_event_OCED(c) 
create_new_eventAttributeValue_OCED(c)
create_new_eventObject_OCED(c)
create_new_object_OCED(c)
create_new_objectObject_OCED(c)
create_new_objectRelationEvent_OCED(c)
create_new_objectAttributeValue_OCED(c)
create_new_objectAttributeValueEvent_OCED(c)