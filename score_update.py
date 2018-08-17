#REF : https://www.codechef.com/ratings

#R = rating, V = volatility

#{R, V, timesPlayed}
#Each player in his first contest would have an initial rating of 1500 and initial volatility of 125.

from math import sqrt, log
from json import load, dump
from copy import deepcopy
from sys import stdin

Eab = lambda Ra, Va, Rb, Vb : 1/(1 + pow(4, ((Ra-Rb)/(sqrt(pow(Va,2) + pow(Vb, 2))))))
#ERank = lambda Ra, Va, Rb_Vb_list : sum([Eab(Ra, Va, Rb, Vb) for Rb, Vb in Rb_Vb_list])
ERank = lambda Ra, Va, Rb_Vb_list : sum([Eab(Ra, Va, X[0], X[1]) for X in Rb_Vb_list])
#Perf = lambda rank, N :  log(N/(rank-1)) / log(4) causes division by zero
Perf = lambda rank, N :  log(N/(max(0.01,rank-0.99))) / log(4)
EPerf = lambda ERank, N : Perf(ERank, N)
APerf = lambda ARank, N : Perf(ARank, N)

def Cf(R_list, V_list, N) : #Competition Factor
	assert len(R_list) == len(V_list) == N
	Ravg = sum(R_list) / len(R_list)
	term1 = sum(map(lambda x : x*x, V_list)) / N
	term2 = sum(map(lambda x : (x-Ravg)**2, R_list)) / (N-1)
	return sqrt(term1 + term2)

RWa = lambda timesPlayed : (0.4*timesPlayed + 0.2) / (0.7*timesPlayed + 0.6)
VWa = lambda timesPlayed : (0.5*timesPlayed + 0.8) / (timesPlayed + 0.6)

NRa = lambda Ra, APerf, EPerf, Cf, RWa : Ra + (APerf - EPerf)*Cf*RWa
NVa = lambda VWa, NRa, Ra, Va : sqrt((VWa*((NRa - Ra)**2) + (Va**2)) / (VWa + 1.1))

Rcap = lambda Ra, timesPlayed : 100 + (75/(timesPlayed + 1)) + ((100*500)/(abs(Ra-1500) + 500))
Vcap = lambda Va : max(75, min(Va, 200)) #(75, 200) #the volatility can change maximum by these two

def read_contest_ranklist() :
	#first line contains site name, rest is rank list
	site = input().strip() #e.g. hackerrank
	scores = {}
	rank = 1
	while True :
		try :
			handle = input().strip()
			scores[handle] = rank #rank, handle
			rank += 1
		except EOFError :
			break
	return site, scores

def update_database(database, site, scores) :
	N = len(scores) #no. of participants
	#participants = set([x[1] for x in scores])
	#assert N == len(participants)
	R_list, V_list, S_list = [], [], []
	new_database = deepcopy(database)
	for student in database : #student = SRN
		if site in database[student] and database[student][site] in scores :
			R_list.append(database[student]["rating"])
			V_list.append(database[student]["volatility"])
			S_list.append(student)
		else :
			new_database[student]["lastFive"] = max(database[student]["lastFive"]-1, 0)
			if new_database[student]["lastFive"] == 0 :
				new_database[student]["rating"] = 0.9 * database[student]["rating"]
				new_database[student]["volatility"] = 125
				new_database[student]["lastFive"] = 5
	if N > len(R_list) :
		print("Some students are not in the database yet but have taken part")
		print("Add them to the database to have their scores updated")
		N = len(R_list)
	Rb_Vb_list = list(zip(R_list, V_list))
	var_Cf = Cf(R_list, V_list, N)
	for student in S_list :
		Ra = database[student]["rating"]
		Va = database[student]["volatility"]
		actual_rank = scores[database[student][site]]
		timesPlayed = database[student]["timesPlayed"]
		new_rating = NRa(Ra,
						APerf(actual_rank, N),
						EPerf(ERank(Ra, Va, Rb_Vb_list),N),
						var_Cf,
						RWa(timesPlayed)
						)
		new_volatility = NVa(VWa(timesPlayed), new_rating, Ra,	Va)
		if new_rating > Ra : #a cap to how much the rating can change
			new_rating = min(new_rating, Ra + Rcap(Ra, timesPlayed))
		else :
			new_rating = max(new_rating, Ra - Rcap(Ra, timesPlayed))
		new_volatility = Vcap(new_volatility) # a cap to how much volatility can change

		new_database[student]["rating"] = new_rating
		new_database[student]["best"] = max(database[student]["best"], new_rating)
		new_database[student]["volatility"] = new_volatility
		new_database[student]["timesPlayed"] += 1
		new_database[student]["lastFive"] = 5 #now student can choose to not participate in next 5 contests
	return new_database

if __name__ == "__main__" :
	with open("database.json","r") as f:
		database = load(f)
	#database is a dictionary of dictionaries whose keys are SRN
	site, scores = read_contest_ranklist() #reads from stdin till EOF
	if len(scores) <= 1 :
		quit()
	new_database = update_database(database, site, scores)

	with open("database.json","w") as f:
		dump(new_database, f)