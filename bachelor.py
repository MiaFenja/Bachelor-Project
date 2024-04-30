import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
ocelbase = "OCEL"
c = mydb.cursor()
c.execute("DROP DATABASE IF EXISTS testing1")
c.execute("CREATE DATABASE testing1")
c.execute("USE testing1")

def create_eventType_Ocel(c):
    c.execute("""CREATE TABLE eventType (
                eventTypeID BIGINT NOT NULL AUTO_INCREMENT,
                eventType varchar(50),
                primary key(eventTypeID))
    """)
    c.execute(f"""INSERT INTO eventType(eventType) 
              SELECT ocel_type from {ocelbase}.event_map_type""")

def create_event_Ocel(c):
    c.execute("""CREATE TABLE event_ (
                    eventID VARCHAR(50), 
                    eventTypeID BIGINT, 
                    eventTime DATETIME, 
                    PRIMARY KEY (eventID))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type)""")
    
    names = c.fetchall()
    c.execute("""CREATE TABLE
              temporaryTable(
              ocel_id varchar(50), 
              eventType varchar(50),
              ocel_time DATETIME)""")
    for t in names:
         c.execute(f"""INSERT INTO temporaryTable 
                   SELECT ocel_id,
                   ocel_type AS eventType,
                   ocel_time 
                   FROM {ocelbase}.{t[0]}
                   NATURAL LEFT JOIN {ocelbase}.event_""")

    
    c.execute("""INSERT INTO event_ SELECT 
              ocel_id AS eventID, 
              eventTypeID,
              ocel_time AS eventTime from
              temporaryTable LEFT JOIN eventType 
              on temporaryTable.eventType = eventType.eventType""")
    c.execute("DROP TABLE temporaryTable")


def create_objectObject_Ocel(c):
    c.execute("""CREATE TABLE objectObject (
                    objectObjectID BIGINT NOT NULL AUTO_INCREMENT,
                    fromObjectID VARCHAR(50), 
                    toObjectID  VARCHAR(50), 
                    objectRelationType VARCHAR(50),
                    PRIMARY KEY (objectObjectID))""")
    
    c.execute(f"""INSERT INTO objectObject(fromObjectID,toObjectID,objectRelationType) 
                  SELECT {ocelbase}.object_object.ocel_source AS fromObjectID, 
                  {ocelbase}.object_object.ocel_target AS toObjectID, 
                  {ocelbase}.object_object.ocel_qualifier AS objectRelationType 
                  FROM {ocelbase}.object_object LEFT JOIN {ocelbase}.event_object 
                  ON {ocelbase}.event_object.ocel_object = {ocelbase}.object_object.ocel_target 
                  OR {ocelbase}.event_object.ocel_object = {ocelbase}.object_object.ocel_source""")

def create_eventObject_Ocel(c):
    c.execute("""CREATE TABLE eventObject (
                    eventID VARCHAR(50), 
                    objectID VARCHAR(50),
                    OEqualifier TEXT, 
                    PRIMARY KEY (eventID,objectID))""")
    
    c.execute(f"""INSERT INTO eventObject 
                  SELECT {ocelbase}.event_object.ocel_event AS eventID, 
                  {ocelbase}.event_object.ocel_object AS objectID, 
                  {ocelbase}.event_object.ocel_qualifier AS OEqualifier 
                  FROM {ocelbase}.event_object""")
    
def create_objectType(c):
    c.execute("""CREATE TABLE objectType (
                    objectTypeID INT NOT NULL AUTO_INCREMENT,
                    objectType TEXT,
                    PRIMARY KEY (objectTypeID))""")
    
    c.execute(f"""INSERT INTO objectType (objectType) 
                  SELECT {ocelbase}.object_map_type.ocel_type AS objectType FROM {ocelbase}.object_map_type""")

def create_object(c):
    c.execute("""CREATE TABLE object (
                    objectID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    PRIMARY KEY (objectID))""")
    
    c.execute(f"""INSERT INTO object
                 SELECT {ocelbase}.object.ocel_id AS objectID, 
                 testing1.objectType.objectTypeID FROM {ocelbase}.object NATURAL JOIN testing1.objectType WHERE objectType = ocel_type""")
    
def create_objectRelationEvent(c):
    c.execute("""CREATE TABLE objectRelationEvent (
                    objectObjectID BIGINT,
                    eventID VARCHAR(50),
                    OOEqualifier VARCHAR(50),
                    PRIMARY KEY (objectObjectID, eventID))""")
    
    c.execute("""INSERT INTO objectRelationEvent (objectObjectID, eventID)
                 SELECT objectObject.objectObjectID, eventObject.eventID FROM objectObject 
                 NATURAL JOIN eventObject WHERE objectObject.fromObjectID = eventObject.objectID 
                 OR objectObject.toObjectID = eventObject.objectID""")

def create_objectAttribute(c):
    c.execute("""CREATE TABLE objectAttribute (
                    objectAttributeID INT NOT NULL AUTO_INCREMENT,
                    objectTypeID INT,
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
            c.execute(f"""INSERT INTO objectAttribute (objectTypeID,objectAttributeName)
                         SELECT object.objectTypeID, '{j[0]}' FROM object natural join {ocelbase}.{i[0]} WHERE {ocelbase}.{i[0]}.ocel_id = object.objectID limit 1""")
  
            

def create_objectAttributeValue(c):
    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID INT NOT NULL AUTO_INCREMENT,
                    objectID VARCHAR(50),
                    objectAttributeValTime DATETIME,
                    objectAttributeID INT,
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
                   (objectID, objectAttributeValTime, objectAttributeID, AttributeValue)
                    SELECT {ocelbase}.{i[0]}.ocel_id AS objectID, 
                    {ocelbase}.{i[0]}.ocel_time AS objectAttributeValTime, objectAttributeID, 
                        convert({ocelbase}.{i[0]}.{j[0]},varchar(50)) AS AttributeValue FROM {ocelbase}.{i[0]} join (object,objectAttribute) ON ({ocelbase}.{i[0]}.ocel_id = object.objectID AND object.objectTypeID = objectAttribute.objectTypeID AND objectAttribute.objectAttributeName = '{j[0]}')""")
            
            
            
        
        

create_eventType_Ocel(c)
create_event_Ocel(c)
create_objectObject_Ocel(c)
create_eventObject_Ocel(c)
create_objectType(c)
create_object(c)
create_objectRelationEvent(c)
create_objectAttribute(c)
create_objectAttributeValue(c)
c.execute("select * from objectAttributeValue")
fetchh = c.fetchall()
print(fetchh)
mydb.commit()


