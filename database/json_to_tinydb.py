import json
from tinydb import TinyDB


with open("database.json") as fp:
    database_dict = json.load(fp)


new_db = TinyDB("db.json")

for usn in database_dict:
    database_dict[usn]["usn"] = usn

res = new_db.insert_multiple(database_dict.values())
print(res)
