import pandas as pd
import timeit
import datetime as dt

#lib should be outer
def join_pds(outer, inner):
    start_time = timeit.default_timer()
    indexed_outer = outer.set_index(['Time', 'Day', 'Month', 'Year'])
    indexed_inner = inner.set_index(['Time', 'Day', 'Month', 'Year'])
    joined = indexed_outer.join(indexed_inner, how = 'inner', lsuffix = '_l', rsuffix = '_r')
    joined = joined.reset_index(level = ['Time', 'Day', 'Month', 'Year'])
    end_time = timeit.default_timer()
    print 'join_pds(): ' + str(end_time - start_time) + "\n"
    return move_class_right(joined)

#0 = Monday...
# need to catch bad day month combination
def add_weekday(df):
    start_time = timeit.default_timer()
    print 'adding weekdays...' + '\n'
    for i, row in df.iterrows():
        year = df.iloc[i]['Year']
        month = df.iloc[i]['Month']
        day = df.iloc[i]['Day']
        try:
            weekday = dt.datetime(int(year), int(month), int(day)).weekday()
            df.set_value(i, 'Day', weekday)
        except ValueError:
            print str(day) + "-" + str(month) + "-" + str(year) + "\n"
    df = df.drop('Month', axis = 1)
    end_time = timeit.default_timer()
    print 'add_weekday(): ' + str(end_time - start_time) + "\n"
    return df

def move_class_right(df):
    cols = list(df.columns.values)
    cols.pop(cols.index('Class'))
    df = df[cols + ['Class']]
    return df

def main():
    #read csvs
    weather_csv = 'data/weather/half.csv'
    lib_csv = 'data/lib/no_other.csv'
    weather_pd = pd.read_csv(weather_csv)
    lib_pd = pd.read_csv(lib_csv)

    joined = join_pds(lib_pd, weather_pd)
    weekdayed = add_weekday(joined)
    weekdayed.to_csv('joined.csv', index = False)


if __name__ == "__main__": main()
