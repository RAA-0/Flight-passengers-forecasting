import json
import pandas as pd
from feature_engine.timeseries.forecasting import LagFeatures
import numpy as np 

class FeatureExtractor:
    def __init__(self,config):
        self.config = config

    def fit(self, X, y=None):
        return self
    
    def transform(self,X): 
        print("extracting....")
        self.X= self.extractTotalSeats(X)
        if self.config.type == 'arrival':
            self.X= self.extractGdp(self.X) 
        self.X = self.extract_percentage(self.X)
        self.X = self.extract_lag_features(self.X)
        print("Feature Extraction Done.")
        return self.X
      
    def extractTotalSeats(self,X):
        with open(self.config.aircraft_json_path) as f:
            aircraft_data = json.load(f)
        X["capacity"]=X["code"].apply(lambda r: aircraft_data.get(r, {}).get('totalSeats', None) )
        return X
    
    def extractGdp(self, X):
        with open(self.config.airport_json_path) as a:
            airports_data = json.load(a)
        with open(self.config.gdp_json_path) as g:
            gdp_data = json.load(g)

        def get_country_code(row):
            icao = row["origin"] 
            country = airports_data.get(icao, {}).get("country", None)  
            return country
        def get_gdp(row):
            country_code = get_country_code(row)
            if country_code=='':
                return None
            else:
                #year = str(pd.to_datetime(row["date_time"]).year) 
                year = '2023' 
                try:
                    gdp = float(gdp_data.get(country_code, {}).get(year, None))
                except: 
                    gdp =None 
                return gdp    
        X["GDP"] = X.apply(get_gdp, axis=1)
        return X
        
    def extract_percentage(self,X):
        numerator_col = X[self.config.percentage_columns[1]]
        denominator_col = X[self.config.percentage_columns[0]]
        result = np.where((numerator_col == 0) | np.isnan(numerator_col), 0, (numerator_col / denominator_col) * 100)
        X['transfer_percentage'] = np.round(result, 2)

        return X
    
    def extract_lag_features(self,X): 
        lag_cols = ["total","transfer_percentage"]
        lagged_dfs = []
        X_ = X.groupby('flt_number') 
        for flght_nb, group in X.groupby('flt_number'):
                lagged_group = group.copy()
                for lag_col in lag_cols:
                    for i in range(1,4):
                        lagged_values = group[lag_col].shift(i)
                        mask = (group['flt_number'] != flght_nb) | (group['flt_number'] != group['flt_number'].shift(i))
                        mask.iloc[:i] = True  
                        lagged_values[mask] = np.nan
                        lagged_group[f'{lag_col}_lag{i}'] = lagged_values
                lagged_dfs.append(lagged_group)
        
        X = pd.concat(lagged_dfs)
        return X

         
        
            
        
   