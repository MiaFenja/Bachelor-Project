import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="1234",
)
ocelbase = "OCEL"
c = mydb.cursor()
c.execute("DROP DATABASE IF EXISTS testing1")
c.execute("CREATE DATABASE testing1")
c.execute("USE testing1")

def create_event_Ocel(c):
    c.execute("""CREATE TABLE event_ (
                    eventID VARCHAR(50), 
                    eventType TEXT, 
                    eventTime DATETIME, 
                    PRIMARY KEY (eventID))""")
    
    c.execute(f"""SELECT table_name FROM information_schema.tables 
                  WHERE table_name IN (SELECT CONCAT('event_',ocel_type_map) 
                  FROM {ocelbase}.event_map_type)""")
    
    names = c.fetchall()
    print(names)
    for t in names:
        c.execute(f"""INSERT INTO event_ SELECT ocel_id AS eventID, ocel_type AS eventType, 
                      ocel_time AS eventTime FROM {ocelbase}.{t[0]} NATURAL LEFT JOIN {ocelbase}.event_ 
                      WHERE {ocelbase}.event_.ocel_id = {ocelbase}.{t[0]}.ocel_id""")

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

create_event_Ocel(c)
create_objectObject_Ocel(c)
create_eventObject_Ocel(c)
c.execute("SELECT * FROM eventObject")
print(c.fetchall())
