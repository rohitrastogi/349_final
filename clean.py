import pandas as pd
import numpy as np
import datetime
import timeit

def fill_columns(df):
    start_time = timeit.default_timer()
    print 'filling columns...' + '\n'
    for col in list(df):
        df[col] = df[col].ffill()
    end_time = timeit.default_timer()
    print 'fill_columns(): ' + str(end_time - start_time) + "\n"
    return df

def round_time_down(df):
    start_time = timeit.default_timer()
    print 'rounding times...' + '\n'
    df["Time"] = np.nan
    for i in df.iterrows():
        num_minutes = df.iloc[i]['Minute']
        num_hours = df.iloc[i]['Hour']
        if num_minutes < 30 and num_minutes >= 0:
            df.set_value(i, 'Time', str(int(num_hours)) +  "00")
        elif num_minutes < 60 and num_minutes >= 30:
            df.set_value(i, 'Time', str(int(num_hours)) +  "30")
    df = df.drop('Minute', axis = 1)
    df = df.drop('Hour', axis = 1)
    end_time = timeit.default_timer()
    print 'round_time_down(): ' + str(end_time - start_time) + "\n"
    return df

def sum_half_hour(df):
    start_time = timeit.default_timer()
    print 'summing totals...' + '\n'
    df['Total'] =  df.groupby(['Day', 'Time'])['Number'].transform(sum)
    df = df.drop('Number', axis = 1)
    df = df.drop_duplicates()
    end_time = timeit.default_timer()
    print 'sum_half_hour(): ' + str(end_time - start_time) + "\n"
    return df

#subject to change
def add_quarter(df):
    start_time = timeit.default_timer()
    print 'adding quarters ...' + '\n'
    df["Quarter"] = np.nan
    df = df.reset_index(drop=True)
    quarters = {
    'summer_15_start': (2015, 6, 22),
    'summer_15_end' : (2015, 8, 15),
    'fall_15_start': (2015, 9, 11),
    'fall_15_end': (2015, 12, 12),
    'winter_16_start': (2016, 1, 4),
    'winter_16_end': (2016, 3, 19),
    'spring_16_start': (2016, 3, 29),
    'spring_16_end': (2016, 6, 11),
    'summer_16_start': (2016, 6, 20),
    'summer_16_end': (2016, 8, 13)}
    for i, row in df.iterrows():
        date = (int(df.iloc[i]['Month']), int(df.iloc[i]['Day']))
        if date >= quarters['summer_15_start'] and date <= quarters['summer_15_end']:
            df.set_value(i, 'Quarter', 'Fall')
        elif date >= quarters['fall_15_start'] and date <= quarters['fall_15_end']:
            df.set_value(i, 'Quarter', 'Fall')
        elif date >= quarters['winter_16_start'] and date <= quarters['winter_16_end']:
            df.set_value(i, 'Quarter', 'Winter')
        elif date >= quarters['spring_16_start'] and date <= quarters['spring_16_end']:
            df.set_value(i, 'Quarter', 'Spring')
        elif date >= quarters['summer_16_start'] and date <= quarters['summer_16_end']:
            df.set_value(i, 'Quarter', 'Summer')
        else:
            df.set_value(i, 'Quarter', 'Other')
    end_time = timeit.default_timer()
    print 'add_quarter(): ' + str(end_time - start_time) + "\n"
    return df

#0 = Monday...
# need to catch bad day month combination
def add_weekday(df):
    start_time = timeit.default_timer()
    print 'adding weekdays...' + '\n'
    for i in df.iterrows():
        year = df.iloc[i]['Year']
        month = df.iloc[i]['Month']
        day = df.iloc[i]['Day']
        weekday = datetime.datetime(int(year), int(month), int(day)).weekday()
        df.set_value(i, 'Day', weekday)
    end_time = timeit.default_timer()
    print 'add_weekday(): ' + str(end_time - start_time) + "\n"
    return df

def main():
    print 'calling main ...' + '\n'
    test_file = './data/default.csv'
    dataframe = pd.read_csv(test_file)

    filled = fill_columns(dataframe)
    rounded = round_time_down(filled)
    summed = sum_half_hour(rounded)
    quartered = add_quarter(summed)
    weekdayed = add_weekday(quartered)
    #filled.to_csv('test.csv')

if __name__ == "__main__": main()
