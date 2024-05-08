import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()

def drop_views(c):
    c.execute("""SELECT name FROM sqlite_master WHERE type = 'view' AND name LIKE '%OCEL'""")
    views = c.fetchall()
    for i in views:
        c.execute(f"""DROP VIEW IF EXISTS {i[0]}""")
    connect.commit()


def create_view_event(c):
    c.execute("""CREATE VIEW event_OCEL AS SELECT event.eventID AS ocel_id, eventType.eventType AS ocel_type 
                 FROM event NATURAL JOIN eventType WHERE event.eventTypeID = eventType.eventTypeID""")
    connect.commit()

def get(data):
    return data.replace(" ", "_")

def create_view_eventMapType(c):
    connect.create_function("get",1,get)
    c.execute("CREATE VIEW event_map_type_OCEL AS SELECT eventType AS ocel_type, get(eventType) AS event_type_map FROM eventType")
    

def create_view_object(c):
    c.execute("""CREATE VIEW object_OCEL AS SELECT object.objectID AS ocel_id, objectType.objectType AS ocel_type 
                 FROM object NATURAL JOIN objectType WHERE object.objectTypeID = objectType.objectTypeID""")
    connect.commit()

def create_view_object_object(c):
    c.execute("""CREATE VIEW object_object_OCEL AS SELECT objectObject.fromObjectID AS ocel_source_id, 
                 objectObject.toObjectID AS ocel_target_id, objectObject.objectRelationType AS ocel_qualifier 
                 FROM objectObject""")

def create_view_objectMapType(c):
    c.execute("CREATE VIEW object_map_type_OCEL AS SELECT objectType AS ocel_type, get(objectType) AS object_type_map FROM objectType")

def create_view_eventObject(c):
    c.execute("""CREATE VIEW event_object_OCEL AS SELECT eventObject.eventID AS ocel_event_id, 
                 eventObject.objectID AS ocel_object_id, eventObject.OEqualifier AS ocel_qualifier 
                 FROM eventObject""")

def create_view_eventOcelTypes(c):
    c.execute("""SELECT eventTypeID, get(eventType) FROM eventType""")
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

def create_view_objectOcelTypes(c):
    c.execute("""SELECT objectTypeID, get(objectType) FROM objectType""")
    eventTypes = c.fetchall()

    for i in eventTypes:
        c.execute(f"""SELECT objectAttributeName, objectAttributeID FROM objectAttribute WHERE objectTypeID = '{i[0]}'""")
        attributeNames = c.fetchall()
        str = ""
        if len(attributeNames) > 0:
            for j in attributeNames:
                str += ", ( SELECT attributeValue AS " + j[0] + " FROM objectAttributeValue WHERE objectAttributeValue.objectAttributeID = '"+ j[1] +"') "
        c.execute(f"""CREATE VIEW object_{i[1]}_OCEL AS SELECT object.objectID AS ocel_id, objectAttributeValue.objectAttributeValTime AS ocel_time {str} 
                      FROM object NATURAL JOIN objectAttributeValue NATURAL JOIN objectAttribute WHERE object.objectTypeID = '{i[0]}'""")
    connect.commit()

drop_views(c)
create_view_event(c)
create_view_eventMapType(c)
create_view_object(c)
create_view_object_object(c)
create_view_objectMapType(c)
create_view_eventObject(c)
# create_view_eventOcelTypes(c)
# create_view_objectOcelTypes(c)

c.execute("select * from event_OCEL")
print(c.fetchall())


