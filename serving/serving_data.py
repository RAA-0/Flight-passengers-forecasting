import joblib

class DataServer:
    def __init__(self,config,data):
        self.config = config
        self.data = data 
        self.targets = ['total','transfer_percentage']
        
    
    def serve(self):
        self.df_=self.data.copy()
        for target in self.targets:
            self.df = self.drop_columns(target)
            model = self.get_model(target)
            predictions = model.predict(self.df)
            self.df_[f'predicted_{target}'] = predictions
        self.df_.to_csv(self.config.result_path,index=False)
        return self.df_

    def get_model(self,target):
        model_path = "Training\\models\\lightgbm_model_"+target+"_"+self.config.type+"1.pkl"
        model = joblib.load(model_path)
        return model 
    
    def drop_columns(self,target):
        data = self.data.drop(columns=self.config.columns_to_drop(target))
        return data 

        

        