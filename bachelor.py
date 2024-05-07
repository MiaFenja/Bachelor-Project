import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="1234"
)
ocelbase = "OCEL"

c = mydb.cursor()
c.execute("DROP DATABASE IF EXISTS testing1")
c.execute("CREATE DATABASE testing1")
c.execute("USE testing1")

def create_eventType_Ocel(c):
    c.execute("""CREATE TABLE eventType (
                eventTypeID VARCHAR(50),
                eventType varchar(50),
                primary key(eventTypeID))
    """)
    c.execute("""SET @id = 0""")
    c.execute(f"""INSERT INTO eventType(eventType,eventTypeID)
              SELECT ocel_type AS eventType, CONCAT('ET-',(@id := @id +1)) AS eventTypeID from {ocelbase}.event_map_type""")

def create_event_Ocel(c):
    c.execute("""CREATE TABLE event (
                    eventID VARCHAR(50), 
                    eventTypeID VARCHAR(50), 
                    eventTime DATETIME, 
                    PRIMARY KEY (eventID))""")
    
    c.execute(f"""SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type""")
    
    names = c.fetchall()
    for t in names:
         c.execute(f"""INSERT INTO event
                   SELECT ocel_id AS eventID, eventTypeID, ocel_time AS eventTime FROM {ocelbase}.event 
                   NATURAL JOIN {ocelbase}.{t[0]} NATURAL JOIN eventType 
                   WHERE eventType.eventType = {ocelbase}.event.ocel_type;""")

  


def create_objectObject_Ocel(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectObject (
                    objectObjectID VARCHAR(50),
                    fromObjectID VARCHAR(50), 
                    toObjectID  VARCHAR(50), 
                    objectRelationType VARCHAR(50),
                    PRIMARY KEY (objectObjectID))""")
    
    c.execute(f"""INSERT INTO objectObject(fromObjectID,toObjectID,objectRelationType, objectObjectID) 
                  SELECT {ocelbase}.object_object.ocel_source_id AS fromObjectID, 
                  {ocelbase}.object_object.ocel_target_id AS toObjectID, 
                  {ocelbase}.object_object.ocel_qualifier AS objectRelationType, CONCAT('OO-',(@id := @id + 1)) 
                  FROM {ocelbase}.object_object LEFT JOIN {ocelbase}.event_object 
                  ON {ocelbase}.event_object.ocel_object_id = {ocelbase}.object_object.ocel_target_id 
                  OR {ocelbase}.event_object.ocel_object_id = {ocelbase}.object_object.ocel_source_id""")

def create_eventObject_Ocel(c):
    c.execute("""CREATE TABLE eventObject (
                    eventID VARCHAR(50), 
                    objectID VARCHAR(50),
                    OEqualifier TEXT, 
                    PRIMARY KEY (eventID,objectID))""")
    
    c.execute(f"""INSERT INTO eventObject 
                  SELECT {ocelbase}.event_object.ocel_event_id AS eventID, 
                  {ocelbase}.event_object.ocel_object_id AS objectID, 
                  {ocelbase}.event_object.ocel_qualifier AS OEqualifier 
                  FROM {ocelbase}.event_object""")
    
def create_objectType(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectType (
                    objectTypeID VARCHAR(50),
                    objectType TEXT,
                    PRIMARY KEY (objectTypeID))""")
    
    c.execute(f"""INSERT INTO objectType (objectType, objectTypeID) 
                  SELECT {ocelbase}.object_map_type.ocel_type AS objectType, CONCAT('OT-',(@id := @id + 1)) FROM {ocelbase}.object_map_type""")

def create_object(c):
    c.execute("""CREATE TABLE object (
                    objectID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    PRIMARY KEY (objectID))""")
    
    c.execute(f"""INSERT INTO object
                 SELECT {ocelbase}.object.ocel_id AS objectID, 
                 testing1.objectType.objectTypeID FROM {ocelbase}.object NATURAL JOIN testing1.objectType WHERE objectType = ocel_type""")
    
def create_objectRelationEvent(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectRelationEvent (
                    objectRelationEventID VARCHAR(50),
                    objectObjectID VARCHAR(50),
                    eventID VARCHAR(50),
                    OOEqualifier VARCHAR(50),
                    PRIMARY KEY (objectRelationEventID))""")
    
    c.execute("""INSERT INTO objectRelationEvent (objectObjectID, eventID, objectRelationEventID)
                 SELECT objectObject.objectObjectID, eventObject.eventID, CONCAT('ORE-',(@id := @id + 1)) FROM objectObject 
                 NATURAL JOIN eventObject WHERE objectObject.fromObjectID = eventObject.objectID 
                 OR objectObject.toObjectID = eventObject.objectID""")

def create_objectAttribute(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectAttribute (
                    objectAttributeID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    objectAttributeName VARCHAR(50),
                    PRIMARY KEY (objectAttributeID))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('object_',ocel_type_map) 
                  FROM {ocelbase}.object_map_type)""")
    
    objNames = c.fetchall()

    for i in objNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()

        for j in atrName:
            c.execute(f"""INSERT INTO objectAttribute (objectTypeID,objectAttributeName,objectAttributeID)
                         SELECT object.objectTypeID, '{j[0]}', CONCAT('OA-',(@id := @id + 1)) FROM object natural join {ocelbase}.{i[0]} 
                         WHERE {ocelbase}.{i[0]}.ocel_id = object.objectID limit 1""")
  
            

def create_objectAttributeValue(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID VARCHAR(50),
                    objectID VARCHAR(50),
                    objectAttributeValTime DATETIME,
                    objectAttributeID VARCHAR(50),
                    AttributeValue VARCHAR(50),
                    PRIMARY KEY (valueID))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('object_',ocel_type_map) 
                  FROM {ocelbase}.object_map_type)""")
    
    objNames = c.fetchall()
    for i in objNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()
        for j in atrName:
            c.execute(f"""INSERT INTO objectAttributeValue
                         (objectID, objectAttributeValTime, objectAttributeID, AttributeValue, valueID)
                         SELECT {ocelbase}.{i[0]}.ocel_id AS objectID, 
                         {ocelbase}.{i[0]}.ocel_time AS objectAttributeValTime, objectAttributeID, 
                         CONVERT({ocelbase}.{i[0]}.{j[0]},VARCHAR(50)) AS AttributeValue, CONCAT('OAV-',(@id := @id + 1)) 
                         FROM {ocelbase}.{i[0]} join (object,objectAttribute) ON ({ocelbase}.{i[0]}.ocel_id = object.objectID 
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
                  FROM {ocelbase}.event_map_type)""")
    
    eventNames = c.fetchall()

    for i in eventNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()

        for j in atrName:
            c.execute(f"""INSERT INTO eventAttribute (eventTypeID,eventAttributeName,eventAttributeID)
                         SELECT event.eventTypeID, '{j[0]}', CONCAT('EA-',(@id := @id+1)) FROM event NATURAL JOIN {ocelbase}.{i[0]} 
                         WHERE {ocelbase}.{i[0]}.ocel_id = event.eventID limit 1""")        

def create_eventAttributeValue(c):
    c.execute("""CREATE TABLE eventAttributeValue (
                    eventID VARCHAR(50),
                    eventAttributeID VARCHAR(50),
                    eventAttributeValue VARCHAR(50),
                    PRIMARY KEY (eventID, eventAttributeValue)) """)        

    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type)""")
    
    eventNames = c.fetchall()
    for i in eventNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()
        for j in atrName:
            c.execute(f"""INSERT INTO eventAttributeValue
                         SELECT {ocelbase}.{i[0]}.ocel_id AS eventID, 
                         eventAttributeID, CONVERT({ocelbase}.{i[0]}.{j[0]},VARCHAR(50)) AS eventAttributeValue 
                         FROM {ocelbase}.{i[0]} join (event,eventAttribute) ON ({ocelbase}.{i[0]}.ocel_id = event.eventID 
                         AND event.eventTypeID = eventAttribute.eventTypeID AND eventAttribute.eventAttributeName = '{j[0]}')""")

create_eventType_Ocel(c)
create_event_Ocel(c)
create_objectObject_Ocel(c)
create_eventObject_Ocel(c)
create_objectType(c)
create_object(c)
create_objectRelationEvent(c)
create_objectAttribute(c)
create_objectAttributeValue(c)
create_objectAttributeValueEvent(c)
create_eventAttribute(c)
create_eventAttributeValue(c)
c.execute("select * from object")
fetchh = c.fetchall()
print(fetchh)
mydb.commit()


