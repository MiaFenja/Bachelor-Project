def create_eventType_OCEL(c,connect,ocelbase):
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
              # INSERT merged.eventType(eventType,eventTypeID)  SELECT new.ocel_type, CONCAT("ET-",Convert(SUBSTRING(max(merged.eventType.eventTypeID),4),INTEGER)+1) from merged.eventType""")
    #c.execute(f"USE merged")
    connect.commit()

def create_event_OCEL(c,connect,ocelbase):
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
        c.execute(f"""INSERT INTO event SELECT {ocelbase}.event.ocel_id, eventTypeID, ocel_time from {ocelbase}.event JOIN eventType ON ocel_type = eventType NATURAL JOIN {ocelbase}.{t[0]}""")
        c.execute(f"USE {ocelbase}") 
        c.execute(f"""CREATE TRIGGER {t[0]}trigger AFTER INSERT ON {ocelbase}.{t[0]} FOR EACH ROW 
                    INSERT merged.event(eventID, eventTypeID,eventTime) SELECT new.ocel_id, merged.eventType.eventTypeID, new.ocel_time FROM  merged.eventType NATURAL JOIN event WHERE event.ocel_id = new.ocel_id  and ocel_type = eventType.eventType""")
        c.execute("USE merged")
    connect.commit()


def create_objectObject_OCEL(c,connect,ocelbase):
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
                  FROM {ocelbase}.object_object""")  
   
    #Triggers when ocel object object is updated
    c.execute(f"""USE {ocelbase}""")
    c.execute(f"""CREATE TRIGGER ootrigger AFTER INSERT ON object_object FOR EACH ROW
                INSERT INTO merged.objectObject(fromObjectID,toObjectID,objectRelationType, objectObjectID) 
                  SELECT new.ocel_source_id AS fromObjectID, new.ocel_target_id,
                  new.ocel_qualifier AS objectRelationType,CONCAT("OO-",(Convert(SUBSTRING(max(merged.objectObject.objectObjectID),4),INTEGER)+1))
                  FROM merged.objectObject""")
    c.execute(f"USE merged")
    connect.commit()


def create_eventObject_OCEL(c,connect,ocelbase):
    c.execute("""CREATE TABLE eventObject (
                    eventID VARCHAR(50), 
                    objectID VARCHAR(50),
                    EOqualifier TEXT, 
                    PRIMARY KEY (eventID,objectID))""")
    
    c.execute(f"""INSERT INTO eventObject 
                  SELECT {ocelbase}.event_object.ocel_event_id AS eventID, 
                  {ocelbase}.event_object.ocel_object_id AS objectID, 
                  {ocelbase}.event_object.ocel_qualifier AS EOqualifier 
                  FROM {ocelbase}.event_object""")
    c.execute(f"USE {ocelbase}")
    c.execute(f"""CREATE TRIGGER eventObjectTrigger AFTER INSERT ON event_object FOR EACH ROW 
              INSERT INTO merged.eventObject VALUES(new.ocel_event_id, new.ocel_object_id, new.ocel_qualifier)""")
    c.execute("USE merged")


def create_objectType_OCEL(c,connect,ocelbase):
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectType (
                    objectTypeID VARCHAR(50),
                    objectType TEXT,
                    PRIMARY KEY (objectTypeID))""")
    
    c.execute(f"""INSERT INTO objectType (objectType, objectTypeID) 
                  SELECT {ocelbase}.object_map_type.ocel_type AS objectType, CONCAT('OT-',(@id := @id + 1)) FROM {ocelbase}.object_map_type""")
    #Same as the eventType one
    #c.execute(f"USE {ocelbase}")
    #c.execute(f"""CREATE TRIGGER objectTypetrigger AFTER INSERT ON object_map_type FOR EACH ROW
              # INSERT merged.objectType(objectType,objectTypeID)  SELECT new.ocel_type, CONCAT("OT-",Convert(SUBSTRING(max(merged.objectType.objectTypeID),4),INTEGER)+1) from merged.objectType""")
    #c.execute(f"USE merged")
    connect.commit()


def create_object_OCEL(c,connect,ocelbase):
    c.execute("""CREATE TABLE object (
                    objectID VARCHAR(50),
                    objectTypeID VARCHAR(50),
                    PRIMARY KEY (objectID))""")
    
    c.execute(f"""INSERT INTO object
                 SELECT {ocelbase}.object.ocel_id AS objectID, 
                 merged.objectType.objectTypeID FROM {ocelbase}.object LEFT JOIN merged.objectType ON {ocelbase}.object.ocel_type = objectType.objectType""")

    
    c.execute(f"USE {ocelbase}") 
    c.execute(f"""CREATE TRIGGER objecttrigger AFTER INSERT ON object FOR EACH ROW 
                    INSERT merged.object(objectID, objectTypeID) SELECT new.ocel_id, merged.objectType.objectTypeID FROM  merged.objectType
                   NATURAL JOIN object WHERE object.ocel_id = new.ocel_id and ocel_type = objectType.objectType""")
    c.execute("USE merged")
    connect.commit()


def create_objectRelationEvent_OCEL(c,connect,ocelbase):
    c.execute("""CREATE TABLE objectRelationEvent (
                    objectRelationEventID VARCHAR(50),
                    objectObjectID VARCHAR(50),
                    eventID VARCHAR(50),
                    OOEqualifier VARCHAR(50),
                    PRIMARY KEY (objectRelationEventID))""")
    
    connect.commit()

def create_objectAttribute_OCEL(c,connect,ocelbase):
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
            
   
    
   # c.execute(f"""USE {ocelbase}""")
    #c.execute(f"""CREATE TRIGGER attributeUpdate AFTER UPDATE ON object_map_type FOR EACH ROW
                      #INSERT INTO objectAttribute (objectTypeID,objectAttributeName,objectAttributeID)
                        #values((SELECT merged.objectType.objectTypeID FROM merged.objectType WHERE objectType = new.ocel_type), 
                      #(SELECT COLUMN_NAME
                     #FROM INFORMATION_SCHEMA.COLUMNS
                     # WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = CONCAT('object_',new.ocel_type_map) 
                     #AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'),(SELECT(CONCAT('OA-',(Convert(SUBSTRING(max(merged.objectAttribute),4),INTEGER)+1)))))""")
   # c.execute("""USE merged""")
    connect.commit()
            

def create_objectAttributeValue_OCEL(c,connect,ocelbase):
    #Should triggers when something is added in the object type tables 
    c.execute("""SET @id = 0;""")
    c.execute("""CREATE TABLE objectAttributeValue (
                    valueID VARCHAR(50),
                    instanceID VARCHAR(50),
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
        count = 1
        for j in atrName:
            c.execute(f"""INSERT INTO objectAttributeValue
                         (objectID, instanceID, objectAttributeValTime, objectAttributeID, AttributeValue, valueID)
                         SELECT ocel_id,CONCAT("OG-", ROW_NUMBER() OVER ()) AS instanceID,ocel_time, objectAttributeID, 
                         cast({ocelbase}.{i[0]}.{j[0]} as VARCHAR(50)) AS AttributeValue, CONCAT('OAV-',(@id := @id + 1)) FROM {ocelbase}.{i[0]}
                           inner join object ON {ocelbase}.{i[0]}.ocel_id = object.objectID inner join 
                           objectAttribute ON object.objectTypeID = objectAttribute.objectTypeID
                             AND objectAttribute.objectAttributeName
                               = '{j[0]}'""")
           
            c.execute(f"SELECT objectAttributeID FROM objectAttribute WHERE objectAttributeName = '{j[0]}'")
            z = c.fetchall()

            str += f"""(CONCAT("OAV-", ((SELECT count(valueID)+{count} FROM (SELECT * FROM merged.objectAttributeValue) as o ))),CONCAT("OG-",((SELECT count(instanceID)+1 FROM  (SELECT * FROM merged.objectAttributeValue WHERE objectID = new.ocel_id) as o))),new.ocel_id,new.ocel_time,'{z[0][0]}',new.{j[0]}),""" 
            count += 1
        str=str[:-1]
        c.execute(f"USE {ocelbase}")
       
        #Adds a new row for each line added
        c.execute(f"""CREATE TRIGGER {i[0]}trigger AFTER INSERT ON {i[0]} FOR EACH ROW 
                   INSERT INTO merged.objectAttributeValue SELECT * from (values{str}) as t""")
        c.execute("USE merged")
    connect.commit()


def create_objectAttributeValueEvent_OCEL(c,connect,ocelbase):
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
    connect.commit()


def create_eventAttribute_OCEL(c,connect,ocelbase):
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
            
    connect.commit()

   # c.execute(f"""USE {ocelbase}""")
   # c.execute(f"""CREATE TRIGGER attributeUpdateev AFTER UPDATE ON event_map_type FOR EACH ROW
     #                 INSERT INTO eventAttribute (eventTypeID,eventAttributeName,eventAttributeID)
     #                    values((SELECT merged.eventType.eventTypeID FROM merged.eventType WHERE eventType = new.ocel_type), 
     #                 (SELECT COLUMN_NAME
      #                FROM INFORMATION_SCHEMA.COLUMNS
      #                WHERE TABLE_SCHEMA = '{ocelbase}' AND TABLE_NAME = CONCAT('event_',new.ocel_type_map) 
       #               AND COLUMN_NAME != 'ocel_id' AND COLUMN_NAME != 'ocel_time'),(SELECT(CONCAT('EA-',(Convert(SUBSTRING(max(merged.eventAttribute),4),INTEGER)+1)))))""")
   # c.execute("""USE merged""")


def create_eventAttributeValue_OCEL(c,connect,ocelbase):
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
            
            #(SELECT(CONCAT('EAV-',(Convert(SUBSTRING(max(merged.eventAttributeValue),5),INTEGER)+1))))
            str += f"(new.ocel_id,'{z[0][0]}',new.{j[0]})," 
        str = str[:-1]
        
        #Adds a new row for each line added
        if len(atrName) !=0:
            c.execute(f"USE {ocelbase}")
            c.execute(f"""CREATE TRIGGER {i[0]}valtrigger AFTER INSERT ON {i[0]} FOR EACH ROW 
                    INSERT merged.eventAttributeValue values{str}""")
            c.execute("USE merged")
    connect.commit()


