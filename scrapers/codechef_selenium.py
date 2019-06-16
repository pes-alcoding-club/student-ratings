from selenium import webdriver
from time import sleep
from collections import namedtuple

chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2,  # does not load images on web page
         'disk-cache-size': 1024}  # use disk cache to reduce page load time
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chromeOptions)

scoreboard_base_url:str = "https://www.codechef.com/rankings"
site_url="https://www.codechef.com"
scoreboard_filter_query:str = "?filterBy=Institution%3DPES%20University%2C%20Bengaluru&order=asc&sortBy=rank"
contest_code:str="COOK106"
name_class:str="user-name"

division=namedtuple('division',['problems','scraped_scoreboard'])
divisions:dict={'A':division(set(),list()),'B':division(set(),list())}
final_scoreboard:list=list()
easy_points:int=100 # Points to add to division A participants assuming they can solve all easy div B problems
if contest_code[0:4]=="COOK":
    easy_points=100000 # Initial value set to points per problem

for division in divisions:
    # To get list of problems in contest page
    driver.get(f"{site_url}/{contest_code}{division}")
    while not driver.find_elements_by_tag_name("tbody"): # wait till contest page has loaded
        sleep(0.1)
    table_rows=driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    for row in table_rows:
        divisions[division].problems.add(row.find_elements_by_tag_name("td")[1].text)
    
    # To obrain PES scoreboard in contest
    driver.get(f"{scoreboard_base_url}/{contest_code}{division}{scoreboard_filter_query}")    
    while not driver.find_elements_by_tag_name("tbody"): # wait till scoreboard has loaded
        sleep(0.1)    
    total_pages=int(driver.find_elements_by_class_name("jump")[-1].find_element_by_tag_name("a").text)
    for page in range(total_pages):    
        name_elements=driver.find_elements_by_class_name(name_class)
        score_elements=driver.find_elements_by_xpath("//td[@class='num']//div[not(@class) and (@title='' or not(@title))]")
        if contest_code[0:4]=="COOK":
            # For cook-off contests, there's an extra penalty provision, we need only the alternate elements.
            score_elements=score_elements[::2]            
            ''' Extract all time elements, remove semi-colons, convert to numeric type. 
                Smaller the time, the better. But score needs to be generated with left most digit being
                number of points, hence time's subtracted from 100000 to allow descending order of scores '''            
            time_elements=list(map(lambda x:100000-float(x.text.replace(":","")), driver.find_elements_by_class_name("total-time")))
            # The score's added to the left of the time             
            divisions[division].scraped_scoreboard.extend(zip(
                [x.find_elements_by_tag_name("span")[-1].text for x in name_elements],
                [float(score_elements[i].text.split()[0])*100000+time_elements[i] for i in range(len(score_elements))]))        
        else:
            divisions[division].scraped_scoreboard.extend(zip(
                [x.find_elements_by_tag_name("span")[-1].text for x in name_elements],
                [float(y.text.split()[0]) for y in score_elements]))                
        if page==total_pages-1: # Reached Last Page
            break    
        driver.get(f"{scoreboard_base_url}/{contest_code}{division}{scoreboard_filter_query}&page={page+2}") # go to next page
        while int(driver.find_elements_by_class_name("active")[-1].text) == page+1: # wait till next page has loaded
            sleep(0.1)
driver.close()

easy_points=len(divisions['B'].problems-divisions['A'].problems)*easy_points

for i in range(len(divisions['A'].scraped_scoreboard)): # Add easy points to all div-A participants
    divisions['A'].scraped_scoreboard[i]=divisions['A'].scraped_scoreboard[i][0],divisions['A'].scraped_scoreboard[i][1]+easy_points
print(divisions)
final_scoreboard.extend(divisions['A'].scraped_scoreboard)
final_scoreboard.extend(divisions['B'].scraped_scoreboard)
final_scoreboard=sorted(final_scoreboard,key=lambda x:x[1],reverse=True) # Sort list in desc. order based on points. (username, points)

if final_scoreboard: # If scoreboard's not empty    
    if contest_code[0:5]=="LTIME" or contest_code[0:4]=="COOK":
        print(*[x[0] for x in final_scoreboard], sep="\n")  
    else: # Shared ranking possible for long contests.
        last_score=final_scoreboard[0][1]
        for user in final_scoreboard:
            if user[1]!=last_score:
                print()
                last_score=user[1]
            print(user[0],end=" ")    
