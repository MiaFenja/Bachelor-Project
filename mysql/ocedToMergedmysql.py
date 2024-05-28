import mysql.connector
connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
ocedbase = "OCED"

c = connect.cursor()
c.execute("DROP DATABASE IF EXISTS testing1")
c.execute("CREATE DATABASE testing1")
c.execute("USE testing1")


def create_eventType_OCED(c,connect):
    c.execute("""CREATE TABLE eventType (
                eventTypeID VARCHAR(50) PRIMARY KEY,
                eventType TEXT
                )""")
    c.execute("""SET @id = 0""")
    c.execute(f"""SELECT DISTINCT eventType FROM {ocedbase}.event""")
    eventTypes = c.fetchall()
    for et in eventTypes:
        c.execute(f"""INSERT INTO eventType
              values((CONCAT('ET-',(@id := @id +1))), '{et[0]}')
              """)


def create_event_OCED(c,connect):
    c.execute("""CREATE TABLE event (
                    eventID VARCHAR(50) PRIMARY KEY, 
                    eventTypeID VARCHAR(50), 
                    eventTime DATETIME)""")
    
    c.execute(f"""INSERT INTO event SELECT eventID, eventTypeID, timestamp AS eventTime FROM {ocedbase}.event NATURAL JOIN eventType""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER eventTrigger AFTER INSERT ON event FOR EACH ROW
               INSERT INTO testing1.event values(new.eventID, (SELECT DISTINCT eventTypeID FROM event NATURAL JOIN testing1.eventType WHERE new.eventType = eventType), new.timestamp)""")
    c.execute("USE testing1")
    connect.commit()

def create_objectObject_OCED(c,connect):
    c.execute("""CREATE TABLE objectObject (
                    objectObjectID VARCHAR(50),
                    fromObjectID VARCHAR(50), 
                    toObjectID  VARCHAR(50), 
                    objectRelationType VARCHAR(50),
                    PRIMARY KEY (objectObjectID))""")
    c.execute(f"""INSERT INTO objectObject SELECT * FROM {ocedbase}.objectObject""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER objectObjectTrigger AFTER INSERT ON objectObject FOR EACH ROW
              INSERT INTO testing1.objectObject values(new.objectObjectID,new.fromObjectID,new.toObjectID,new.objectRelationType )""")
    c.execute(f"USE testing1")
    connect.commit()

def create_eventObject_OCED(c,connect):
    c.execute("""CREATE TABLE eventObject (
                    eventID VARCHAR(50), 
                    objectID VARCHAR(50),
                    EOqualifier VARCHAR(50), 
                    PRIMARY KEY (eventID,objectID))""")
    c.execute(f"""INSERT INTO eventObject SELECT eventID, objectID, EOqualifier FROM {ocedbase}.eventObject""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER eventObjectTrigger AFTER INSERT ON eventObject FOR EACH ROW
            INSERT INTO testing1.eventObject VALUES(new.eventID, new.objectID, new.EOqualifier)""")
    c.execute(f"USE testing1")
    connect.commit()
    
def create_objectType_OCED(c,connect):
    c.execute("""CREATE TABLE objectType (
                    objectTypeID VARCHAR(50),
                    objectType VARCHAR(50),
                    PRIMARY KEY (objectTypeID))""")
    
    c.execute("""SET @id = 0""")
    c.execute(f"""SELECT DISTINCT objectType FROM {ocedbase}.object""")
    objectTypes = c.fetchall()
    for ot in objectTypes:
        c.execute(f"""INSERT INTO objectType
              values((CONCAT('OT-',(@id := @id +1))), '{ot[0]}')
              """)


def create_object_OCED(c,connect):
    c.execute("""CREATE TABLE object (
                    objectID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    PRIMARY KEY (objectID))""")
    c.execute(f"""INSERT INTO object SELECT objectID, objectTypeID FROM {ocedbase}.object NATURAL JOIN objectType""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER objectTrigger AFTER INSERT ON object FOR EACH ROW
              INSERT testing1.object values(new.objectID,(SELECT objectTypeID FROM testing1.objectType Where testing1.objectType.objectType = new.objectType))""")
    c.execute(f"USE testing1")
    connect.commit()

def create_objectRelationEvent_OCED(c,connect):
    c.execute("""CREATE TABLE objectRelationEvent (
                    objectRelationEventID VARCHAR(50),
                    objectObjectID VARCHAR(50),
                    eventID VARCHAR(50),
                    OOEqualifier VARCHAR(50),
                    PRIMARY KEY (objectRelationEventID))""")
    c.execute(f"SET @id = 0")
    c.execute(f"""INSERT INTO objectRelationEvent SELECT CONCAT('ORE-',(@id := @id + 1)), objectObjectID, eventID, OOEqualifier FROM {ocedbase}.objectRelationEvent""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER objectRelationetrigger AFTER INSERT ON objectRelationEvent FOR EACH ROW
               INSERT testing1.objectRelationEvent  VALUES((SELECT CONCAT("ORE-",Count(*)) FROM objectRelationEvent), new.objectObjectID, new.eventID, new.OOEqualifier)""")
    c.execute(f"USE testing1")
    connect.commit()

def create_objectAttribute_OCED(c,connect):
    c.execute("""CREATE TABLE objectAttribute (
                    objectAttributeID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    objectAttributeName VARCHAR(50),
                    PRIMARY KEY (objectAttributeID))""")
    c.execute(f"""SELECT DISTINCT objectType.objectTypeID AS objectTypeID, objectAttributeValue.objectAttributeName FROM objectType NATURAL JOIN object NATURAL JOIN {ocedbase}.objectAttributeValue""")
    objectat = c.fetchall()
    c.execute("""SET @id = 0""")
    for oa in objectat:
        print(oa[0])
        c.execute(f"""INSERT INTO objectAttribute
                  values(CONCAT('OA-',(@id := @id + 1)),'{oa[0]}', '{oa[1]}')""")
    c.execute(f"""USE {ocedbase}""")
    c.execute(f"""CREATE TRIGGER objectatTrigger AFTER INSERT ON objectAttributeValue FOR EACH ROW 
              INSERT testing1.objectAttribute
      SELECT DISTINCT (SELECT CONCAT('OA-',(Convert(SUBSTRING(max(testing1.objectAttribute.objectAttributeID),4),INTEGER)+1)) FROM testing1.objectAttribute)
, objectTypeID, new.objectAttributeName
               FROM testing1.objectType NATURAL JOIN testing1.object NATURAL JOIN objectAttributeValue
               WHERE new.objectAttributeName = objectAttributeName and (objectTypeID NOT IN (SELECT objectTypeID FROM testing1.objectAttribute) OR new.objectAttributeName NOT IN (SELECT objectAttributeName FROM testing1.objectAttribute))"""  )
    c.execute(f"""USE testing1""")
    connect.commit()
            

def create_objectAttributeValue_OCED(c,connect):
    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID VARCHAR(50),
                    objectID VARCHAR(50),
                    objectAttributeValTime DATETIME,
                    objectAttributeID VARCHAR(50),
                    attributeValue VARCHAR(50),
                    PRIMARY KEY (valueID))""")
    c.execute(f"""INSERT INTO objectAttributeValue (valueID, objectID, objectAttributeID, attributeValue) 
                 SELECT objectAttributeValueID AS valueID, objectID, objectAttributeID, objectAttributeValue AS attributeValue 
                 FROM {ocedbase}.objectAttributeValue NATURAL JOIN objectAttribute""")
    c.execute(f"""USE {ocedbase}""")
    c.execute(f"""CREATE TRIGGER oavtrigger AFTER INSERT ON objectAttributeValue FOR EACH ROW 
              INSERT testing1.objectAttributeValue(valueID,objectID,objectAttributeID, attributeValue) values(new.objectAttributeValueID, new.objectID, (SELECT objectAttributeID FROM testing1.objectAttribute Where new.objectAttributeName = testing1.objectAttribute.objectAttributeName), new.objectAttributeValue)""")
    c.execute(f"""USE testing1""")
    connect.commit()

def create_objectAttributeValueEvent_OCED(c,connect):
    c.execute("""CREATE TABLE objectAttributeValueEvent (
              valueID VARCHAR(50),
              eventID VARCHAR(50),
              OAEqualifier VARCHAR(50),
              PRIMARY KEY(valueID,eventID))""")
    c.execute(f"SET @id = 0")
    c.execute(f"""INSERT INTO objectAttributeValueEvent SELECT objectAttributeValueID AS valueID, eventID, OAEqualifier 
                 FROM {ocedbase}.objectAttributeValueEvent""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER oaveTrigger AFTER INSERT ON objectAttributeValueEvent FOR EACH ROW
              INSERT testing1.objectAttributeValueEvent values(new.objectAttributeValueID,new.eventID, new.OAEqualifier)""")
    c.execute(f"USE testing1")
    connect.commit()
 
            
def create_eventAttribute_OCED(c,connect):
    c.execute("""CREATE TABLE eventAttribute (
                    eventAttributeID VARCHAR(50),
                    eventTypeID VARCHAR(50),
                    eventAttributeName VARCHAR(50),
                    PRIMARY KEY (eventAttributeID))""")
    c.execute(f"SELECT DISTINCT eventTypeID, eventAttributeName FROM eventType NATURAL JOIN event NAtural JOIN {ocedbase}.eventAttributeValue")
    eventat = c.fetchall()
    c.execute("""SET @id = 0""")
    for ea in eventat:
        c.execute(f"""INSERT INTO eventAttribute
                  values(CONCAT('EA-',(@id := @id + 1)),'{ea[0]}', '{ea[1]}')""")
    c.execute(f"""USE {ocedbase}""")
    c.execute(f"""CREATE TRIGGER eventatTrigger AFTER INSERT ON eventAttributeValue FOR EACH ROW 
              INSERT testing1.eventAttribute
      SELECT DISTINCT (SELECT CONCAT('EA-',(Convert(SUBSTRING(max(testing1.eventAttribute.eventAttributeID),4),INTEGER)+1)) FROM testing1.eventAttribute)
, eventTypeID, new.eventAttributeName
               FROM testing1.eventType NATURAL JOIN testing1.event NATURAL JOIN eventAttributeValue
               WHERE new.eventAttributeName = eventAttributeName and (eventTypeID NOT IN (SELECT eventTypeID FROM testing1.eventAttribute) OR new.eventAttributeName NOT IN (SELECT eventAttributeName FROM testing1.eventAttribute))"""  )
    c.execute(f"""USE testing1""")
    connect.commit()


def create_eventAttributeValue_OCED(c,connect):
    c.execute("""CREATE TABLE eventAttributeValue (
                    eventID VARCHAR(50),
                    eventAttributeID VARCHAR(50),
                    eventAttributeValue VARCHAR(50),
                    PRIMARY KEY (eventID, eventAttributeID)) """) 
    c.execute(f"""INSERT INTO eventAttributeValue SELECT {ocedbase}.eventAttributeValue.eventID, eventAttribute.eventAttributeID, 
                 {ocedbase}.eventAttributeValue.eventAttributeValue 
                 FROM {ocedbase}.eventAttributeValue NATURAL JOIN event NATURAL JOIN eventAttribute""")
    c.execute(f"USE {ocedbase}")
    c.execute(f"""CREATE TRIGGER eavtrigger AFTER INSERT ON eventAttributeValue FOR EACH ROW 
              INSERT testing1.eventAttributeValue(eventID,eventAttributeID, eventAttributeValue) values(new.eventID, (SELECT eventAttributeID from testing1.eventAttribute NATURAL JOIN testing1.event NATURAL JOIN  testing1.eventType where new.eventAttributeName = eventAttributeName AND eventID = new.eventID), new.eventAttributeValue)""")
    c.execute(f"USE testing1")
    connect.commit()

 
create_eventType_OCED(c,connect)
create_event_OCED(c,connect)
create_eventObject_OCED(c,connect)
create_objectObject_OCED(c,connect)
create_objectType_OCED(c,connect)
create_object_OCED(c,connect)
create_objectRelationEvent_OCED(c,connect)
create_objectAttribute_OCED(c,connect)
create_objectAttributeValue_OCED(c,connect)
create_objectAttributeValueEvent_OCED(c,connect)
create_eventAttribute_OCED(c,connect)
create_eventAttributeValue_OCED(c,connect)