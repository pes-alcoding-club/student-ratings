#adds new student and their handles to the database
from json import load, dump
def add_new_student() :
	default_rating = 1500
	default_volatility = 125
	default_timesPlayed = 0
	default_lastFive = 5

	srn = input("SRN : ").strip()
	name = input("Name : ").strip()
	email = input("Email : ").strip()
	# print("Enter 0 to skip any of the following information")
	hackerearth = input("Hackerearth Username : ").strip()
	# hackerrank = input("Hackerrank Username : ").strip()
	# codechef = input("Codechef Username : ").strip()
	# kickstart = input("Google Kickstart Username : ").strip()
	#codejam = input("Google Codejam Username : ").strip()

	with open("database.json","r") as f:
		database = load(f)
	if srn in database :
		print("Student already exists! Use update database instead")
		return
	new_dict = dict()
	new_dict["name"] = name
	new_dict["email"] = email
	# if len(hackerearth) > 2 :
	# 	new_dict["hackerearth"] = hackerearth
	# if len(hackerrank) > 2 :
	# 	new_dict["hackerrank"] = hackerrank
	# if len(codechef) > 2 :
	# 	new_dict["codechef"] = codechef
	if len(codejam) > 2 : 
		new_dict["codejam"] = codejam
	# if len(kickstart) > 2 :
	# 	new_dict["kickstart"] = kickstart
	
	new_dict["rating"] = default_rating
	new_dict["volatility"] = default_volatility
	new_dict["timesPlayed"] = default_timesPlayed
	new_dict["lastFive"] = default_lastFive
	new_dict["best"] = default_rating

	database[srn] = new_dict

	with open("database.json","w") as f:
		dump(database, f)

def update_student() :
	# default_rating = 1500
	# default_volatility = 125
	# default_timesPlayed = 0
	# default_lastFive = 5
	print("Yet to implement. Manually change json if update is necessary")
	return None

if __name__ == "__main__" :
	print("1. New Student\n2. Update Student\n3. Quit")
	choice = int(input("Choice : "))
	choices = {1: add_new_student, 2 : update_student, 3 : quit}
	choices[choice]()
