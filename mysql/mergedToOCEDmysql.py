

def create_view_event_OCED(c,connect):
    c.execute("""CREATE VIEW event_OCED AS SELECT event.eventID, eventType.eventType, event.eventTime FROM event NATURAL JOIN eventType""")
    connect.commit()

def create_view_eventAttributeValue_OCED(c,connect):
    c.execute(f"""CREATE VIEW eventAttributeValue_OCED AS SELECT eventID,eventAttributeName,eventAttributeValue FROM eventAttributeValue NATURAL JOIN eventAttribute """)
    connect.commit()

def create_view_eventObject_OCED(c,connect):
    c.execute("""CREATE VIEW eventObject_OCED AS SELECT * FROM eventObject""")
    connect.commit()

def create_view_object_OCED(c,connect):
    c.execute("""CREATE VIEW object_OCED AS SELECT object.objectID, objectType.objectType FROM object NATURAL JOIN objectType""")
    connect.commit()

def create_view_objectObject_OCED(c,connect):
    c.execute("""CREATE VIEW objectObject_OCED AS SELECT * FROM objectObject""")
    connect.commit()

def create_view_objectRelationEvent_OCED(c,connect):
    c.execute("""CREATE VIEW objectRelationEvent_OCED AS SELECT objectRelationEvent.objectObjectID, objectRelationEvent.eventID, 
                 objectRelationEvent.OOEqualifier FROM objectRelationEvent""")
    connect.commit()

def create_view_objectAttributeValue_OCED(c,connect):
    c.execute(f"""CREATE VIEW objectAttributeValue_OCED AS SELECT instanceID, objectID,objectAttributeName,AttributeValue FROM objectAttributeValue NATURAL JOIN objectAttribute """)
    connect.commit()

def create_view_objectAttributeValueEvent_OCED(c,connect):
    c.execute("""CREATE VIEW objectAttributeValueEvent_OCED AS SELECT eventID, valueID AS objectAttributeValueID, OAEqualifier FROM objectAttributeValueEvent""")
    connect.commit()
