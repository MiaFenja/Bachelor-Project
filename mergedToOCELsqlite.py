def create_new_event_OCEL(c, connect):
    c.execute(f"""CREATE TABLE IF NOT EXISTS "event" (
	`ocel_id` TEXT,
    `ocel_type` TEXT,
    PRIMARY KEY (`ocel_id`),
    FOREIGN KEY (`ocel_type`) REFERENCES event_map_type (`ocel_type`))
""")
    c.execute("""INSERT INTO event SELECT merged.event.eventID AS ocel_id, merged.eventType.eventType AS ocel_type 
                 FROM merged.event NATURAL JOIN merged.eventType WHERE merged.event.eventTypeID = merged.eventType.eventTypeID""")
    connect.commit()

def get(data):
    return data.replace(" ", "")

def create_new_eventMapType_OCEL(c, connect):
    connect.create_function("get",1,get)
    c.execute(f"""CREATE TABLE IF NOT EXISTS "event_map_type" (
	`ocel_type` TEXT,
    `ocel_type_map` TEXT,
    PRIMARY KEY (`ocel_type`))
    """)
    c.execute("INSERT INTO event_map_type SELECT eventType AS ocel_type, get(eventType) AS event_type_map FROM merged.eventType")
    

def create_new_object_OCEL(c, connect):
    
    c.execute("""CREATE TABLE IF NOT EXISTS "object" (
	`ocel_id` TEXT,
    `ocel_type` TEXT,
    PRIMARY KEY (`ocel_id`),
    FOREIGN KEY (`ocel_type`) REFERENCES object_map_type (`ocel_type`)
)""")
    c.execute("""INSERT INTO object SELECT merged.object.objectID AS ocel_id, merged.objectType.objectType AS ocel_type 
                 FROM merged.object NATURAL JOIN merged.objectType WHERE merged.object.objectTypeID = merged.objectType.objectTypeID""")
    connect.commit()

def create_new_objectObject_OCEL(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "object_object" (
	`ocel_source_id` TEXT,
    `ocel_target_id` TEXT,
    `ocel_qualifier` TEXT,
    PRIMARY KEY (`ocel_source_id`, `ocel_target_id`, `ocel_qualifier`)
)""")

    c.execute("""INSERT INTO object_object SELECT merged.objectObject.fromObjectID AS ocel_source_id, 
                 merged.objectObject.toObjectID AS ocel_target_id, merged.objectObject.objectRelationType AS ocel_qualifier 
                 FROM merged.objectObject""")

def create_new_objectMapType_OCEL(c, connect):
    c.execute("""CREATE TABLE IF NOT EXISTS "object_map_type" (
	`ocel_type` TEXT,
    `ocel_type_map` TEXT,
    PRIMARY KEY (`ocel_type`))
""")
    c.execute("INSERT INTO object_map_type SELECT objectType AS ocel_type, get(objectType) AS object_type_map FROM merged.objectType")

def create_new_eventObject_OCEL(c, connect):
    c.execute(""" CREATE TABLE IF NOT EXISTS "event_object" (
	`ocel_event_id` TEXT,
    `ocel_object_id` TEXT,
    `ocel_qualifier` TEXT,
    PRIMARY KEY (`ocel_event_id`, `ocel_object_id`, `ocel_qualifier`)
    )""")
    c.execute("""INSERT INTO event_object SELECT merged.eventObject.eventID AS ocel_event_id, 
                 merged.eventObject.objectID AS ocel_object_id, merged.eventObject.EOqualifier AS ocel_qualifier 
                 FROM merged.eventObject""")

def create_new_eventOcelTypes_OCEL(c, connect):
   c.execute("""SELECT eventType, eventTypeID FROM merged.eventType""")
   tablenames = c.fetchall()
   for n in tablenames:
       tablename = f"event_{n[0].replace(' ','')}"
       c.execute(f"SELECT eventAttributeName, eventAttributeID FROM merged.eventAttribute where eventTypeID ='{n[1]}'")
       str = ""
       at = c.fetchall()
       for e in at:
           str += f"'{e[0]}' TEXT, "
       c.execute(f"""CREATE TABLE "{tablename}"(
                 'ocel_id' TEXT,
                 'ocel_time' DATETIME,
                 {str} FOREIGN KEY ('ocel_id') REFERENCES 'event'('ocel_id')
                  )""")
       str = ""
       for e in at:
           c.execute(f"""CREATE table {e[0].replace(" ", "")}{n[0].replace(" ","")}table AS SELECT eventID, eventTime, eventAttributeValue as {e[0]} FROM merged.event NATURAL JOIN merged.eventAttribute NATURAL JOIN merged.eventAttributeValue WHERE eventAttributeID = '{e[1]}' AND eventTypeID = '{n[1]}'""")
           str = str + f"{e[0].replace(' ','')}{n[0].replace(' ','')}table natural JOIN "
       str = str[:-13]
       if len(at)>0:
        c.execute(f"""INSERT INTO {tablename} SELECT DISTINCT * FROM {str}""")
       else: 

           c.execute(f"""INSERT INTO {tablename} SELECT DISTINCT eventID, eventTime FROM merged.event where eventTypeID = '{n[1]}'""")
       for e in at:
           c.execute(f"""DROP TABLE {e[0].replace(" ", "")}{n[0].replace(" ","")}table""")
       connect.commit()

def create_new_objectOcelTypes_OCEL(c, connect):
   #What is needed: type, for name
   #attribute name
   #attribute values
   #time 
   #locations
   #eventType
   #attribute
   #attributevalues 
   #event
   #in common: eventType and eventAttribute and event= eventTypeID
   #eventAttributeValuye and event: eventID
   #eventAttribute and eventAttributeValue : eventAttributeID
   #Get the tablenames:
   c.execute("""SELECT objectType, objectTypeID FROM merged.objectType""")
   tablenames = c.fetchall()
   # For each type there are several possibilities: No attributes, one attribute and multiple attributes
   #go through create table:
   for n in tablenames:
       tablename = f"object_{n[0].replace(' ','')}"
       c.execute(f"SELECT objectAttributeName, objectAttributeID FROM merged.objectAttribute where objectTypeID ='{n[1]}'")
       str = ""
       at = c.fetchall()
       for e in at:
           str += f"'{e[0]}' TEXT, "
       c.execute(f"""CREATE TABLE "{tablename}"(
                 'ocel_id' TEXT,
                 'ocel_time' DATETIME,
                 {str} FOREIGN KEY ('ocel_id') REFERENCES 'object'('ocel_id')
                  )""")
       str = ""
       for e in at:
           c.execute(f"""CREATE table {e[0].replace(" ", "")}{n[0].replace(" ","")}table AS SELECT objectID, objectAttributeValTime, AttributeValue as {e[0]} FROM merged.objectAttribute NATURAL JOIN merged.objectAttributeValue WHERE objectAttributeID = '{e[1]}' AND objectTypeID = '{n[1]}'""")
           str = str + f"{e[0].replace(' ','')}{n[0].replace(' ','')}table natural JOIN "
       str = str[:-13]
       if len(at)>0:
        c.execute(f"""INSERT INTO {tablename} SELECT DISTINCT * FROM {str}""")
       else:
            c.execute(f"""INSERT INTO {tablename} SELECT DISTINCT objectID, objectAttributeValTime FROM merged.object NATURAL JOIN merged.objectAttributeValue where objectTypeID = '{n[1]}'""")
       for e in at:
           c.execute(f"""DROP TABLE {e[0].replace(' ', '')}{n[0].replace(' ','')}table""")
       connect.commit()

