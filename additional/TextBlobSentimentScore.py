import json 

class TextBlobScore:
    def __init__(self,json_path):
        self.json_path = json_path
    def fit(self, X, y=None):
        return self
    def transform(self,X):
        print("Sentiment scores are being extracted...")
        with open(self.json_path) as sr:
            scores = json.load(sr)
        for index,row in X.iterrows():
            year = row["date_time_year"]
            month = row["date_time_month"]
            day = row["date_time_day_of_month"]
            print("still in the process",year,month,day)
            try:
                X.loc[index, 'polarity'] = scores[str(year)][str(month).zfill(2)][str(day).zfill(2)]["polarity"]
                X.loc[index, 'subjectivity'] = scores[str(year)][str(month).zfill(2)][str(day).zfill(2)]["subjectivity"]
            except:
                X.loc[index, 'polarity'] = 0
                X.loc[index, 'subjectivity'] = 0
        return X