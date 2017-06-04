import csv

with open ('./data/test_lib_cleaned.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        with open('./data/weather_half_hour_duplicates_and_blanks_removed.csv','rb') as csvfile2:
            reader1 = csv.reader(csvfile2, delimiter = ',')
            for row1 in reader1:
                    if row[1] == row1[8] and row[2].replace('.0',"") == row1[9] and row[3].replace('.0',"") == row1[10] and row[4] == row1[0]:
                        with open('./data/merged_data.csv','a') as csvfile3:
                            writer = csv.writer(csvfile3, delimiter = ',')
                            writer.writerow([row[1],row[2],row[3],row[4],row[6],row1[1],row1[2],row1[3],row1[4],row1[5],row1[6],row1[7],row[5]])




# with open('./data/weather_half_hour_duplicates_and_blanks_removed.csv','rb') as csvfile2:
#     reader1 = csv.reader(csvfile2, delimiter = ',')
#     for row in reader1:
#         print row
