import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()
c.execute("ATTACH DATABASE 'db/OCED_Simple_Database.db' as 'ocedbase'")

def create_eventType_OCED(c):
    return

def create_event_OCED(c):
    return
       

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
    c.execute("""CREATE TABLE "eventAttribute" (
                    `eventAttributeID` TEXT,
                    `eventTypeID` TEXT,
                    `eventAttributeName` TEXT,
                    PRIMARY KEY (`eventAttributeID`))""")
    c.execute("""SELECT DISTINCT eventAttributeName FROM ocedbase.eventAttributeValue""")
    atrnames =     


def create_eventAttributeValue_OCED(c):
    c.execute("""CREATE TABLE eventAttributeValue (
                    eventID VARCHAR(50),
                    eventAttributeID VARCHAR(50),
                    eventAttributeValue VARCHAR(50),
                    PRIMARY KEY (eventID, eventAttributeValue)) """)  
    c.execute(f"""SELECT DISTINCT eventAttributeName FROM eventAttribute)     
    c.execute(f""" INSERT INTO eventAttributeValue )

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
c.execute("select * from objectObject")
fetchh = c.fetchall()

