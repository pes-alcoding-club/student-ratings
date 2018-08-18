from selenium import webdriver
from time import sleep
import csv
import io


sleep_time = 2

# Alter these before every round
scoreboard_url = "https://codejam.withgoogle.com/2018/challenges/0000000000007706/scoreboard"
items_in_a_row = 21
useless_elements_start = 13
useless_elements_end = 5


driver = webdriver.Chrome()
driver.get(scoreboard_url)
input("Sign in to your google account from your browser and enter any key : ")
sleep(sleep_time)
driver.refresh()
print("Please wait")
sleep(sleep_time)
driver.refresh()
sleep(sleep_time)
temp = ""

page_no = 0
rank_start = 1
rank_end = 30
results = []

def f(rank_start = 1) :
	sleep(sleep_time)
	table  = driver.find_elements_by_xpath("//table[@class='scoreboard']//tr")
	for rows in table :
		#print(type(rows))
		row = rows.find_elements_by_xpath('//td')
		raw_items = [a.text for a in row]
		break
	
	while raw_items :
		results.append(raw_items[:items_in_a_row])
		raw_items = raw_items[items_in_a_row:]
	#for row in results[:-1] :
	#	print (row)
try :
	for i in range(10**5) :
		try :
			item = driver.find_elements_by_xpath('//li')[useless_elements_start-1:-useless_elements_end][i]
			#print(type(item),item, item.text)
			item.click()
			sleep(sleep_time)
			# i += 1
			f(rank_start)
			rank_start += 30
		except IndexError :
			break
except UnboundLocalError :
	pass



driver.close()
print(len(results))

clean_results = []
for item in results :
	if item[0].isdigit() :
		clean_results.append(tuple(item))
clean_set = set(clean_results)
clean_results = list(clean_set)
clean_results.sort(key = lambda x : int(x[0]))

with io.open("output.csv",'w', encoding = "utf-8", newline = "") as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(clean_results)