import csv
import io
from json import load

if __name__ == "__main__" :
	with open("database.json","r") as f:
		database = load(f)
	table = [["SRN", "Name", "Rating", "Best"]]
	for student in database :
		row = [rank]
		row.append(student)
		row.append(database[student]["name"])
		row.append(database[student]["rating"])
		row.append(database[student]["best"])
		table.append(row[:])
	table.sort(key = lambda x : x[2], reverse = True)

	with io.open("output.csv",'w', encoding = "utf-8", newline = "") as resultFile:
		wr = csv.writer(resultFile, dialect='excel')
		wr.writerows(table)
	#output of this can be directly put into google sheets
