import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
)
c = mydb.cursor()
c.execute("drop database if exists testing1")
c.execute("Create database testing1")
c.execute("use testing1")

def create_event_Ocel(c):
    c.execute("CREATE TABLE event_ (eventID varchar(50), eventType Text, eventTime DATETIME, PRIMARY KEY (eventID))")
    c.execute("select table_name from information_schema.tables where table_name in (select concat('event_',ocel_type_map) from ocel.event_map_type)")
    names = c.fetchall()
    print(names)
    for t in names:
        c.execute(f'insert into event_ select ocel_id as eventID, ocel_type as eventType, ocel_time as eventTime from ocel.{t[0]} NATURAL left join ocel.event_ where ocel.event_.ocel_id = ocel.{t[0]}.ocel_id')

def create_objectObject_Ocel(c):
    c.execute('create table objectObject (objectObjectID bigINT not NULL auto_increment ,fromObjectID varchar(50), toObjectID  varchar(50), objectRelationType varchar(50),primary key(objectObjectID))')
    c.execute('insert into objectObject(fromObjectID,toObjectID,objectRelationType) select ocel.object_object.ocel_source as fromObjectID, ocel.object_object.ocel_target as toObjectID, ocel.object_object.ocel_qualifier as objectRelationType from ocel.object_object left join ocel.event_object on ocel.event_object.ocel_object = ocel.object_object.ocel_target or ocel.event_object.ocel_object = ocel.object_object.ocel_source')

def create_eventObject_Ocel(c):
    c.execute('create table eventObject (eventID varchar(50), objectID varchar(50),OEqualifier Text, primary key(eventID,objectID))')
    c.execute('insert into eventObject select ocel.event_object.ocel_event as eventID, ocel.event_object.ocel_object as objectID, ocel.event_object.ocel_qualifier as OEqualifier from ocel.event_object')
create_event_Ocel(c)
create_objectObject_Ocel(c)
create_eventObject_Ocel(c)
c.execute("select * from eventObject")
print(c.fetchall())
