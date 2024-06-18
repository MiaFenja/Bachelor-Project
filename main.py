import sqlite3
import sys
sys.path.append("sqlite/")
import ocelToMergedsqlite as o1m
import ocedToMergedsqlite as o2m
import mergedToOCEDsqlite as m2o
import mergedToOCELsqlite as m1o
import time
import Jsonoutput as jsono
import mysql.connector
sys.path.append("mysql/")
import mergedToOCEDmysql as m2om
import mergedToOCELmysql as m1om
import ocedToMergedmysql as o2mm
import ocelToMergedmysql as o1mm


def create_merged_sqlite(c,base,connect,type):
    str = ""
    if type == 'OCEL':
        str="ocelbase" 
    else:
        str = "ocedbase"
    c.execute(f"ATTACH DATABASE {base} as '{str}'")
    if type == 'OCEL':
        o1m.create_eventType_OCEL(c,connect)
        o1m.create_event_OCEL(c,connect)
        o1m.create_objectObject_OCEL(c,connect)
        o1m.create_eventObject_OCEL(c,connect)
        o1m.create_objectType_OCEL(c,connect)
        o1m.create_object_OCEL(c,connect)
        o1m.create_objectRelationEvent_OCEL(c,connect)
        o1m.create_objectAttribute_OCEL(c,connect)
        o1m.create_objectAttributeValue_OCEL(c,connect)
        o1m.create_objectAttributeValueEvent_OCEL(c,connect)
        o1m.create_eventAttribute_OCEL(c,connect)
        o1m.create_eventAttributeValue_OCEL(c,connect)
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
 
def create_merged_mysql(c,base,connect,type):
    if type == 'OCEL':
        o1mm.create_eventType_OCEL(c,connect,base)
        o1mm.create_event_OCEL(c,connect,base)
        o1mm.create_objectObject_OCEL(c,connect,base)
        o1mm.create_eventObject_OCEL(c,connect,base)
        o1mm.create_objectType_OCEL(c,connect,base)
        o1mm.create_object_OCEL(c,connect,base)
        o1mm.create_objectRelationEvent_OCEL(c,connect,base)
        o1mm.create_objectAttribute_OCEL(c,connect,base)
        o1mm.create_objectAttributeValue_OCEL(c,connect,base)
        o1mm.create_objectAttributeValueEvent_OCEL(c,connect,base)
        o1mm.create_eventAttribute_OCEL(c,connect,base)
        o1mm.create_eventAttributeValue_OCEL(c,connect,base)
    else:
        o2mm.create_eventType_OCED(c,connect,base)
        o2mm.create_event_OCED(c,connect,base)
        o2mm.create_objectObject_OCED(c,connect,base)
        o2mm.create_eventObject_OCED(c,connect,base)
        o2mm.create_objectType_OCED(c,connect,base)
        o2mm.create_object_OCED(c,connect,base)
        o2mm.create_objectRelationEvent_OCED(c,connect,base)
        o2mm.create_objectAttribute_OCED(c,connect,base)
        o2mm.create_objectAttributeValue_OCED(c,connect,base)
        o2mm.create_objectAttributeValueEvent_OCED(c,connect,base)
        o2mm.create_eventAttribute_OCED(c,connect,base)
        o2mm.create_eventAttributeValue_OCED(c,connect,base)   

def create_output_sqlite(c, merged, connect, type):
    c.execute(f"ATTACH DATABASE 'output/merged.sqlite' as 'merged'")

    if type == 'OCED':
        m2o.create_new_event_OCED(c, connect) 
        m2o.create_new_eventAttributeValue_OCED(c, connect)
        m2o.create_new_eventObject_OCED(c, connect)
        m2o.create_new_object_OCED(c, connect)
        m2o.create_new_objectObject_OCED(c, connect)
        m2o.create_new_objectRelationEvent_OCED(c, connect)
        m2o.create_new_objectAttributeValue_OCED(c, connect)
        m2o.create_new_objectAttributeValueEvent_OCED(c, connect)
    elif type == "jsonocel":
        connect = sqlite3.connect("output/merged.sqlite")
        c = connect.cursor()
        jsono.createJson(c,connect)
    else:
        m1o.create_new_eventMapType_OCEL(c, connect)
        m1o.create_new_objectMapType_OCEL(c, connect)
        m1o.create_new_event_OCEL(c, connect)
        m1o.create_new_object_OCEL(c, connect)
        m1o.create_new_objectObject_OCEL(c, connect)
        m1o.create_new_eventObject_OCEL(c, connect)
        m1o.create_new_eventOcelTypes_OCEL(c, connect)
        m1o.create_new_objectOcelTypes_OCEL(c, connect)

         
def create_output_mysql(c,merged,connect,type):
    if type == 'OCED':
        m2om.create_view_event_OCED(c, connect) 
        m2om.create_view_eventAttributeValue_OCED(c, connect)
        m2om.create_view_eventObject_OCED(c, connect)
        m2om.create_view_object_OCED(c, connect)
        m2om.create_view_objectObject_OCED(c, connect)
        m2om.create_view_objectRelationEvent_OCED(c, connect)
        m2om.create_view_objectAttributeValue_OCED(c, connect)
        m2om.create_view_objectAttributeValueEvent_OCED(c, connect)
    elif type == 'jsonocel':
        jsono.createJson(c,connect)
    else:
        m1om.create_view_eventMapType_OCEL(c, connect)
        m1om.create_view_objectMapType_OCEL(c, connect)
        m1om.create_view_event_OCEL(c, connect)
        m1om.create_view_object_OCEL(c, connect)
        m1om.create_view_objectObject_OCEL(c, connect)
        m1om.create_view_eventObject_OCEL(c, connect)
        m1om.create_view_eventOcelTypes_OCEL(c, connect)
        m1om.create_view_objectOcelTypes_OCEL(c, connect)


def main(sql, filepath, input_format, output_format):
    if sql == 'SQLite':
        connect = sqlite3.connect("output/merged.sqlite")
        c = connect.cursor()
        if input_format != "merged":
            start_time = time.time()
            create_merged_sqlite(c,f"'{filepath}'",connect,input_format)
            print("Task completed in %s seconds" % (time.time() - start_time))


        connect = sqlite3.connect(f"output/newDB.sqlite")
        c = connect.cursor()

        start_time = time.time()
        create_output_sqlite(c,'output/merged.sqlite',connect,output_format)
        print("Task completed in %s seconds" % (time.time() - start_time))
    else:
        input1 = input("Insert host:")
        input2 = input("Insert user:")
        input3 = input("Insert password:")
        connect = mysql.connector.connect(
            host = input1,
            user = input2,
            password = input3
        )
        c = connect.cursor()
        c.execute("USE merged")
        if input_format != "merged":
            c.execute("DROP DATABASE IF EXISTS merged")
            c.execute("CREATE DATABASE merged")
           
            
            start_time = time.time()
            create_merged_mysql(c,filepath,connect,input_format)
            print("Task completed in %s seconds" % (time.time() - start_time))

        start_time = time.time()
        create_output_mysql(c,'output/merged.sqlite',connect,output_format)
        print("Task completed in %s seconds" % (time.time() - start_time))
    
terminput = sys.argv
main(f"{terminput[1]}", f"{terminput[2]}", f"{terminput[3]}", f"{terminput[4]}")


