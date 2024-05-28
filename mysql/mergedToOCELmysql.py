import mysql.connector
connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
c = connect.cursor()
c.execute("USE testing1")
c.execute("DROP VIEW IF EXISTS event_map_type_ocel")
c.execute("DROP VIEW IF EXISTS event_object_ocel")
c.execute("DROP VIEW IF EXISTS event_ocel")
c.execute("DROP VIEW IF EXISTS object_map_type_ocel")
c.execute("DROP VIEW IF EXISTS object_object_ocel")
c.execute("DROP VIEW IF EXISTS object_ocel")


def create_view_event_OCEL(c):
    c.execute("""CREATE VIEW event_OCEL AS SELECT event.eventID AS ocel_id, eventType.eventType AS ocel_type 
                 FROM event NATURAL JOIN eventType WHERE event.eventTypeID = eventType.eventTypeID""")
    connect.commit()


def create_view_eventMapType_OCEL(c):
    
    c.execute("CREATE VIEW event_map_type_OCEL AS SELECT eventType AS ocel_type, REPLACE(eventType, \" \", \"\") AS event_type_map FROM eventType")
    

def create_view_object_OCEL(c):
    c.execute("""CREATE VIEW object_OCEL AS SELECT object.objectID AS ocel_id, objectType.objectType AS ocel_type 
                 FROM object NATURAL JOIN objectType WHERE object.objectTypeID = objectType.objectTypeID""")
    connect.commit()

def create_view_object_object_OCEL(c):
    c.execute("""CREATE VIEW object_object_OCEL AS SELECT objectObject.fromObjectID AS ocel_source_id, 
                 objectObject.toObjectID AS ocel_target_id, objectObject.objectRelationType AS ocel_qualifier 
                 FROM objectObject""")

def create_view_objectMapType_OCEL(c):
    c.execute("CREATE VIEW object_map_type_OCEL AS SELECT objectType AS ocel_type, REPLACE(objectType,\" \",\"\") AS object_type_map FROM objectType")

def create_view_eventObject_OCEL(c):
    c.execute("""CREATE VIEW event_object_OCEL AS SELECT eventObject.eventID AS ocel_event_id, 
                 eventObject.objectID AS ocel_object_id, eventObject.OEqualifier AS ocel_qualifier 
                 FROM eventObject""")

def create_view_eventOcelTypes_OCEL(c):
    c.execute("SELECT eventTypeID FROM eventType")
    objectTypes = c.fetchall()
    for e in objectTypes:
        c.execute(f"SELECT eventAttributeName from eventAttribute WHERE eventTypeID = '{e[0]}'")
        allAttribute = c.fetchall()
        list = []
        for a in allAttribute:
            list.append(f"event_{a[0]}_{e[0].replace("-","")}_view")
           
            c.execute(f"CREATE VIEW event_{a[0]}_{e[0].replace("-","")}_view AS SELECT eventID as ocel_id, eventTime as ocel_time, eventAttributeValue AS '{a[0]}' FROM event NATURAL JOIN eventAttributeValue Natural JOiN eventAttribute WHERE eventAttributeName = '{a[0]}'  ")
        
        str = ""
        for l in list:
            str += f"{l} NATURAL JOIN "

        
        str = str[:-12]
        if len(str)>0:
            c.execute(f"CREATE VIEW event_{e[0].replace("-","")}_view_ocel AS SELECT * FROM {str}")
    connect.commit()

def create_view_objectOcelTypes_OCEL(c):
    c.execute("SELECT objectTypeID FROM objectType")
    objectTypes = c.fetchall()
    for e in objectTypes:
        c.execute(f"SELECT objectAttributeName from objectAttribute WHERE objectTypeID = '{e[0]}'")
        allAttribute = c.fetchall()
        list = []
        for a in allAttribute:
            list.append(f"object_{a[0]}_{e[0].replace("-","")}_view")
           
            c.execute(f"CREATE VIEW object_{a[0]}_{e[0].replace("-","")}_view AS SELECT objectID as ocel_id, objectAttributeValTime as ocel_time, attributeValue AS '{a[0]}' FROM objectAttributeValue Natural JOiN objectAttribute WHERE objectAttributeName = '{a[0]}'  ")
        
        str = ""
        for l in list:
            str += f"{l} NATURAL JOIN "

        
        str = str[:-12]
        if len(str)>0:
            c.execute(f"CREATE VIEW object_{e[0].replace("-","")}_view_ocel AS SELECT * FROM {str}")
       
    connect.commit()


create_view_event_OCEL(c)
create_view_eventMapType_OCEL(c)
create_view_object_OCEL(c)
create_view_object_object_OCEL(c)
create_view_objectMapType_OCEL(c)
create_view_eventObject_OCEL(c)
create_view_eventOcelTypes_OCEL(c)
create_view_objectOcelTypes_OCEL(c)

c.execute("select * from event_OCEL")
print(c.fetchall())


