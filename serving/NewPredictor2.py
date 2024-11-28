import pandas as pd 
import joblib
from sklearn.metrics import r2_score

class NewPredictor:
    def __init__(self,df,config):
        self.df = df
        self.config = config 
  

    def start_new_prediction(self):
        print("starting new predictions.....")
        self.predict_changes()
        self.new_prediction()


    def predict_changes(self):
        model=joblib.load(self.config.prophet_model_path)
        self.df.sort_values(by='ds', inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        predictions = model.predict(self.df)['yhat']
        self.df['predicted_change'] = predictions
     

    def new_prediction(self):
        self.df['new_prediction']=self.df['predicted_total']*(1+self.df['predicted_change']/100)
        self.df['new_prediction'] = self.df['new_prediction'].clip(lower=0, upper=self.df['capacity'])
        self.df[['ds','event','predicted_total','predicted_change','new_prediction']].to_csv(self.config.result_path,index=False)



    