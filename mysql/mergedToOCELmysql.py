def create_view_event_OCEL(c,connect):
    c.execute("""CREATE VIEW event_OCEL AS SELECT event.eventID AS ocel_id, eventType.eventType AS ocel_type 
                 FROM event NATURAL JOIN eventType WHERE event.eventTypeID = eventType.eventTypeID""")
    connect.commit()


def create_view_eventMapType_OCEL(c,connect):
    
    c.execute("CREATE VIEW event_map_type_OCEL AS SELECT eventType AS ocel_type, REPLACE(eventType, \" \", \"\") AS event_type_map FROM eventType")
    

def create_view_object_OCEL(c,connect):
    c.execute("""CREATE VIEW object_OCEL AS SELECT object.objectID AS ocel_id, objectType.objectType AS ocel_type 
                 FROM object NATURAL JOIN objectType WHERE object.objectTypeID = objectType.objectTypeID""")
    connect.commit()

def create_view_objectObject_OCEL(c,connect):
    c.execute("""CREATE VIEW object_object_OCEL AS SELECT objectObject.fromObjectID AS ocel_source_id, 
                 objectObject.toObjectID AS ocel_target_id, objectObject.objectRelationType AS ocel_qualifier 
                 FROM objectObject""")

def create_view_objectMapType_OCEL(c,connect):
    c.execute("CREATE VIEW object_map_type_OCEL AS SELECT objectType AS ocel_type, REPLACE(objectType,\" \",\"\") AS object_type_map FROM objectType")

def create_view_eventObject_OCEL(c,connect):
    c.execute("""CREATE VIEW event_object_OCEL AS SELECT eventObject.eventID AS ocel_event_id, 
                 eventObject.objectID AS ocel_object_id, eventObject.OEqualifier AS ocel_qualifier 
                 FROM eventObject""")

def create_view_eventOcelTypes_OCEL(c,connect):
    c.execute("SELECT eventType, eventTypeID FROM eventType")
    tablenames = c.fetchall()

    for n in tablenames:
        tablename = f"event_{n[0].replace(' ','')}"
        c.execute(f"SELECT eventAttributeName, eventAttributeID from eventAttribute WHERE eventTypeID = '{n[1]}'")
        str = ""
        at = c.fetchall()
        for e in at:
            c.execute(f"""CREATE VIEW {e[0].replace(" ","")}{n[0].replace(" ","")}view AS SELECT eventID, eventTime, eventAttributeValue AS {e[0]} FROM event NATURAL JOIN eventAttribute NATURAL JOIN eventAttributeValue WHERE eventAttributeID = '{e[1]}' AND eventTypeID = '{n[1]}'""")
            str = str + f"{e[0].replace(' ','')}{n[0].replace(' ','')}view NATURAL JOIN "
        str = str[:-13]
        if len(at)>0:
            c.execute(f"""CREATE VIEW {tablename} AS SELECT DISTINCT * FROM {str}""")
        else:
            c.execute(f"""CREATE VIEW {tablename} AS SELECT eventID, eventTime FROM event where eventTypeID = '{n[1]}'""")
           
    connect.commit()

def create_view_objectOcelTypes_OCEL(c,connect):
    c.execute("SELECT objectType, objectTypeID FROM objectType")
    tablenames = c.fetchall()
    for n in tablenames:
        c.execute(f"SELECT objectAttributeName, objectAttributeID from objectAttribute WHERE objectTypeID = '{n[1]}'")
        at = c.fetchall()
        tablename = f"object_{n[0].replace(' ','')}"
        str = ""
        for e in at:
            c.execute(f"""CREATE VIEW {e[0].replace(" ","")}{n[0].replace(" ","")}view AS SELECT objectID, objectAttributeValTime, AttributeValue as {e[0]} FROM objectAttribute Natural JOIN objectAttributeValue WHERE objectAttributeID = '{e[1]}' AND objectTypeID = '{n[1]}'""")
            str = str + f"{e[0].replace(' ','')}{n[0].replace(' ','')}view natural join "
        str = str[:-13]
        if len(at)>0:
            c.execute(f"""CREATE VIEW {tablename} AS SELECT DISTINCT * FROM {str}""")
        else:
            c.execute(f"""CREATE VIEW {tablename} AS SELECT objectID, objectValTime FROM objectAttributeValue""")
    connect.commit()



