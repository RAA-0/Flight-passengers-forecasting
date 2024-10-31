import pandas as pd

class CustomizeData:
    def __init__(self,config):
        
        self.config = config
    def fit(self, X, y=None):
        return self
    
    def transform(self, X): 
        print("customizing....")
        X = self.sort_by_index(X)     
        X = self.filter(X) 
        X = self.select_and_rename_columns(X)
        X.to_csv(f"data\\customized_data\\{self.config['type']}_customized.csv",index=False)
        print("Customiziation Done.")
        return X
    
    def sort_by_index(self,X):
        X = pd.DataFrame(X.sort_values(by=self.config['index']))
        return X
    
    def filter(self,X):
        #2-remove the data in specific years (2020-2021) due to the pandemic  
        X = X[~X[self.config['index']].dt.year.isin([2018,2019,2020,2021])]
        return X
    
    def select_and_rename_columns(self,X):
        X =X[self.config['columns']]
        X.columns = self.config["new_names"]
        return X
        

       
