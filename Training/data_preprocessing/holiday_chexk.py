import json 

class CheckHoliday:
    def __init__(self,json_path):
        self.json_path = json_path

    def fit(self, X, y=None):
        return self
    
    def transform(self,X):
        print("extracting holidays")
        with open(self.json_path) as hj:
            holidays = json.load(hj)
        month_mapping = {
                            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
                        }
        X['holiday'] = False
        for index,row in X.iterrows():
                year = row["date_time_year"]
                month = row["date_time_month"]
                day = row["date_time_day_of_month"]
                for holiday, dates_list in holidays[str(year)].items():
                    for date in dates_list:
                        if month_mapping[date[1]] == str(month).zfill(2) and date[0] == str(day):
                            X.loc[index, 'holiday'] = True
                            break  
        return X
                   
                        
    
