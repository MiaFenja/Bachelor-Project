import sqlite3

connect = sqlite3.connect("merged.sqlite")
c = connect.cursor()
c.execute("ATTACH DATABASE 'db/OCED_Simple_Database.db' as 'ocedbase'")

def create_eventType_Ocel(c):


def create_event_Ocel(c):


       

def create_objectObject_Ocel(c):


def create_eventObject_Ocel(c):

    
def create_objectType(c):


def create_object(c):

    
def create_objectRelationEvent(c):

def create_objectAttribute(c):

            

def create_objectAttributeValue(c):


def create_objectAttributeValueEvent(c):

 
            
def create_eventAttribute(c):



def create_eventAttributeValue(c):
   

 
create_eventType_Ocel(c)
create_event_Ocel(c)
create_objectObject_Ocel(c)
create_eventObject_Ocel(c)
create_objectType(c)
create_object(c)
create_objectRelationEvent(c)
create_objectAttribute(c)
create_objectAttributeValue(c)
create_objectAttributeValueEvent(c)
create_eventAttribute(c)
create_eventAttributeValue(c)
c.execute("select * from objectObject")
fetchh = c.fetchall()

