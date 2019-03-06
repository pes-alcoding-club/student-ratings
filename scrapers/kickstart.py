from selenium import webdriver
from time import sleep


scoreboard_url: str = "https://codingcompetitions.withgoogle.com/kickstart/round/0000000000051060"

driver = webdriver.Chrome()
driver.get(scoreboard_url)

scoreClass="user-total-score"
rankClass="ranking-table__row-cell__rank"
nameClass="ranking-table__row-cell__displayname"

scoreList=[]
rankList=[]
nameList=[]



# Wait for scoreboard to load
while not driver.find_elements_by_class_name(scoreClass):
    sleep(1)    

# Find number of pages in the scoreboard
numberOfPages=int(driver.find_element_by_class_name("ranking-table-page-number-total-pages").text.split()[1])



for page in range(numberOfPages):
    
    scoreElements=driver.find_elements_by_class_name(scoreClass)
    rankElements=driver.find_elements_by_class_name(rankClass)[1:]
    nameElements=driver.find_elements_by_class_name(nameClass)

    for i in range(len(scoreElements)):
        nameList.append(nameElements[i].find_element_by_tag_name("p").text)
        rankList.append(rankElements[i].text)
        scoreList.append(scoreElements[i].text)

    # If page is not the last page, wait till next page has loaded
    if page<numberOfPages-1:
        nextPageButton=driver.find_elements_by_tag_name("button")[-1]
        nextPageButton.click()
        while True:
            lastNameOnPage=driver.find_elements_by_class_name(nameClass)[-1].find_element_by_tag_name("p").text
            if lastNameOnPage!=nameList[-1]:
                break
            sleep(1)
    
'''    
# Write to csv    
with open("kickstart.csv","w") as scoreFile:
    scoreFile.write("Rank,UserName,Score\n")
    for i in range(len(nameList)):
        scoreFile.write(rankList[i]+","+nameList[i]+","+scoreList[i]+"\n")
'''

for username in nameList:
    print(username,end=" ")