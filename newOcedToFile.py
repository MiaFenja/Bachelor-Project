import sqlite3


connect = sqlite3.connect("newOCED.sqlite")
c = connect.cursor()

c.execute(f"ATTACH DATABASE 'merged.sqlite' as 'merged'")

c.execute("""CREATE TABLE event AS SELECT * FROM merged.event_OCED""")
c.execute("""CREATE TABLE eventAttrbuteValue AS SELECT * FROM merged.eventAttributeValue_OCED""")
c.execute("""CREATE TABLE eventObject AS SELECT * FROM merged.eventObject_OCED""")
c.execute("""CREATE TABLE object AS SELECT * FROM merged.object_OCED""")
c.execute("""CREATE TABLE objectObject AS SELECT * FROM merged.objectObject_OCED""")
c.execute("""CREATE TABLE objectRelationEvent AS SELECT * FROM merged.objectRelationEvent_OCED""")
c.execute("""CREATE TABLE objectAttributeValue AS SELECT * FROM merged.objectAttributeValue_OCED""")
c.execute("""CREATE TABLE objectAttributeValueEvent AS SELECT * FROM merged.objectAttributeValueEvent_OCED""")

connect.commit()
