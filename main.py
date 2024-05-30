import sqlite3
import ocelToMerged as o1m
import ocedToMerged as o2m
def create_from_ocel(c,base,connect,type):
    str = ""
    if type == 'ocel':
         str='ocelbase' 
    else:
        str = 'ocedbase'
    c.execute(f"ATTACH DATABASE {base} as '{str}'")
    if type == 'ocel':
        o1m.create_eventType_Ocel(c,connect)
        o1m.create_event_Ocel(c,connect)
        o1m.create_objectObject_Ocel(c,connect)
        o1m.create_eventObject_Ocel(c,connect)
        o1m.create_objectType_Ocel(c,connect)
        o1m.create_object_Ocel(c,connect)
        o1m.create_objectRelationEvent_Ocel(c,connect)
        o1m.create_objectAttribute_Ocel(c,connect)
        o1m.create_objectAttributeValue_Ocel(c,connect)
        o1m.create_objectAttributeValueEvent_Ocel(c,connect)
        o1m.create_eventAttribute_Ocel(c,connect)
        o1m.create_eventAttributeValue_Ocel(c,connect)
    else:
        o2m.create_eventType_OCED(c,connect)
        o2m.create_event_OCED(c,connect)
        o2m.create_objectObject_OCED(c,connect)
        o2m.create_eventObject_OCED(c,connect)
        o2m.create_objectType_OCED(c,connect)
        o2m.create_object_OCED(c,connect)
        o2m.create_objectRelationEvent_OCED(c,connect)
        o2m.create_objectAttribute_OCED(c,connect)
        o2m.create_objectAttributeValue_OCED(c,connect)
        o2m.create_objectAttributeValueEvent_OCED(c,connect)
        o2m.create_eventAttribute_OCED(c,connect)
        o2m.create_eventAttributeValue_OCED(c,connect)
def main():
    connect = sqlite3.connect("merged.sqlite")
    c = connect.cursor()
<<<<<<< Updated upstream
    create_from_ocel(c,"'db/OCED_Simple_Database.db'",connect,'oced')
=======
    create_from_ocel(c,"'db/OCEL_Simple_Database.db'",connect,'ocel')
>>>>>>> Stashed changes
main()
