file = open("db/newBigOCEL_dump.sql","r")
import re
li = ""

dump2 = open("db/newBigOCEL_mySQL.sql", "a")
for l in file.readlines():
    l2 = l.replace("\"", "").replace("TEXT","VARCHAR(50)").replace("`", "").replace("PRAGMA foreign_keys=OFF;", "SET FOREIGN_KEY_CHECKS=0;").replace("BEGIN TRANSACTION;","").replace("TIMESTAMP", "DATETIME")
    l2 = re.sub(r'(?<=\d)[T]', " ",l2)
    l2 = re.sub(r'\.\d\d\d[Z]', "",l2)
    dump2.write(l2)

