import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()
c.execute("ATTACH DATABASE 'db/OCED_Simple_Database.db' as 'ocedbase'")

def create_eventType_OCED(c):
    c.execute("""CREATE TABLE "eventType" (
                `eventTypeID` TEXT PRIMARY KEY,
                `eventType` TEXT
                )""")
    
    c.execute(f"""INSERT INTO eventType(eventType)
              SELECT DISTINCT eventType FROM ocedbase.event""")
    c.execute(f"SELECT rowid from eventType")
    rowids = c.fetchall()
    for i in rowids:
        c.execute(f"""UPDATE eventType 
                  SET eventTypeID = "ET-{i[0]}" 
                  WHERE rowid  = {i[0]}""")
    connect.commit()

def create_event_OCED(c):
    c.execute("""CREATE TABLE "event" (
                    `eventID` TEXT PRIMARY KEY, 
                    `eventTypeID` TEXT, 
                    `eventTime` TIMESTAMP)""")
    
    c.execute("""INSERT INTO event SELECT eventID, eventTypeID, timestamp AS eventTime FROM ocedbase.event NATURAL JOIN eventType""")
    connect.commit()

def create_objectObject_OCED(c):
    return

def create_eventObject_OCED(c):
    return
    
def create_objectType_OCED(c):
    return

def create_object_OCED(c):
    return

def create_objectRelationEvent_OCED(c):
    return

def create_objectAttribute_OCED(c):
    return
            

def create_objectAttributeValue_OCED(c):
    return

def create_objectAttributeValueEvent_OCED(c):
    return
 
            
def create_eventAttribute_OCED(c):
    return


def create_eventAttributeValue_OCED(c):
   return

 
create_eventType_OCED(c)
create_event_OCED(c)
create_objectObject_OCED(c)
create_eventObject_OCED(c)
create_objectType_OCED(c)
create_object_OCED(c)
create_objectRelationEvent_OCED(c)
create_objectAttribute_OCED(c)
create_objectAttributeValue_OCED(c)
create_objectAttributeValueEvent_OCED(c)
create_eventAttribute_OCED(c)
create_eventAttributeValue_OCED(c)
c.execute("select * from event")
fetchh = c.fetchall()

