import sqlite3
connect = sqlite3.connect("db/OCEL_Simple_Database.db")
c = connect.cursor()
#1) Existence of the type-independent tables
c.execute("""SELECT Count(*) FROM sqlite_master WHERE type = "table" AND tbl_name IN
("event_corr_type", "object_corr_type", "event", "object", "event_object",
"object_object")""")
v = c.fetchall()
if v[0]==6:
    print(True)
else:
    print(v[0][0])
    print(False)
#2) Existence of the object type tables and correspondence with the object
#types in object_corr_type
c.execute("""SELECT Count(*) FROM (SELECT a.ocel_type_corr, b.tbl_name FROM (SELECT
ocel_type_corr FROM object_corr_type) a LEFT OUTER JOIN (SELECT tbl_name
FROM sqlite_master WHERE type = "table" AND tbl_name LIKE "object_%") b
ON b.tbl_name = "object_" || a.ocel_type_corr WHERE b.tbl_name IS NULL)""")
if c.fetchall()[0]==0:
    print(True)
else:
    print(False)
c.execute("""
SELECT Count(*) FROM (SELECT a.ocel_type_corr, b.tbl_name FROM (SELECT
tbl_name FROM sqlite_master WHERE type = "table" AND tbl_name LIKE
"object_%") b LEFT OUTER JOIN (SELECT ocel_type_corr FROM
object_corr_type) a ON b.tbl_name = "object_" || a.ocel_type_corr WHERE
a.ocel_type_corr IS NULL)""")
S#hould be 2 (object_object, object_corr_type)
v = c.fetchall()
if v[0]==2:
    print(True)
else:
    print(False)
    #3) Existence of the event type tables and correspondence with th event
#types in event_corr_type
c.execute("""
SELECT Count(*) FROM (SELECT a.ocel_type_corr, b.tbl_name FROM (SELECT
ocel_type_corr FROM event_corr_type) a LEFT OUTER JOIN (SELECT tbl_name
FROM sqlite_master WHERE type = "table" AND tbl_name LIKE "event_%") b
ON b.tbl_name = "event_" || a.ocel_type_corr WHERE b.tbl_name IS NULL)""")
if c.fetchall()[0]==0:
    print(True)
else:
    print(False)
    c.execute("""
SELECT Count(*) FROM (SELECT a.ocel_type_corr, b.tbl_name FROM (SELECT
tbl_name FROM sqlite_master WHERE type = "table" AND tbl_name LIKE
"event_%") b LEFT OUTER JOIN (SELECT ocel_type_corr FROM
event_corr_type) a ON b.tbl_name = "event_" || a.ocel_type_corr WHERE
a.ocel_type_corr IS NULL)""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#4) Existence of the ocel_type column
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name IN ("object_corr_type",
"event_corr_type", "event", "object") AND m.type = "table" AND p.name =
"ocel_type")""");
if c.fetchall()[0]==4:
    print(True)
else:
    print(False)
#5) Existence of the ocel_type_corr column
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name IN ("object_corr_type",
"event_corr_type") AND m.type = "table" AND p.name = "ocel_type_corr")""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#6) Existence of the ocel_id column
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name IN ("event", "object")
AND m.type = "table" AND p.name = "ocel_id")""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#7) Existence of the ocel_qualifier column
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name IN ("event_object",
"object_object") AND m.type = "table" AND p.name = "ocel_qualifier")""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#8) Existence of the ocel_event-id and ocel_object_id columns
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name = "event_object" AND
m.type = "table" AND p.name IN ("ocel_event_id", "ocel_object_id"))""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#9) Existence of the ocel_source_id and ocel_target_id columns
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.tbl_name = "object_object" AND
m.type = "table" AND p.name IN ("ocel_source_id", "ocel_target_id"))""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#10) Existence of the ocel_id column for all object type specific tables
c.execute("""SELECT m.tbl_name, Count(*) FROM sqlite_master m JOIN object_corr_type ty
on m.tbl_name = "object_" || ty.ocel_type_corr JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND p.name =
"ocel_id" GROUP BY m.tbl_name""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#11) Existence of the ocel_id column for all event type specific tables
c.execute("""SELECT m.tbl_name, Count(*) FROM sqlite_master m JOIN event_corr_type ty
on m.tbl_name = "event_" || ty.ocel_type_corr JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND p.name =
"ocel_id" GROUP BY m.tbl_name""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#12) Existence and type of the ocel_time column for all object type
#specific tables
c.execute("""SELECT m.tbl_name, Count(*) FROM sqlite_master m JOIN object_corr_type ty
on m.tbl_name = "object_" || ty.ocel_type_corr JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND p.name =
"ocel_time" AND p.type = "TIMESTAMP" GROUP BY m.tbl_name""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#13) Existence and type of the ocel_time column for all event type
#specific tables
c.execute("""SELECT m.tbl_name, Count(*) FROM sqlite_master m JOIN event_corr_type ty
on m.tbl_name = "event_" || ty.ocel_type_corr JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND p.name =
"ocel_time" AND p.type = "TIMESTAMP" GROUP BY m.tbl_name""")

#14) Primary key object_corr_type and event_corr_type tables
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND m.tbl_name
IN ("object_corr_type", "event_corr_type") AND p.name = "ocel_type" AND
p.pk > 0)""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#15) Primary key object and event tables
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND m.tbl_name
IN ("object", "event") AND p.name = "ocel_id" AND p.pk > 0)""")
if c.fetchall()[0]==2:
    print(True)
else:
    print(False)
#16) Primary keys event_object table
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND m.tbl_name =
"event_object" AND p.name IN ("ocel_event_id", "ocel_object_id",
"ocel_qualifier") AND p.pk > 0)""");
if c.fetchall()[0]==3:
    print(True)
else:
    print(False)
#17) Primary keys object_object table
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM sqlite_master m JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND m.tbl_name =
"object_object" AND p.name IN ("ocel_source_id", "ocel_target_id",
"ocel_qualifier") AND p.pk > 0)""")
if c.fetchall()[0]==3:
    print(True)
else:
    print(False)
#18) Primary key event type specific table
c.execute("""SELECT m.tbl_name, sum(p.pk) FROM sqlite_master m JOIN event_corr_type
ty on m.tbl_name = "event_" || ty.ocel_type_corr JOIN
pragma_table_info(m.tbl_name) p WHERE m.type = "table" AND p.name =
"ocel_id" GROUP BY m.tbl_name""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#19) Foreign key event table
c.execute("""SELECT Count(*) FROM (SELECT * from pragma_foreign_key_list("event") p
WHERE p."table" = "event_corr_type" AND p."from" = "ocel_type" AND p."to"
= "ocel_type")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#20) Foreign key object table
c.execute("""SELECT Count(*) FROM (SELECT * from pragma_foreign_key_list("object") p
WHERE p."table" = "object_corr_type" AND p."from" = "ocel_type" AND p."to"
= "ocel_type")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#21) Foreign keys event_object table
c.execute("""SELECT Count(*) FROM (SELECT * from
pragma_foreign_key_list("event_object") p WHERE p."table" = "event" AND
p."from" = "ocel_event_id" AND p."to" = "ocel_id")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
c.execute("""SELECT Count(*) FROM (SELECT * from
pragma_foreign_key_list("event_object") p WHERE p."table" = "object" AND
p."from" = "ocel_object_id" AND p."to" = "ocel_id")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#22) Foreign key object_object table
c.execute("""SELECT Count(*) FROM (SELECT * from
pragma_foreign_key_list("object_object") p WHERE p."table" = "object" AND
p."from" = "ocel_source_id" AND p."to" = "ocel_id")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
c.execute("""SELECT Count(*) FROM (SELECT * from
pragma_foreign_key_list("object_object") p WHERE p."table" = "object" AND
p."from" = "ocel_target_id" AND p."to" = "ocel_id")""")
if c.fetchall()[0]==1:
    print(True)
else:
    print(False)
#23) Foreign key event type specific tables
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM (SELECT tbl_name
FROM sqlite_master WHERE type = "table") m JOIN event_corr_type ty on
m.tbl_name = "event_" || ty.ocel_type_corr LEFT OUTER JOIN
pragma_foreign_key_list(m.tbl_name) p ON p."table" = "event" AND p."from"
= "ocel_id" AND p."to" = "ocel_id" WHERE p."table" IS NULL)""")
if c.fetchall()[0]==0:
    print(True)
else:
    print(False)
#24) Foreign key object type specific tables
c.execute("""SELECT Count(*) FROM (SELECT m.tbl_name, p.* FROM (SELECT tbl_name
FROM sqlite_master WHERE type = "table") m JOIN object_corr_type ty on
m.tbl_name = "object_" || ty.ocel_type_corr LEFT OUTER JOIN
pragma_foreign_key_list(m.tbl_name) p ON p."table" = "object" AND p."from"
= "ocel_id" AND p."to" = "ocel_id" WHERE p."table" IS NULL)""")
if c.fetchall()[0]==0:
    print(True)
else:
    print(False)