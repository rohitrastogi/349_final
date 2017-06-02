import pandas as pd
import numpy as np
import urllib2
from bs4 import BeautifulSoup

#setup
link = "https://www.wunderground.com/history/airport/KPWK/2015/7/1/DailyHistory.html"
html = urllib2.urlopen(link).read()
soup = BeautifulSoup(html, "lxml")
table = soup.find_all('table')[4]

#months

header = list(map(lambda x: x.get_text(), table.find_all('th')))



weather = []
#write to dataframe directly?
for ri,row in enumerate(table.find_all('tr')[1:]):
    timestep = []
    for ci, column in enumerate(row.find_all('td')):
        timestep.append(column.get_text().encode('ascii', 'ignore').decode('ascii').strip('\n\t'))
    weather.append(timestep)


sum = pd.DataFrame(weather, columns = np.asarray(header))
