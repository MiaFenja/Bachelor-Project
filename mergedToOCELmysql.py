import mysql.connector
connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
c = connect.cursor()
c.execute("USE testing1")
c.execute("DROP VIEW event_map_type_ocel")
c.execute("DROP VIEW event_object_ocel")
c.execute("DROP VIEW event_ocel")
c.execute("DROP VIEW object_map_type_ocel")
c.execute("DROP VIEW object_object_ocel")
c.execute("DROP VIEW object_ocel")


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
    c.execute("""SELECT eventTypeID, REPLACE(eventType,\" \",\"\") FROM eventType""")
    eventTypes = c.fetchall()

    for i in eventTypes:
        c.execute(f"""SELECT eventAttributeName, eventAttributeID FROM eventAttribute WHERE eventTypeID = '{i[0]}'""")
        attributeNames = c.fetchall()
        str = ""
        if len(attributeNames) > 0:
            for j in attributeNames:
                str += ", ( SELECT eventAttributeValue AS " + j[0] + " FROM eventAttributeValue WHERE eventAttributeValue.eventAttributeID = '"+ j[1] +"') "
        c.execute(f"""CREATE VIEW event_{i[1]}_OCEL AS SELECT event.eventID AS ocel_id, event.eventTime AS ocel_time {str} 
                      FROM event NATURAL JOIN eventAttributeValue NATURAL JOIN eventAttribute WHERE event.eventTypeID = '{i[0]}'""")
    connect.commit()

def create_view_objectOcelTypes_OCEL(c):
    c.execute("""SELECT objectTypeID, REPLACE(objectType,\" \",\"\") FROM objectType""")
    eventTypes = c.fetchall()

    for i in eventTypes:
        c.execute(f"""SELECT objectAttributeName, objectAttributeID FROM objectAttribute WHERE objectTypeID = '{i[0]}'""")
        attributeNames = c.fetchall()
        str = ""
        if len(attributeNames) > 0:
            allvalsandnames = []
            for j in attributeNames:
                c.execute(" SELECT attributeValue, objectID FROM objectAttributeValue WHERE objectAttributeValue.objectAttributeID = '"+ j[1] +"'")
                allvalsandnames.append((j[0],c.fetchall()))
        print(allvalsandnames)
        c.execute(f"CREATE VIEW {i[0]}")
       
    connect.commit()


create_view_event_OCEL(c)
create_view_eventMapType_OCEL(c)
create_view_object_OCEL(c)
create_view_object_object_OCEL(c)
create_view_objectMapType_OCEL(c)
create_view_eventObject_OCEL(c)
# create_view_eventOcelTypes_OCEL(c)
#create_view_objectOcelTypes_OCEL(c)

c.execute("select * from event_OCEL")
print(c.fetchall())


