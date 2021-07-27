from bs4 import BeautifulSoup
import requests
import json
#import sqlite3
import os

databasename = 'weatherspark'

def getWeathersparkHomepage():

    datavar = requests.get('https://weatherspark.com/y/144837/Average-Weather-in-Christchurch-New-Zealand-Year-Round')
    textvar = datavar.text
    soupvar = BeautifulSoup(textvar, 'html.parser')

    filevar = open('testfile.htm', 'w')
    writevar = filevar.write(str(soupvar.prettify))
    filevar.close()
    return "Weatherspark homepage retrieved!"

def setUpDatabase(db_name): # function that creates/connects us to the SQL database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def saveAPage():

    datavar = requests.get("https://weatherspark.com/random")
    textvar = datavar.text
    soupvar = BeautifulSoup(textvar, 'html.parser')

    upvar1 = soupvar.find(id = "Sidebar-Container")
    countylink = upvar1.find('a')['href']

    upvar2 = soupvar.find(class_ = "breadcrumb hidden-lg hidden-print")
    placename = upvar2.find_all('li')[-1].text

    #filevar = open(str(str(placename.strip('\n')) + '/' + str(countylink)).replace('/', '|') + '.htm', 'w')
    #writevar = filevar.write(soupvar.prettify())
    #filevar.close()

    return str(placename.strip('\n')) + '/' + str(countylink)

#getWeathersparkHomepage()

# just save each page? it's probably easier

#cur, conn = setUpDatabase(databasename)
#conn.close()

#for num in range(1000):
    #print(saveAPage())

def scoreEntries(numarg):

    for anynum in range(numarg):
        filename = os.listdir()[numarg]
        if filename[-4:] == '.htm':
            filevar = open(filename)
            readvar = filevar.read()
            soup = BeautifulSoup(readvar, 'html.parser')
            returnvar = soup.find('p').find_all('em')
            minmaxtemps = tuple(anyentry.text.strip('\n').strip().replace('Â', '') for anyentry in returnvar)
            if int(minmaxtemps[2][:-2]) >= 10 and int(minmaxtemps[3][:-2]) <= 85:
                return minmaxtemps
            #for anytag in soup:
            #    print(type(anytag))

print(scoreEntries(200))
#print(os.listdir())
#print(saveAPage())
#print(getWeathersparkHomepage())

# Criteria #
# Minimum 45% sunny in winter, maximum 75% sunny in summer
# wind speed not in excess of 20mph in summer, 15mph in winter
# div class_ = Figure-chart is what we need to access to get all the data charts
# the first one of these has min max cloudiness stats, min max rainfall stats
# the blurb at the top has min max temp stats
# the fifth figure-chart has min max precip chance stats
# the seventh figure-chart has min max sunlight hours stats
# the eleventh figure-chart has min max windspeed stats
# 
# 
# 
# Collect Maxmax, max, avgmax, avgmin, min, and minmin temps, max sun, min sun, max wind, min wind, 
