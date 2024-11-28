import pandas as pd 
import joblib
from sklearn.metrics import r2_score

class NewPredictor:
    def __init__(self,df,config):
        self.df = df
        self.config = config 
        self.df_with_events= pd.DataFrame()
        self.df_wihtout_events=pd.DataFrame()

    def start_new_prediction(self):
        print("starting new predictions.....")
        self.classify_data_with_events()
        self.predict_changes()
        self.new_prediction()


    def predict_changes(self):
        model=joblib.load(self.config.prophet_model_path)
        self.df_with_events.sort_values(by='ds', inplace=True)
        self.df_with_events.reset_index(drop=True, inplace=True)
        try:
            predictions = model.predict(self.df_with_events)['yhat']
            self.df_with_events['predicted_change'] = predictions
        except ValueError:
            print("no events detected!")
        self.df_without_events['predicted_change']=0

    def new_prediction(self):
        df = (pd.concat([self.df_without_events,self.df_with_events])).sort_values(by='ds')
        df['new_prediction']=df['predicted_total']*(1+df['predicted_change']/100)
        df['new_prediction'] = df['new_prediction'].clip(lower=0, upper=df['capacity'])
        df[['ds','event','predicted_total','predicted_change','new_prediction']].to_csv(self.config.result_path,index=False)

    def classify_data_with_events(self):
        events = ["pandemic","ramadan_season","hajj_season","new_years_eve","eid_al_adha","christmas_season","weather_disruptions","no_major_event","summer_season","diwali"]
        self.df['has_significant_event'] = self.df['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events))
        self.df_with_events = self.df[self.df['has_significant_event']].copy()
        self.df_without_events = self.df[~self.df['has_significant_event']].copy()

    