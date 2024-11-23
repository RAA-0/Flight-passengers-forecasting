import pandas as pd

class CustomizeData:
    def __init__(self,config):
        
        self.config = config
    def fit(self, X, y=None):
        return self
    
    def transform(self, X): 
        print("customizing....")
        X = self.sort_by_index(X)   
        X=self.filter(X)    
        X = self.select_and_rename_columns(X)
        X.to_csv(self.config.customized_path,index=False)
        print("Customiziation Done.")
        return X
    
    def sort_by_index(self,X):
        X = pd.DataFrame(X.sort_values(by=self.config.date_time_field))
        return X
    
    def filter(self,X):
        X = X[~X[self.config.date_time_field].dt.year.isin([2018,2019])]
        return X
    
    def select_and_rename_columns(self,X):
        X =X[self.config.columns]
        X.columns =self.config.renamed_columns
        return X
        

       