Reduced Data = Day,Time,Quarter as determined to be the best by Weka
Full Data = All attributes 

Note: in the data with the class at the end, I also removed about 30 entries that had ‘-‘ as a value for Wind Speed.  This made it so Weka could not classify since Wind Speed was neither numerical nor nominal (it was both).  So I deleted them.