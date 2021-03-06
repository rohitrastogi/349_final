import pandas as pd
import datetime as dt
import timeit
import matplotlib.pyplot as plt


def fill_columns(df):
    start_time = timeit.default_timer()
    print 'filling columns...' + '\n'
    for col in list(df):
        df[col] = df[col].ffill()
    end_time = timeit.default_timer()
    print 'fill_columns(): ' + str(end_time - start_time) + "\n"
    return df

#half is boolean - if true, round half hour, if false, round full hour
def round_time(df, half):
    start_time = timeit.default_timer()
    print 'rounding times...' + '\n'
    df["Time"] = ""
    for i, row in df.iterrows():
        num_minutes = df.iloc[i]['Minute']
        num_hours = df.iloc[i]['Hour']
        if num_minutes < 30 and num_minutes >= 0:
            df.set_value(i, 'Time', str(int(num_hours)) +  "00")
        elif num_minutes < 60 and num_minutes >= 30:
            if half:
                df.set_value(i, 'Time', str(int(num_hours)) +  "30")
            else:
                df.set_value(i, 'Time', str(int(num_hours) + 1) + "00")
    df = df.drop('Minute', axis = 1)
    df = df.drop('Hour', axis = 1)
    end_time = timeit.default_timer()
    print 'round_time(): ' + str(end_time - start_time) + "\n"
    return df

def sum_on_time(df):
    start_time = timeit.default_timer()
    print 'summing totals...' + '\n'
    df['Total'] =  df.groupby(['Day', 'Time', 'Month', 'Year'])['Number'].transform(sum)
    df = df.drop('Number', axis = 1)
    df = df.drop_duplicates()
    end_time = timeit.default_timer()
    print 'sum_on_time(): ' + str(end_time - start_time) + "\n"
    return df

#subject to change
def add_quarter(df):
    start_time = timeit.default_timer()
    print 'adding quarters ...' + '\n'
    df["Quarter"] = ""
    df["Quarter Progress"] = ""
    df = df.reset_index(drop=True)
    quarters = {
    'summer_15_start': dt.datetime(2015, 6, 22),
    'summer_15_end' : dt.datetime(2015, 8, 15),
    'fall_15_start': dt.datetime(2015, 9, 11),
    'fall_15_end': dt.datetime(2015, 12, 12),
    'winter_16_start': dt.datetime(2016, 1, 4),
    'winter_16_end': dt.datetime(2016, 3, 19),
    'spring_16_start': dt.datetime(2016, 3, 29),
    'spring_16_end': dt.datetime(2016, 6, 11),
    'summer_16_start': dt.datetime(2016, 6, 20),
    'summer_16_end': dt.datetime(2016, 8, 13)}

    for i, row in df.iterrows():
        date = dt.datetime(int(df.iloc[i]['Year']), int(df.iloc[i]['Month']), int(df.iloc[i]['Day']))
        if date >= quarters['summer_15_start'] and date <= quarters['summer_15_end']:
            df.set_value(i, 'Quarter', 'Summer')
            completed_days = (date - quarters['summer_15_start']).days
            days_in_quarter = (quarters['summer_15_end'] - quarters['summer_15_start']).days
            df.set_value(i, 'Quarter Progress', completed_days/float(days_in_quarter))
        elif date >= quarters['fall_15_start'] and date <= quarters['fall_15_end']:
            df.set_value(i, 'Quarter', 'Fall')
            completed_days = (date - quarters['fall_15_start']).days
            days_in_quarter = (quarters['fall_15_end'] - quarters['fall_15_start']).days
            df.set_value(i, 'Quarter Progress', completed_days/float(days_in_quarter))
        elif date >= quarters['winter_16_start'] and date <= quarters['winter_16_end']:
            df.set_value(i, 'Quarter', 'Winter')
            completed_days = (date - quarters['winter_16_start']).days
            days_in_quarter = (quarters['winter_16_end'] - quarters['winter_16_start']).days
            df.set_value(i, 'Quarter Progress', completed_days/float(days_in_quarter))
        elif date >= quarters['spring_16_start'] and date <= quarters['spring_16_end']:
            df.set_value(i, 'Quarter', 'Spring')
            completed_days = (date - quarters['spring_16_start']).days
            days_in_quarter = (quarters['spring_16_end'] - quarters['spring_16_start']).days
            df.set_value(i, 'Quarter Progress', completed_days/float(days_in_quarter))
        elif date >= quarters['summer_16_start'] and date <= quarters['summer_16_end']:
            df.set_value(i, 'Quarter', 'Summer')
            completed_days = (date - quarters['summer_16_start']).days
            days_in_quarter = (quarters['summer_16_end'] - quarters['summer_16_start']).days
            df.set_value(i, 'Quarter Progress', completed_days/float(days_in_quarter))
        #may need to remove
        else:
            df.set_value(i, 'Quarter', 'Other')
            df.set_value(i, 'Quarter Progress', 0.0)
    end_time = timeit.default_timer()
    print 'add_quarter(): ' + str(end_time - start_time) + "\n"
    return df


def add_class(df):
    #starting at 25, 50, 75, 100 percentile
    start_time = timeit.default_timer()
    print 'adding class...' + '\n'
    df['Class'] = ""

    #half-hour quartiles
    # empty = 16
    # not_busy = 51
    # moderately_busy = 125

    # hour quartiles
    empty = 24
    not_busy = 86
    moderately_busy = 242

    # half-hour arbitrary
    # empty = 50
    # not_busy = 100
    # moderately_busy = 150

    for i, row in df.iterrows():
        total = df.iloc[i]['Total']
        if total <= empty:
            df.set_value(i, 'Class', 'Empty')
        elif total <= not_busy:
            df.set_value(i, 'Class', 'Not Busy')
        elif total <= moderately_busy:
            df.set_value(i, 'Class', 'Moderately Busy')
        else:
            df.set_value(i, 'Class', 'Busy')
    df = df.drop('Total', axis = 1)
    end_time = timeit.default_timer()
    print 'add_class(): ' + str(end_time - start_time) + "\n"
    return df

def remove_other(df):
    df = df[df["Quarter"] != "Other"]
    return df

def main():
    print 'calling main ...' + '\n'
    uncleaned_input = 'data/lib/uncleaned_lib.csv'
    dataframe = pd.read_csv(uncleaned_input)

    filled = fill_columns(dataframe)
    rounded = round_time(filled, False)
    summed = sum_on_time(rounded)
    quartered = add_quarter(summed)
    with_class = add_class(quartered)
    removed_other = remove_other(with_class)

    with_class.to_csv('hour.csv', index = False)
    #removed_other.to_csv('no_other.csv', index = False)

    # get descriptive statistics
    # print quartered['Total'].describe()

    # show boxplot
    # quartered.boxplot(column = 'Total')
    # plt.show()

if __name__ == "__main__": main()
