def createTriggers(c, connect, ocelbase, merged):
    c.execute(f"USE {ocelbase}")
    #event
    c.execute(f"""CREATE TRIGGER eventTrigger AFTER INSERT ON event FOR EACH row
       
                Insert into {merged}.event(eventID) values (new.ocel_id, (SELECT eventTypeID FROM {merged}.eventType where {merged}.eventType.eventType = new.ocel_type))""")