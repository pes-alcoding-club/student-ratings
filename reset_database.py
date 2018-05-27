from json import load, dump
with open("database.json", "r") as f :
	database = load(f)
	for ide in database :
		database[ide]["rating"] = 1500
		database[ide]["volatility"] = 125
		database[ide]["best"] = 1500
		database[ide]["timesPlayed"] = 0
		database[ide]["lastFive"] = 5
with open("database.json", "w") as f :
	dump(database, f)

