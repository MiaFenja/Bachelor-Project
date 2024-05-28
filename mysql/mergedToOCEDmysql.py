import mysql.connector
connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
c = connect.cursor()
c.execute("USE testing1")


def create_view_event_OCED(c):
    c.execute("""CREATE VIEW event_OCED AS SELECT event.eventID, eventType.eventType, event.eventTime FROM event NATURAL JOIN eventType""")
    connect.commit()

def create_view_eventAttributeValue_OCED(c):
    c.execute(f"""CREATE VIEW eventAttributeValue_OCED AS SELECT eventID,eventAttributeName,eventAttributeValue FROM eventAttributeValue NATURAL JOIN eventAttribute """)
    connect.commit()

def create_view_eventObject_OCED(c):
    c.execute("""CREATE VIEW eventObject_OCED AS SELECT * FROM eventObject""")
    connect.commit()

def create_view_object_OCED(c):
    c.execute("""CREATE VIEW object_OCED AS SELECT object.objectID, objectType.objectType FROM object NATURAL JOIN objectType""")
    connect.commit()

def create_view_objectObject_OCED(c):
    c.execute("""CREATE VIEW objectObject_OCED AS SELECT * FROM objectObject""")
    connect.commit()

def create_view_objectRelationEvent_OCED(c):
    c.execute("""CREATE VIEW objectRelationEvent_OCED AS SELECT objectRelationEvent.objectObjectID, objectRelationEvent.eventID, 
                 objectRelationEvent.OOEqualifier FROM objectRelationEvent""")
    connect.commit()

def create_view_objectAttributeValue_OCED(c):
    c.execute(f"""CREATE VIEW objectAttributeValue_OCED AS SELECT objectID,objectAttributeName,AttributeValue FROM objectAttributeValue NATURAL JOIN objectAttribute """)
    connect.commit()

def create_view_objectAttributeValueEvent_OCED(c):
    c.execute("""CREATE VIEW objectAttributeValueEvent_OCED AS SELECT eventID, valueID AS objectAttributeValueID, OAEqualifier FROM objectAttributeValueEvent""")
    connect.commit()


create_view_event_OCED(c) 
create_view_eventAttributeValue_OCED(c)
create_view_eventObject_OCED(c)
create_view_object_OCED(c)
create_view_objectObject_OCED(c)
create_view_objectRelationEvent_OCED(c)
create_view_objectAttributeValue_OCED(c)
create_view_objectAttributeValueEvent_OCED(c)

c.execute("select * from objectAttributeValue_OCED")
print(c.fetchall())