import sqlite3
connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()
database = {}
c.execute(f"""SELECT eventType, eventTypeID FROM eventType""")
eventTypes = c.fetchall()
insertede = []
inserteda = []


for e in eventTypes: 
    inside = {"name":e[0]}
    c.execute(f"""SELECT eventattributename FROM eventAttribute WHERE eventTypeID = "{e[1]}" """)
    list = []
    for a in c.fetchall():
        list.append({"name":a[0], "type":"string"})
    inside["attributes"] = list
    insertede.append(inside)
database["eventTypes"]=insertede  

c.execute(f"""SELECT objectType, objectTypeID FROM objectType""")
objectTypes = c.fetchall()
insertedo = []
for o in objectTypes: 
    inside = {"name":o[0]}
    c.execute(f"""SELECT objectAttributeName FROM objectAttribute WHERE objectTypeID = "{o[1]}" """)
    list = []
    for a in c.fetchall():
        list.append({"name":a[0], "type":"string"})
    inside["attributes"] = list
    insertedo.append(inside)
database["objectTypes"]=insertedo



c.execute("""SELECT eventID, eventType, eventTime FROM event NATURAL JOIN eventType """)
events = c.fetchall()
insertedev = []
for e in events: 
  inside = {"id":f"{e[0]}",
            "type": f"{e[1]}",
            "time": f"{e[2]}"}
  c.execute(f"""SELECT eventAttributeName, eventAttributeValue FROM eventAttributeValue NATURAL JOIN eventAttribute WHERE eventID = '{e[0]}' """)
  list = []
  for a in c.fetchall():
      list.append({"name": f"{a[0]}", "value":f"{a[1]}"})
  inside['attributes'] = list
  c.execute(f"""SELECT objectID, EOqualifier FROM eventObject WHERE eventID = "{e[0]}" """)
  rel = []
  for e1 in c.fetchall():
      rel.append({"objectID" : f"{e1[0]}", "qualifier":f"{e1[1]}"})
  inside["relationships"]=rel
  insertedev.append(inside)
database["events"]=insertedev

c.execute("""SELECT objectID, objectType FROM object Natural JOIn objectType""")
objects = c.fetchall()
insertedob = []
for o in objects: 
  inside = {"id":f"{o[0]}",
            "type": f"{o[1]}"}
  c.execute(f"""SELECT objectAttributeName, attributeValue, objectAttributeValTime FROM objectAttributeValue NATURAL JOIN objectAttribute WHERE objectID = '{o[0]}' """)
  list = []
  for a in c.fetchall():
      list.append({"name": f"{a[0]}", "time": f"{a[2]}", "value":f"{a[1]}"})
  inside["attributes"] = list
  c.execute(f"""SELECT toObjectID, objectRelationType FROM objectObject WHERE fromObjectID = "{o[0]}" """)
  rel = []
  for e1 in c.fetchall():
      rel.append({"objectID" : f"{e1[0]}", "qualifier":f"{e1[1]}"})
  inside["relationships"]=rel
  insertedob.append(inside)
  
database["objects"]=insertedob

import json
with  open("ocel.json", "w") as j:
    json.dump(database,j)


