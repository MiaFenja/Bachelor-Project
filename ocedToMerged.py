import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()
c.execute("ATTACH DATABASE 'db/OCED_Simple_Database.db' as 'ocedbase'")

def create_eventType_OCED(c,connect):
    c.execute("""CREATE TABLE "eventType" (
                `eventTypeID` TEXT PRIMARY KEY,
                `eventType` TEXT
                )""")
    
    c.execute(f"""INSERT INTO eventType(eventType)
              SELECT DISTINCT eventType FROM ocedbase.event""")
    c.execute(f"SELECT rowid from eventType")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE eventType 
                  SET eventTypeID = "ET-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_event_OCED(c,connect):
    c.execute("""CREATE TABLE "event" (
                    `eventID` TEXT PRIMARY KEY, 
                    `eventTypeID` TEXT, 
                    `eventTime` TIMESTAMP)""")
    
    c.execute("""INSERT INTO event SELECT eventID, eventTypeID, timestamp AS eventTime FROM ocedbase.event NATURAL JOIN eventType""")
    connect.commit()

def create_objectObject_OCED(c,connect):
    c.execute("""CREATE TABLE "objectObject" (
                    `objectObjectID` TEXT,
                    `fromObjectID` TEXT, 
                    `toObjectID`  TEXT, 
                    `objectRelationType` TEXT,
                    PRIMARY KEY (`objectObjectID`))""")
    c.execute("""INSERT INTO objectObject SELECT * FROM ocedbase.objectObject""")
    connect.commit()

def create_eventObject_OCED(c,connect):
    c.execute("""CREATE TABLE "eventObject" (
                    `eventID` TEXT, 
                    `objectID` TEXT,
                    `EOqualifier` TEXT, 
                    PRIMARY KEY (`eventID`,`objectID`))""")
    c.execute("""INSERT INTO eventObject SELECT eventID, objectID, EOqualifier FROM ocedbase.eventObject""")
    connect.commit()
    
def create_objectType_OCED(c,connect):
    c.execute("""CREATE TABLE "objectType" (
                    `objectTypeID` TEXT,
                    `objectType` TEXT,
                    PRIMARY KEY (`objectTypeID`))""")
    
    c.execute(f"""INSERT INTO objectType (objectType) 
                  SELECT DISTINCT objectType FROM ocedbase.object""")
    c.execute(f"SELECT rowid from objectType")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE objectType 
                  SET objectTypeID = "OT-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_object_OCED(c,connect):
    c.execute("""CREATE TABLE "object" (
                    `objectID` TEXT,
                    `objectTypeID` TEXT,
                    PRIMARY KEY (`objectID`))""")
    c.execute("""INSERT INTO object SELECT objectID, objectTypeID FROM ocedbase.object NATURAL JOIN objectType""")
    connect.commit()

def create_objectRelationEvent_OCED(c,connect):
    c.execute("""CREATE TABLE "objectRelationEvent" (
                    `objectRelationEventID` TEXT,
                    `objectObjectID` TEXT,
                    `eventID` TEXT,
                    `OOEqualifier` TEXT,
                    PRIMARY KEY (`objectRelationEventID`))""")
    c.execute("""INSERT INTO objectRelationEvent (objectObjectID, eventID, OOEqualifier) SELECT * FROM ocedbase.objectRelationEvent""")
    c.execute(f"SELECT rowid from objectRelationEvent")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE objectRelationEvent 
                  SET objectRelationEventID = "ORE-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_objectAttribute_OCED(c,connect):
    c.execute("""CREATE TABLE "objectAttribute" (
                    `objectAttributeID` TEXT,
                    `objectTypeID` TEXT,
                    `objectAttributeName` TEXT,
                    PRIMARY KEY (`objectAttributeID`))""")
    c.execute("""INSERT INTO objectAttribute (objectTypeID, objectAttributeName)
                 SELECT DISTINCT objectType.objectTypeID AS objectTypeID, objectAttributeValue.objectAttributeName FROM objectType NATURAL JOIN object NATURAL JOIN ocedbase.objectAttributeValue""")
    c.execute(f"SELECT rowid from objectAttribute")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE objectAttribute
                  SET objectAttributeID = "OA-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()
            

def create_objectAttributeValue_OCED(c,connect):
    c.execute("""CREATE TABLE "objectAttributeValue" (
                    `valueID` TEXT,
                    `objectID` TEXT,
                    `objectAttributeValTime` TIMESTAMP,
                    `objectAttributeID` TEXT,
                    `attributeValue` TEXT,
                    PRIMARY KEY (`valueID`))""")
    c.execute("""INSERT INTO objectAttributeValue (valueID, objectID, objectAttributeID, attributeValue) 
                 SELECT objectAttributeValueID AS valueID, objectID, objectAttributeID, objectAttributeValue AS attributeValue 
                 FROM ocedbase.objectAttributeValue NATURAL JOIN objectAttribute""")
    connect.commit()

def create_objectAttributeValueEvent_OCED(c,connect):
    c.execute("""CREATE TABLE "objectAttributeValueEvent" (
              `valueID` TEXT,
              `eventID` TEXT,
              `OAEqualifier` TEXT,
              PRIMARY KEY(`valueID`,`eventID`))""")
    c.execute("""INSERT INTO objectAttributeValueEvent SELECT objectAttributeValueID AS valueID, eventID, OAEqualifier 
                 FROM ocedbase.objectAttributeValueEvent""")
    connect.commit()
 
            
def create_eventAttribute_OCED(c,connect):
    c.execute("""CREATE TABLE "eventAttribute" (
                    `eventAttributeID` TEXT,
                    `eventTypeID` TEXT,
                    `eventAttributeName` TEXT,
                    PRIMARY KEY (`eventAttributeID`))""")
    c.execute("INSERT INTO eventAttribute(eventTypeID,eventAttributeName) SELECT DISTINCT eventTypeID, eventAttributeName FROM eventType NATURAL JOIN event NAtural JOIN ocedbase.eventAttributeValue")
    c.execute(f"SELECT rowid from eventAttribute")
    rowids = c.fetchall()

    for k in rowids:
        c.execute(f"""UPDATE eventAttribute
                    SET eventAttributeID = "EA-{k[0]}" 
                    WHERE rowid  = {k[0]}""")
    connect.commit()   


def create_eventAttributeValue_OCED(c,connect):
    c.execute("""CREATE TABLE "eventAttributeValue" (
                    `eventID` TEXT,
                    `eventAttributeID` TEXT,
                    `eventAttributeValue` TEXT,
                    PRIMARY KEY (`eventID`, `eventAttributeID`)) """) 
    c.execute("""INSERT INTO eventAttributeValue SELECT ocedbase.eventAttributeValue.eventID, eventAttribute.eventAttributeID, 
                 ocedbase.eventAttributeValue.eventAttributeValue 
                 FROM ocedbase.eventAttributeValue NATURAL JOIN event NATURAL JOIN eventAttribute""")
    connect.commit()

 
