import sqlite3

connect = sqlite3.connect("new.sqlite")
c = connect.cursor()
c.execute("ATTACH DATABASE 'ContainerLogistics.sqlite' as 'ocelbase'")


def create_eventType_Ocel(c):
    c.execute("""CREATE TABLE "eventType" (
                `eventTypeID` TEXT PRIMARY KEY,
                `eventType` TEXT
                )""")

    c.execute(f"""INSERT INTO eventType(eventType)
              SELECT ocel_type AS eventType FROM ocelbase.event_map_type""")
    c.execute(f"SELECT rowid from eventType")
    rowids = c.fetchall()
    for i in rowids:
        print(i)
        c.execute(f"""UPDATE eventType 
                  SET eventTypeID = "ET-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_event_Ocel(c):
    c.execute("""CREATE TABLE "event" (
                    `eventID` TEXT PRIMARY KEY, 
                    `eventTypeID` TEXT, 
                    `eventTime` TIMESTAMP)""")
    
    c.execute(f"""SELECT 'event_' || ocel_type_map
                  FROM ocelbase.event_map_type""")
    
    names = c.fetchall()
    print(names)
   
    for t in names:
        c.execute(f"""INSERT INTO event SELECT ocelbase.event.ocel_id, eventTypeID, ocel_time from ocelbase.event JOIN eventType ON ocel_type = eventType NATURAL JOIN ocelbase.{t[0]}
                   """)
        connect.commit()
            

       

def create_objectObject_Ocel(c):
    c.execute("""CREATE TABLE "objectObject" (
                    `objectObjectID` TEXT,
                    `fromObjectID` TEXT, 
                    `toObjectID`  TEXT, 
                    `objectRelationType` TEXT,
                    PRIMARY KEY (`objectObjectID`))""")
    
    c.execute(f"""INSERT INTO objectObject(fromObjectID,toObjectID,objectRelationType) 
                  SELECT ocelbase.object_object.ocel_source_id AS fromObjectID, 
                  ocelbase.object_object.ocel_target_id AS toObjectID, 
                  ocelbase.object_object.ocel_qualifier AS objectRelationType 
                  FROM ocelbase.object_object LEFT JOIN ocelbase.event_object 
                  ON ocelbase.event_object.ocel_object_id = ocelbase.object_object.ocel_target_id 
                  OR ocelbase.event_object.ocel_object_id = ocelbase.object_object.ocel_source_id""")
    c.execute(f"SELECT rowid from objectObject")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE objectObject 
                  SET objectObjectID = "OO-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_eventObject_Ocel(c):
    c.execute("""CREATE TABLE "eventObject" (
                    `eventID` TEXT, 
                    `objectID` TEXT,
                    `OEqualifier` TEXT, 
                    PRIMARY KEY (`eventID`,`objectID`))""")
    
    c.execute(f"""INSERT INTO eventObject 
                  SELECT ocelbase.event_object.ocel_event_id AS eventID, 
                  ocelbase.event_object.ocel_object_id AS objectID, 
                  ocelbase.event_object.ocel_qualifier AS OEqualifier 
                  FROM ocelbase.event_object""")
    connect.commit()
    
def create_objectType(c):

    c.execute("""CREATE TABLE "objectType" (
                    `objectTypeID` TEXT,
                    `objectType` TEXT,
                    PRIMARY KEY (`objectTypeID`))""")
    
    c.execute(f"""INSERT INTO objectType (objectType) 
                  SELECT ocelbase.object_map_type.ocel_type AS objectType FROM ocelbase.object_map_type""")
    c.execute(f"SELECT rowid from objectType")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE objectType 
                  SET objectTypeID = "OT-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_object(c):
    c.execute("""CREATE TABLE "object" (
                    `objectID` TEXT,
                    `objectTypeID` TEXT,
                    PRIMARY KEY (`objectID`))""")
    
    c.execute(f"""INSERT INTO object
                 SELECT ocelbase.object.ocel_id AS objectID, 
                 objectType.objectTypeID FROM ocelbase.object LEFT JOIN objectType ON ocelbase.object.ocel_type = objectType.objectType""")
    connect.commit()
    
def create_objectRelationEvent(c):
    c.execute("""CREATE TABLE "objectRelationEvent" (
                    `objectRelationEventID` TEXT,
                    `objectObjectID` TEXT,
                    `eventID` TEXT,
                    `OOEqualifier` TEXT,
                    PRIMARY KEY (`objectRelationEventID`))""")
    connect.commit()

def create_objectAttribute(c):
    c.execute("""CREATE TABLE "objectAttribute" (
                    `objectAttributeID` TEXT,
                    `objectTypeID` TEXT,
                    `objectAttributeName` TEXT,
                    PRIMARY KEY (`objectAttributeID`))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('object_',ocel_type_map) 
                  FROM ocelbase.object_map_type)""")
    
    objNames = c.fetchall()

    for i in objNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = 'ocelbase' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()

        for j in atrName:
            c.execute(f"""INSERT INTO objectAttribute (objectTypeID,objectAttributeName)
                         SELECT object.objectTypeID, '{j[0]}' FROM object natural join ocelbase.{i[0]} 
                         WHERE ocelbase.{i[0]}.ocel_id = object.objectID limit 1""")
            c.execute(f"SELECT rowid from objectAttribute")
            rowids = c.fetchall()
            for i in rowids:
                    c.execute(f"""UPDATE objectAttribute 
                            SET objectAttributeID = "OA-{i[0]}" 
                            WHERE rowid  = {i[0]}""")
            connect.commit()
  
            

def create_objectAttributeValue(c):

    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID VARCHAR(50),
                    objectID VARCHAR(50),
                    objectAttributeValTime DATETIME,
                    objectAttributeID VARCHAR(50),
                    AttributeValue VARCHAR(50),
                    PRIMARY KEY (valueID))""")
    
    c.execute(f"""SELECT name FROM sqlite_schema.tables 
                  WHERE name IN (SELECT CONCAT('object_',ocel_type_map) 
                  FROM ocelbase.object_map_type)""")
    
    objNames = c.fetchall()
    for i in objNames:
        c.execute(f"""SELECT name
                      FROM PRAGMA_TABLE_INFO(ocelbase.{i[0]}) 
                      WHERE name != 'ocel_id' AND name != 'ocel_time'""")
        atrName = c.fetchall()
        for j in atrName:
            c.execute(f"""INSERT INTO objectAttributeValue
                         (objectID, objectAttributeValTime, objectAttributeID, AttributeValue, valueID)
                         SELECT ocelbase.{i[0]}.ocel_id AS objectID, 
                         ocelbase.{i[0]}.ocel_time AS objectAttributeValTime, objectAttributeID, 
                         CONVERT(ocelbase.{i[0]}.{j[0]},VARCHAR(50)) AS AttributeValue, CONCAT('OAV-',(@id := @id + 1)) 
                         FROM ocelbase.{i[0]} join (object,objectAttribute) ON ({ocelbase}.{i[0]}.ocel_id = object.objectID 
                         AND object.objectTypeID = objectAttribute.objectTypeID AND objectAttribute.objectAttributeName = '{j[0]}')""")

def create_objectAttributeValueEvent(c):
    c.execute("""CREATE TABLE objectAttributeValueEvent(
              valueID VARCHAR(50),
              eventID VARCHAR(50),
              OAEqualifier VARCHAR(50),
              PRIMARY KEY(valueID,eventID))""")
    
    c.execute("""INSERT INTO objectAttributeValueEvent(valueID,eventID) SELECT valueID, eventID 
              FROM objectAttributeValue NATURAL JOIN event WHERE eventTime = objectAttributeValTime""")
 
            
def create_eventAttribute(c):
    c.execute("""SET @id = 0""")
    c.execute("""CREATE TABLE eventAttribute (
                    eventAttributeID VARCHAR(50),
                    eventTypeID VARCHAR(50),
                    eventAttributeName VARCHAR(50),
                    PRIMARY KEY (eventAttributeID))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('event_',ocel_type_map) 
                  FROM ocelbase.event_map_type)""")
    
    eventNames = c.fetchall()

    for i in eventNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = 'ocelbase' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()

        for j in atrName:
            c.execute(f"""INSERT INTO eventAttribute (eventTypeID,eventAttributeName,eventAttributeID)
                         SELECT event.eventTypeID, '{j[0]}', CONCAT('EA-',(@id := @id+1)) FROM event NATURAL JOIN {ocelbase}.{i[0]} 
                         WHERE ocelbase.{i[0]}.ocel_id = event.eventID limit 1""")        

def create_eventAttributeValue(c):
    c.execute("""CREATE TABLE eventAttributeValue (
                    eventID VARCHAR(50),
                    eventAttributeID VARCHAR(50),
                    eventAttributeValue VARCHAR(50),
                    PRIMARY KEY (eventID, eventAttributeValue)) """)        

    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('event_',ocel_type_map) 
                  FROM ocelbase.event_map_type)""")
    
    eventNames = c.fetchall()
    for i in eventNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = 'ocelbase' AND TABLE_NAME = 'i[0]' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()
        for j in atrName:
            c.execute(f"""INSERT INTO eventAttributeValue
                         SELECT ocelbase.{i[0]}.ocel_id AS eventID, 
                         eventAttributeID, CONVERT(ocelbase.{i[0]}.{j[0]},VARCHAR(50)) AS eventAttributeValue 
                         FROM ocelbase.{i[0]} join (event,eventAttribute) ON ({ocelbase}.{i[0]}.ocel_id = event.eventID 
                         AND event.eventTypeID = eventAttribute.eventTypeID AND eventAttribute.eventAttributeName = '{j[0]}')""")

create_eventType_Ocel(c)
create_event_Ocel(c)


