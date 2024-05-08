import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()

def drop_views(c):
    c.execute("""SELECT name FROM sqlite_master WHERE type = 'view' AND name LIKE '%OCED'""")
    views = c.fetchall()
    for i in views:
        c.execute(f"""DROP VIEW IF EXISTS {i[0]}""")
    connect.commit()

def create_view_event(c):
    connect.commit()

def create_view_eventAttributeValue(c):
    connect.commit()

def create_view_eventAttributeName(c):
    connect.commit()

def create_view_eventObject(c):
    connect.commit()

def create_view_object(c):
    connect.commit()

def create_view_objectObject(c):
    connect.commit()

def create_view_objectRelationEvent(c):
    connect.commit()

def create_view_objectAttributeValue(c):
    connect.commit()

def create_view_objectAttributeValueEvent(c):
    connect.commit()

def create_view_event(c):
    connect.commit()

def create_view_eventAttributeValue(c):
    connect.commit()

def create_view_eventAttributeName(c):
    connect.commit()

drop_views(c)
create_view_eventObject(c)
create_view_object(c)
create_view_objectObject(c)
create_view_objectRelationEvent(c)
create_view_objectAttributeValue(c)
create_view_objectAttributeValueEvent(c)

c.execute("select * from event_OCED")
print(c.fetchall())