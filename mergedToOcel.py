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

def create_new_object_object_OCEL(c, connect):
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
    c.execute("SELECT eventTypeID, eventType FROM merged.eventType")
    eventTypes = c.fetchall()
    for e in eventTypes:
        c.execute(f"SELECT eventAttributeName from merged.eventAttribute WHERE eventTypeID = '{e[0]}'")
        allAttribute = c.fetchall()
        if len(allAttribute)==0:
            c.execute(f"""CREATE TABLE "event_{e[1].replace(" ","")}" (
                        'ocel_id' TEXT,
                        'ocel_time' TIMESTAMP,
                        FOREIGN KEY ('ocel_id') REFERENCES 'event'('ocel_id'))""")
            c.execute(f"""INSERT INTO event_{e[1].replace(" ","")} SELECT eventID as ocel_id, eventTime as ocel_time FROM merged.event where eventTypeID = '{e[0]}'""")
            
        else:
            list = []
            stra = ""
            for a in allAttribute:
                stra = stra + f"""'{a[0]}'"""+" TEXT, "
                list.append(f"""event_{a[0]}_{e[1].replace(" ","")}_temp""")

            
                c.execute(f"""CREATE TABLE event_{a[0]}_{e[1].replace(" ","")}_temp AS SELECT eventID as ocel_id, eventTime as ocel_time, eventAttributeValue AS '{a[0]}' 
                              FROM merged.event NATURAL JOIN merged.eventAttributeValue Natural JOiN merged.eventAttribute WHERE eventAttributeName = '{a[0]}'  """)
            
            str = ""
            for l in list:
                str += f"{l} NATURAL JOIN "

            
            str = str[:-13]
            if len(list)>1:

                c.execute(f"""CREATE TABLE "event_{e[1].replace(" ","")}" (
                        'ocel_id' TEXT,
                        'ocel_time' TIMESTAMP,
                        {stra} FOREIGN KEY ('ocel_id') REFERENCES 'event'('ocel_id'))""")
                c.execute(f"""INSERT INTO event_{e[1].replace(" ","")} SELECT * FROM {str}""")
                for a in allAttribute:
                    c.execute(f"""DROP TABLE event_{a[0]}_{e[1].replace(" ","")}_temp""")
            else:
            
                c.execute(f"""CREATE TABLE "event_{e[1].replace(" ","")}" (
                        ocel_id text,
                        ocel_time TIMESTAMP,
                        {stra} FOREIGN KEY (ocel_id) REFERENCES 'event'('ocel_id'))""")
                c.execute(f"""INSERT INTO event_{e[1].replace(" ","")} SELECT * FROM event_{allAttribute[0][0]}_{e[1].replace(" ","")}_temp""")
                c.execute(f"""DROP TABLE event_{allAttribute[0][0]}_{e[1].replace(" ","")}_temp""")
    connect.commit()

def create_new_objectOcelTypes_OCEL(c, connect):
    c.execute("SELECT objectTypeID, objectType FROM merged.objectType")
    objectTypes = c.fetchall()
    for e in objectTypes:
        c.execute(f"SELECT objectAttributeName from merged.objectAttribute WHERE objectTypeID = '{e[0]}'")
        allAttribute = c.fetchall()
        if len(allAttribute)==0:
            c.execute(f"""CREATE TABLE "object_{e[1].replace(" ","")}" (
                        'ocel_id' TEXT,
                        'ocel_time' TIMESTAMP,
                        FOREIGN KEY ('ocel_id') REFERENCES 'object'('ocel_id'))""")
            c.execute(f"""INSERT into object_{e[1].replace(" ","")} SELECT objectID as ocel_id,  objectAttributeValTime as ocel_time FROM merged.object NATURAL JOIN merged.objectAttributeValue where objectTypeID = '{e[0]}'""")
        
        else:
            list = []
            stra = ""
            for a in allAttribute:
                stra = stra + f"""`{a[0]}`"""+" TEXT, "
                
                tablename = f"""object_{a[0]}_{e[1].replace(" ","")}_temp"""
                list.append(tablename)
                c.execute(f"""CREATE TABLE {tablename} AS SELECT objectID as ocel_id, objectAttributeValTime as ocel_time, 
                              attributeValue AS {a[0]} FROM merged.objectAttributeValue Natural JOIN merged.objectAttribute WHERE objectAttributeName = '{a[0]}'""")
            
            str = ""
            for l in list:
                str += f"{l} NATURAL JOIN "
            
            str = str[:-13]
            if len(list)>1:
                c.execute(f"""CREATE TABLE "object_{e[1].replace(" ","")}" (
                        'ocel_id' TEXT,
                        'ocel_time' TIMESTAMP,
                        {stra}
                        FOREIGN KEY ('ocel_id') REFERENCES 'object'('ocel_id'))""")
                c.execute(f"""INSERT INTO object_{e[1].replace(" ","")} SELECT * FROM {str}""")
                for a in allAttribute:
                    c.execute(f"""DROP TABLE object_{a[0]}_{e[1].replace(" ","")}_temp""")
            else:
                c.execute(f"""CREATE TABLE "object_{e[1].replace(" ","")}" (
                        'ocel_id' TEXT,
                        'ocel_time' TIMESTAMP,
                        '{allAttribute[0][0]}',
                        FOREIGN KEY ('ocel_id') REFERENCES 'object'('ocel_id'))""")
                c.execute(f"""INSERT INTO object_{e[1].replace(" ","")} SELECT * FROM object_{allAttribute[0][0]}_{e[1].replace(" ","")}_temp""")
                c.execute(f"""DROP TABLE object_{allAttribute[0][0]}_{e[1].replace(" ","")}_temp""")
    connect.commit()


