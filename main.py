import sqlite3
import ocelToMerged as o1m
def create_from_ocel(c,base,connect,type):
    str = ""
    if type == 'ocel':
         str='ocelbase' 
    else:
        str = 'ocedbase'
    c.execute(f"ATTACH DATABASE {base} as 'ocelbase'")

    o1m.create_eventType_Ocel(c,connect)
    o1m.create_event_Ocel(c,connect)
    o1m.create_objectObject_Ocel(c,connect)
    o1m.create_eventObject_Ocel(c,connect)
    o1m.create_objectType(c,connect)
    o1m.create_object(c,connect)
    o1m.create_objectRelationEvent(c,connect)
    o1m.create_objectAttribute(c,connect)
    o1m.create_objectAttributeValue(c,connect)
    o1m.create_objectAttributeValueEvent(c,connect)
    o1m.create_eventAttribute(c,connect)
    o1m.create_eventAttributeValue(c,connect)
def main():
    connect = sqlite3.connect("merged.sqlite")
    c = connect.cursor()
    create_from_ocel(c,"'db/OCEL_Simple_Database.db'",connect,'ocel')
main()
