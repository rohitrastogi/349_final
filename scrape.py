import pandas as pd
import numpy as np
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import re
from copy import deepcopy

#retrieves an ordered list of links for all days
def get_links(months):
    base_link = "https://www.wunderground.com/history/airport/KPWK/"
    month_to_day = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    links = []
    for month in months:
        for day in range(1, month_to_day[month[1]] + 1):
            date_link = [str(month[0]), str(month[1]), str(day), "DailyHistory.html"]
            links.append(base_link + "/".join(date_link))
    return links

#rounds times down from scraped table to the nearest half hour
def round_time(time):
    if int(time[3]) >= 3:
        time = time[0:3] + "30"
    else:
        time = time [0:3] + "00"
    return time.replace(":","")

#converts time from scraped table to military time consistent with library data
def convert_to_military(time):
    in_time = datetime.strptime(time, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

#beautifies scraped output
def strip_ascii(text):
    text = text.encode('ascii', 'ignore').decode('ascii').strip('\n\t')
    return text

def remove_units(df):
    df["Wind Speed"].replace("Calm", 0.0, inplace = True)
    #replacing percent doesnt work
    #df["Humidity"].replace('%', '', inplace = True).astype('float')/100
    return df

#fills missing half hour weather data with data from the previous half hour
def duplicate(weather):
    dup_weather = []
    for i, weather_row in enumerate(weather):
        dup_weather.append(weather_row)
        if i < len(weather) - 1:
            temp_weather_row = deepcopy(weather_row)
            if int(weather[i+1][0]) - int(weather_row[0]) >= 100:
                if weather_row[0][2:] == "30":
                    if temp_weather_row[0][1] == '9' and temp_weather_row[0][0] == '0':
                        temp_weather_row[0] = '1000'
                    elif temp_weather_row[0][1] == '9' and temp_weather_row[0][0] == '1':
                        temp_weather_row[0] = '2000'
                    else:
                        temp_weather_row[0] = temp_weather_row[0][0] + str(int(temp_weather_row[0][1])+ 1) + "00"
                else:
                    temp_weather_row[0] = temp_weather_row[0][0:2] + "30"
        dup_weather.append(temp_weather_row)
    first_weather_row = deepcopy(dup_weather[0])
    first_weather_row[0] = '0000'
    dup_weather.insert(0, first_weather_row)
    return dup_weather

#scrapes weather table for each day link passed
def scrape_day(url, header):
    #setup
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    #2d array that holds scraped data
    day_weather = []
    year = url.split('/')[6]
    month = url.split('/')[7]
    day = url.split('/')[8]

    #check if there is data
    if len(soup.find_all('table')) == 5:
        print str(month) + "-" + str(day) + "-" + str(year) + "\n" #status check
        table = soup.find_all('table')[4]
        prev_time = '1'
        for hour in table.find_all('tr')[1:]:
            hour_weather = []
            temp_hour_weather = hour.find_all('td')
            curr_time = round_time(convert_to_military(strip_ascii(temp_hour_weather[0].get_text())))
            if curr_time != prev_time:
                hour_weather.append(curr_time)
                prev_time = curr_time
                for ci, column in enumerate(temp_hour_weather[1:]):
                    if len(temp_hour_weather[1:]) == 11:
                        skip_cols = [5, 7, 8, 9]
                    #skip days where windchill and heat index are included
                    else:
                        skip_cols = [1, 6, 8, 9, 10]
                    if ci not in skip_cols:
                        column_text = strip_ascii(column.get_text())
                        hour_weather.append(column_text)
                prev_time = curr_time
                day_weather.append(hour_weather)

        #add succesfully populated 2d array to dataframe
        day_df = pd.DataFrame(duplicate(day_weather), columns = np.asarray(header[0:8]))
        day_df.set_value(0, 'Year', year)
        day_df.set_value(0, 'Month', month)
        day_df.set_value(0, 'Day', day)
        day_df.drop_duplicates()
        fill = ['Year', 'Month', 'Day']
        day_df[fill] = day_df[fill].ffill()
        return day_df

# adds date columns to each day's weather dataframe and concatenates all dataframes
def scrape(header, months):
    weather_df = pd.DataFrame(columns = np.asarray(header))
    for link in get_links(months):
        day_df = scrape_day(link, header)
        if day_df is None:
            #skip
            continue
        weather_df = pd.concat([weather_df, day_df])
    weather_df = weather_df.reset_index(drop=True)
    cleaned_df = remove_units(weather_df)
    cleaned_df.to_csv("weather.csv")
    return remove_units(cleaned_df)

def main():
    month_range = [
    (2015, 7)
    # (2015, 8),
    # (2015, 9),
    # (2015, 10),
    # (2015, 11),
    # (2015, 12),
    # (2016, 1),
    # (2016, 2),
    # (2016, 3),
    # (2016, 4),
    # (2016, 5),
    # (2016, 6),
    # (2016, 7),
    # (2016, 8),
    # (2016, 9)
]

    header = ["Time", "Temp", "Dew Point", "Humidity", "Pressure", "Visibility", "Wind Speed", "Conditions", "Year", "Month", "Day"]
    scrape(header, month_range)


if __name__ == "__main__": main()
