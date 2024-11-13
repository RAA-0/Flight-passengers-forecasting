import json 

class SentimentScore:
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
                X.loc[index, 'score'] = scores[str(year)][str(month).zfill(2)][str(day).zfill(2)]["compound"]
            except:
                X.loc[index, 'score'] = 0
        return X