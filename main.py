import sqlite3
import ocelToMerged as o1m
import ocedToMerged as o2m
import mergedToOced as m2o
import mergedToOcel as m1o
import time
import sys

def create_merged(c,base,connect,type):
    str = ""
    if type == 'OCEL':
         str="ocelbase" 
    else:
        str = "ocedbase"
    c.execute(f"ATTACH DATABASE {base} as '{str}'")
    if type == 'OCEL':
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

def create_output(c, merged, connect, type):
    c.execute(f"ATTACH DATABASE 'merged.sqlite' as 'merged'")

    if type == 'OCED':
        m2o.create_new_event_OCED(c, connect) 
        m2o.create_new_eventAttributeValue_OCED(c, connect)
        m2o.create_new_eventObject_OCED(c, connect)
        m2o.create_new_object_OCED(c, connect)
        m2o.create_new_objectObject_OCED(c, connect)
        m2o.create_new_objectRelationEvent_OCED(c, connect)
        m2o.create_new_objectAttributeValue_OCED(c, connect)
        m2o.create_new_objectAttributeValueEvent_OCED(c, connect)
    else:
        m1o.create_new_eventMapType_OCEL(c, connect)
        m1o.create_new_objectMapType_OCEL(c, connect)
        m1o.create_new_event_OCEL(c, connect)
        m1o.create_new_object_OCEL(c, connect)
        m1o.create_new_object_object_OCEL(c, connect)
        m1o.create_new_eventObject_OCEL(c, connect)
        m1o.create_new_eventOcelTypes_OCEL(c, connect)
        m1o.create_new_objectOcelTypes_OCEL(c, connect)

def main(sql, filepath, input_format, output_format):
    if sql == 'SQLite':
        connect = sqlite3.connect("merged.sqlite")
        c = connect.cursor()
        
        start_time = time.time()
        create_merged(c,f"'{filepath}'",connect,input_format)
        print("Task completed in %s seconds" % (time.time() - start_time))


        connect = sqlite3.connect("newDB.sqlite")
        c = connect.cursor()

        start_time = time.time()
        create_output(c,'merged.sqlite',connect,output_format)
        print("Task completed in %s seconds" % (time.time() - start_time))

input = sys.argv
main(f"{input[1]}", f"{input[2]}", f"{input[3]}", f"{input[4]}")


# python main.py 'SQLite' 'db/OCEL_big_data.db' 'OCEL' 'OCED'
# python main.py 'SQLite' 'db/OCEL_Simple_Database.db' 'OCEL' 'OCEL'