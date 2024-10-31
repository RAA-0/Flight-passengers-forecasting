import pandas as pd



class Cleaner:
    def __init__(self,config):
        self.config = config

    def fit(self, X, y=None):
        return self
    def transform(self,X):
        print("cleaning....")
        X = self.handle_missing_values(X)
        X = self.drop_illogical_values(X)
        X= self.drop_wrong_values(X)
        print("Cleaning DOne.")
        return X 
    
    def handle_missing_values(self,X):
        #1-fill missing values in the target with zeros    
        X["transfer"]=X["transfer"].fillna(0)
        #2-dropping missing values in features 
        features = ["date_time","transfer","origin","destination","disembarking","joining","airline","ac_type","capacity","GDP","total_lag1","total_lag2","total_lag3",'transfer_percentage_lag1','transfer_percentage_lag2','transfer_percentage_lag3']
        features = [col for col in features if col in X.columns]
        X=X.dropna(subset=features)
        return X
    
    def drop_illogical_values(self,X):
        #1- if the total is not the sum of transfer and disembarking 
        X = X[X["transfer"]+X[self.config['distinct_feature']]==X["total"]]
        #2- dropping negative values 
        X = X[(X[self.config['distinct_feature']]>=0) & (X["total"]>=0)] 
        #3- dropping if the total > capacity 
        X=X[X["total"]<=X["capacity"]]
        return X
    
    def drop_wrong_values(self,X):
        #4- droping wrong country/airline values 
        wrong_values = ['ZZZF','LOCL','no data','None']
        X = X[~X[self.config['column_to_check']].isin(wrong_values).any(axis=1)]
        return X




    






       
    