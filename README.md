# 349_final

**Scripts used to clean library data and scrape/clean weather data for 349 Final Project**

Interpret our data:

**/data/weather -> data outputted from get_weather.py**
- half.csv (half-hour bucket features)
- hour.csv (hour bucket features)

**/data/lib -> data outputted from clean_library.py**
- arbitrary.csv (half-hour bucket features with arbitrary class bucketing)
- hour.csv (hour bucket features with quartile class bucketing)
- no_other.csv (half hour bucket features with quartile class bucketing, instances that have quarter = 'other' are removed
- w_other.csv (half hour bucket features with quartile class bucketing)
- uncleaned_lib.csv (data given to us by library in csv format)

**/data/joined -> data outputted from join_data.py**
- arbitrary.csv (half-hour bucket features with arbitrary class bucketing)
- hour.csv (hour bucket features with quartile class bucketing)
- no_other.csv (half hour bucket features with quartile class bucketing, instances that have quarter = 'other' are removed
- w_other.csv (half hour bucket features with quartile class bucketing)
