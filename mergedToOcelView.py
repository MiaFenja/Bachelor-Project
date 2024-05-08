import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()

def drop_views(c):
    c.execute("""DROP VIEW IF EXISTS event_OCEL""")
    c.execute("""DROP VIEW IF EXISTS object_OCEL""")
    c.execute("""DROP VIEW IF EXISTS object_object_OCEL""")
    c.execute("""DROP VIEW IF EXISTS event_object_OCEL""")
    c.execute("""DROP VIEW IF EXISTS event_map_type_Ocel""")
    c.execute("""DROP VIEW IF EXISTS object_map_type_OCEL""")
    connect.commit()


def create_view_event(c):
    c.execute("""CREATE VIEW event_OCEL AS SELECT event.eventID AS ocel_id, eventType.eventType AS ocel_type 
                 FROM event NATURAL JOIN eventType WHERE event.eventTypeID = eventType.eventTypeID""")
    connect.commit()

def get(data):
    return data.replace(" ", "_")
def create_view_eventMapType(c):
    connect.create_function("get",1,get)
    c.execute("CREATE VIEW event_map_type_Ocel AS SELECT eventType AS ocel_type, get(eventType) AS event_type_map FROM eventType")
    

def create_view_object(c):
    c.execute("""CREATE VIEW object_OCEL AS SELECT object.objectID AS ocel_id, objectType.objectType AS ocel_type 
                 FROM object NATURAL JOIN objectType WHERE object.objectTypeID = objectType.objectTypeID""")
    connect.commit()

def create_view_object_object(c):
    c.execute("""CREATE VIEW object_object_OCEL AS SELECT objectObject.fromObjectID AS ocel_source_id, 
                 objectObject.toObjectID AS ocel_target_id, objectObject.objectRelationType AS ocel_qualifier 
                 FROM objectObject""")

def create_view_objectMapType(c):
    c.execute("CREATE VIEW object_map_type_Ocel AS SELECT objectType AS ocel_type, get(objectType) AS object_type_map FROM objectType")

def create_view_eventObject(c):
    c.execute("""CREATE VIEW event_object_OCEL AS SELECT eventObject.eventID AS ocel_event_id, 
                 eventObject.objectID AS ocel_object_id, eventObject.OEqualifier AS ocel_qualifier 
                 FROM eventObject""")

def create_view_eventOcelTypes(c):
    return

def create_view_objectOcelTypes(c):
    return

drop_views(c)
create_view_event(c)
create_view_eventMapType(c)
create_view_object(c)
create_view_object_object(c)
create_view_objectMapType(c)
create_view_eventObject(c)
create_view_eventOcelTypes(c)
create_view_objectOcelTypes(c)

c.execute("select * from event_object_OCEL")
print(c.fetchall())



