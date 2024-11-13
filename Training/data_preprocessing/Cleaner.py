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
        X["transfer"]=X["transfer"].fillna(0)
        #features = ["date_time","transfer","origin","destination","disembarking","joining","airline","ac_type","capacity","GDP"]
        features = ["date_time","transfer","origin","destination","disembarking","joining","airline","ac_type","capacity","GDP","total_lag1","total_lag2","total_lag3",'transfer_percentage_lag1','transfer_percentage_lag2','transfer_percentage_lag3']
        features = [col for col in features if col in X.columns]
        X=X.dropna(subset=features)
        return X
    
    def drop_illogical_values(self,X):
        X = X[X["transfer"]+X[self.config['distinct_feature']]==X["total"]]
        X = X[(X[self.config['distinct_feature']]>=0) & (X["total"]>=0)] 
        X=X[X["total"]<=X["capacity"]]
        return X
    
    def drop_wrong_values(self,X):
        wrong_values = ['ZZZF','LOCL','no data','None']
        X = X[~X[self.config['column_to_check']].isin(wrong_values).any(axis=1)]
        return X




    






       
    