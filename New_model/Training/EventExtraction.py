import json
import ast 
import pandas as pd 

class EventFeatureExtractor:
    def __init__(self):
        self.non_recurrent_events=[]
        with open('New_model\\event_config.json') as r:
            event_config=json.load(r)
        for event in event_config.keys():
            if event_config[event]['type']=='variable_dates_events':
                self.non_recurrent_events.append(event)
    def fit(self,X,y=None):
        return self

    def transform(self,X):
        print('extracting...')
        X= self.lag_ffeatures(X)
        for event in self.non_recurrent_events:
            X[event] = X['event'].apply(lambda events: 1 if event in events else 0)
        return X


    def lag_ffeatures(self, df):

        training_data = pd.read_csv('New_model\\data\\Training\\TrainingData.csv')
        training_data['arrival_mean'] = training_data.groupby('event')['arrival_percentage_change'].transform('mean')
        training_data['departure_mean'] = training_data.groupby('event')['departure_percentage_change'].transform('mean')
        new_rows = []
        for index, row in df.iterrows():
                filtered_df = training_data[training_data['event'].isin(ast.literal_eval(row['event']))]
                sorted_df = filtered_df.sort_index(ascending=False)
                new_row = dict(row)
                for lag_col in ["arrival","departure"]:
                    if len(sorted_df) >= 1:  
                        new_row[f'{lag_col}_pct_change_lag1'] = sorted_df.head(1)[f"{lag_col}_percentage_change"].values[0]
                    else:
                        print("shu l hal?")
                new_rows.append(new_row)

        prediction_dataset = pd.DataFrame(new_rows)
        print(prediction_dataset)
        return prediction_dataset 
        df['arrival_pct_change_lag1'] = df.groupby(['event'])['arrival_percentage_change'].shift(1)
        df['departure_pct_change_lag1'] = df.groupby(['event'])['departure_percentage_change'].shift(1)

        df['mean'] = df.groupby('event')['arrival_percentage_change'].transform('mean')
        df['arrival_pct_change_lag1'].fillna(df['mean'], inplace=True)

        df['mean'] = df.groupby('event')['departure_percentage_change'].transform('mean')
        df['departure_pct_change_lag1'].fillna(df['mean'], inplace=True)
        return df 