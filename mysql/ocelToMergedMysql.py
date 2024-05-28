import mysql.connector
import triggers
connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
ocelbase = "OCEL"

c = connect.cursor()
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
    #Gets triggered when event_map_type is 
   # c.execute(f"USE {ocelbase}")
    #c.execute(f"""CREATE TRIGGER eventTypetrigger AFTER INSERT ON event_map_type FOR EACH ROW
              # INSERT testing1.eventType(eventType,eventTypeID)  SELECT new.ocel_type, CONCAT("ET-",Convert(SUBSTRING(max(testing1.eventType.eventTypeID),4),INTEGER)+1) from testing1.eventType""")
    #c.execute(f"USE testing1")

def create_event_Ocel(c):
    c.execute("""CREATE TABLE event (
                    eventID VARCHAR(50), 
                    eventTypeID VARCHAR(50), 
                    eventTime DATETIME, 
                    PRIMARY KEY (eventID))""")
    
    c.execute(f"""SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type""")
    
    names = c.fetchall()
    #triggers every time an event type table ex event_receiveOrder is uppdated so not when event is, 
    #goes with the assumption that eventType in merged is already updated if neccesary will not work if the event type table in ocel is updated before event_map_type in ocel
    for t in names:
        c.execute(f"""INSERT INTO event
                   SELECT ocel_id AS eventID, eventTypeID, ocel_time AS eventTime FROM {ocelbase}.event
                   NATURAL JOIN {ocelbase}.{t[0]} NATURAL JOIN eventType 
                   WHERE eventType.eventType = {ocelbase}.event.ocel_type;""")
        c.execute(f"USE {ocelbase}") 
        c.execute(f"""CREATE TRIGGER {t[0]}trigger AFTER INSERT ON {ocelbase}.{t[0]} FOR EACH ROW 
                    INSERT testing1.event(eventID, eventTypeID,eventTime) SELECT new.ocel_id, testing1.eventType.eventTypeID, new.ocel_time FROM  testing1.eventType NATURAL JOIN event WHERE event.ocel_id = new.ocel_id  and ocel_type = eventType.eventType""")
        c.execute("USE testing1")



def create_objectObject_Ocel(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectObject (
                    objectObjectID VARCHAR(50),
                    fromObjectID VARCHAR(50), 
                    toObjectID  VARCHAR(50), 
                    objectRelationType VARCHAR(50),
                    PRIMARY KEY (objectObjectID))""")
    
   
    c.execute(f"""INSERT INTO objectObject(objectObjectID,fromObjectID,toObjectID,objectRelationType) 
                  SELECT CONCAT('OO-',(@id := @id + 1)), {ocelbase}.object_object.ocel_source_id, 
                  {ocelbase}.object_object.ocel_target_id, 
                  {ocelbase}.object_object.ocel_qualifier 
                  FROM {ocelbase}.object_object LEFT JOIN {ocelbase}.event_object 
                  ON {ocelbase}.event_object.ocel_object_id = {ocelbase}.object_object.ocel_target_id 
                  OR {ocelbase}.event_object.ocel_object_id = {ocelbase}.object_object.ocel_source_id""")  
   
    #Triggers when ocel object object is updated
    c.execute(f"""USE {ocelbase}""")
    c.execute(f"""CREATE TRIGGER ootrigger AFTER INSERT ON object_object FOR EACH ROW
                INSERT INTO testing1.objectObject(fromObjectID,toObjectID,objectRelationType, objectObjectID) 
                  SELECT new.ocel_source_id AS fromObjectID, new.ocel_target_id,
                  new.ocel_qualifier AS objectRelationType,CONCAT("OO-",(Convert(SUBSTRING(max(testing1.objectObject.objectObjectID),4),INTEGER)+1))
                  FROM testing1.objectObject""")
    c.execute(f"USE testing1")
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
    c.execute(f"USE {ocelbase}")
    c.execute(f"""CREATE TRIGGER eventObjectTrigger AFTER INSERT ON event_object FOR EACH ROW 
              INSERT INTO testing1.eventObject VALUES(new.ocel_event_id, new.ocel_object_id, new.ocel_qualifier)""")
    c.execute("USE testing1")
def create_objectType(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectType (
                    objectTypeID VARCHAR(50),
                    objectType TEXT,
                    PRIMARY KEY (objectTypeID))""")
    
    c.execute(f"""INSERT INTO objectType (objectType, objectTypeID) 
                  SELECT {ocelbase}.object_map_type.ocel_type AS objectType, CONCAT('OT-',(@id := @id + 1)) FROM {ocelbase}.object_map_type""")
    #Same as the eventType one
    c.execute(f"USE {ocelbase}")
    c.execute(f"""CREATE TRIGGER objectTypetrigger AFTER INSERT ON object_map_type FOR EACH ROW
               INSERT testing1.objectType(objectType,objectTypeID)  SELECT new.ocel_type, CONCAT("OT-",Convert(SUBSTRING(max(testing1.objectType.objectTypeID),4),INTEGER)+1) from testing1.objectType""")
    c.execute(f"USE testing1")

def create_object(c):
    c.execute("""CREATE TABLE object (
                    objectID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    PRIMARY KEY (objectID))""")
    
    c.execute(f"""INSERT INTO object
                 SELECT {ocelbase}.object.ocel_id AS objectID, 
                 testing1.objectType.objectTypeID FROM {ocelbase}.object NATURAL JOIN testing1.objectType WHERE objectType = ocel_type""")

    
    c.execute(f"USE {ocelbase}") 
    c.execute(f"""CREATE TRIGGER objecttrigger AFTER INSERT ON object FOR EACH ROW 
                    INSERT testing1.object(objectID, objectTypeID) SELECT new.ocel_id, testing1.objectType.objectTypeID FROM  testing1.objectType
                   NATURAL JOIN object WHERE object.ocel_id = new.ocel_id and ocel_type = objectType.objectType""")
    c.execute("USE testing1")

def create_objectRelationEvent(c):
    c.execute("""CREATE TABLE objectRelationEvent (
                    objectRelationEventID VARCHAR(50),
                    objectObjectID VARCHAR(50),
                    eventID VARCHAR(50),
                    OOEqualifier VARCHAR(50),
                    PRIMARY KEY (objectRelationEventID))""")
    


def create_objectAttribute(c):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectAttribute (
                    objectAttributeID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    objectAttributeName VARCHAR(50),
                    PRIMARY KEY (objectAttributeID))""")
    
    c.execute(f"""SELECT CONCAT('object_',ocel_type_map) 
                  FROM {ocelbase}.object_map_type""")
    
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
            
   
    
    c.execute(f"""USE {ocelbase}""")
    c.execute(f"""CREATE TRIGGER attributeUpdate AFTER UPDATE ON object_map_type FOR EACH ROW
                      INSERT INTO objectAttribute (objectTypeID,objectAttributeName,objectAttributeID)
                        values((SELECT testing1.objectType.objectTypeID FROM testing1.objectType WHERE objectType = new.ocel_type), 
                      (SELECT COLUMN_NAME
                     FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = CONCAT('object_',new.ocel_type_map) 
                     AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'),(SELECT(CONCAT('OA-',(Convert(SUBSTRING(max(testing1.objectAttribute),4),INTEGER)+1)))))""")
    c.execute("""USE testing1""")
 
            

def create_objectAttributeValue(c):
    #Should triggers when something is added in the object type tables 
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID VARCHAR(50),
                    objectID VARCHAR(50),
                    objectAttributeValTime DATETIME,
                    objectAttributeID VARCHAR(50),
                    AttributeValue VARCHAR(50),
                    PRIMARY KEY (valueID))""")
    
    c.execute(f"""SELECT CONCAT('object_',ocel_type_map) 
                  FROM {ocelbase}.object_map_type""")
    
    objNames = c.fetchall()
    for i in objNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()
        str = ""
        for j in atrName:
        
            c.execute(f"""INSERT INTO objectAttributeValue
                         (objectID, objectAttributeValTime, objectAttributeID, AttributeValue, valueID)
                         SELECT {ocelbase}.{i[0]}.ocel_id AS objectID, 
                         {ocelbase}.{i[0]}.ocel_time AS objectAttributeValTime, objectAttributeID, 
                         CONVERT({ocelbase}.{i[0]}.{j[0]},VARCHAR(50)) AS AttributeValue, CONCAT('OAV-',(@id := @id + 1)) 
                         FROM {ocelbase}.{i[0]} join (object,objectAttribute) ON ({ocelbase}.{i[0]}.ocel_id = object.objectID 
                         AND object.objectTypeID = objectAttribute.objectTypeID AND objectAttribute.objectAttributeName = '{j[0]}')""")
           
            c.execute(f"SELECT objectAttributeID FROM objectAttribute WHERE objectAttributeName = '{j[0]}'")
            z = c.fetchall()
            str += f"((SELECT(CONCAT('OAV-',(Convert(SUBSTRING(max(testing1.objectAttributeValue),5),INTEGER)+1)))),new.ocel_id,new.ocel_time,'{z[0][0]}',new.{j[0]})," 
        str=str[:-1]
        c.execute(f"USE {ocelbase}")
       
        #Adds a new row for each line added
        c.execute(f"""CREATE TRIGGER {i[0]}trigger AFTER INSERT ON {i[0]} FOR EACH ROW 
                  INSERT INTO testing1.objectAttributeValue values{str}""")
        c.execute("USE testing1")
def create_objectAttributeValueEvent(c):
    #Should trigger when object attribute value is updated, assumes event is updated first
    c.execute("""CREATE TABLE objectAttributeValueEvent(
              valueID VARCHAR(50),
              eventID VARCHAR(50),
              OAEqualifier VARCHAR(50),
              PRIMARY KEY(valueID,eventID))""")
    
    c.execute("""INSERT INTO objectAttributeValueEvent(valueID,eventID) SELECT valueID, eventID 
              FROM objectAttributeValue NATURAL JOIN event WHERE eventTime = objectAttributeValTime""")
    
    c.execute(f"""CREATE TRIGGER objvalevent AFTER INSERT ON objectAttributeValue FOR EACH ROW
            INSERT objectAttributeValueEvent(valueID,eventID) SELECT objectAttributeValue.valueID, event.eventID 
              FROM objectAttributeValue NATURAL JOIN event WHERE eventTime = objectAttributeValTime AND valueID = new.valueID""")
def create_eventAttribute(c):
    c.execute("""SET @id = 0""")
    c.execute("""CREATE TABLE eventAttribute (
                    eventAttributeID VARCHAR(50),
                    eventTypeID VARCHAR(50),
                    eventAttributeName VARCHAR(50),
                    PRIMARY KEY (eventAttributeID))""")
    
    c.execute(f"""SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type""")
    
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
            


    c.execute(f"""USE {ocelbase}""")
    c.execute(f"""CREATE TRIGGER attributeUpdateev AFTER UPDATE ON event_map_type FOR EACH ROW
                      INSERT INTO eventAttribute (eventTypeID,eventAttributeName,eventAttributeID)
                         values((SELECT testing1.eventType.eventTypeID FROM testing1.eventType WHERE eventType = new.ocel_type), 
                      (SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = CONCAT('event_',new.ocel_type_map) 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'),(SELECT(CONCAT('EA-',(Convert(SUBSTRING(max(testing1.eventAttribute),4),INTEGER)+1)))))""")
    c.execute("""USE testing1""")
def create_eventAttributeValue(c):
     #Once again should happen when the event tables are updated
    c.execute("""CREATE TABLE eventAttributeValue (
                    eventID VARCHAR(50),
                    eventAttributeID VARCHAR(50),
                    eventAttributeValue VARCHAR(50),
                    PRIMARY KEY (eventID, eventAttributeValue)) """)        

    c.execute(f"""SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type""")
    
    eventNames = c.fetchall()
    for i in eventNames:
        c.execute(f"""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = '{i[0]}' 
                      AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'""")
        atrName = c.fetchall()
        str = ""
        for j in atrName:
            c.execute(f"""INSERT INTO eventAttributeValue
                         SELECT {ocelbase}.{i[0]}.ocel_id AS eventID, 
                         eventAttributeID, CONVERT({ocelbase}.{i[0]}.{j[0]},VARCHAR(50)) AS eventAttributeValue 
                         FROM {ocelbase}.{i[0]} join (event,eventAttribute) ON ({ocelbase}.{i[0]}.ocel_id = event.eventID 
                         AND event.eventTypeID = eventAttribute.eventTypeID AND eventAttribute.eventAttributeName = '{j[0]}')""")
            
            c.execute(f"SELECT eventAttributeID FROM eventAttribute WHERE eventAttributeName = '{j[0]}'")
            z = c.fetchall()
            
            #(SELECT(CONCAT('EAV-',(Convert(SUBSTRING(max(testing1.eventAttributeValue),5),INTEGER)+1))))
            str += f"(new.ocel_id,'{z[0][0]}',new.{j[0]})," 
        str = str[:-1]
        
        #Adds a new row for each line added
        if len(atrName) !=0:
            c.execute(f"USE {ocelbase}")
            c.execute(f"""CREATE TRIGGER {i[0]}valtrigger AFTER INSERT ON {i[0]} FOR EACH ROW 
                    INSERT testing1.eventAttributeValue values{str}""")
            c.execute("USE testing1")


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
connect.commit()


