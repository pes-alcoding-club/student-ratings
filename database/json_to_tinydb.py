from tinydb import TinyDB
from database.db_tools import read_database

database_dict = read_database(filename="database.json")
new_db = TinyDB("db.json")

for usn in database_dict:
    database_dict[usn]["usn"] = usn

res = new_db.insert_multiple(database_dict.values())
print(res)
