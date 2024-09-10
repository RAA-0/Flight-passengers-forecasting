from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from joblib import dump
from joblib import load
class FeaturePreProcessing:
    def __init__(self,indicator,t,config):
         self.indicator = indicator
         self.t = t
         self.config = config
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        print("encoding...")
        X = self.OneHotencoding(X)
        print("Encoding Done.")
        return X
    
    def OneHotencoding(self,X):
        if self.indicator == 'T':
            encoder = OneHotEncoder(sparse_output=False, dtype=int)
            encoded_data = encoder.fit_transform(X[self.config["cat_cols"]])
            encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(self.config["cat_cols"]), dtype=int)
            encoded_df.index = X.index
            result_df = pd.concat([X.drop(columns=self.config["cat_cols"]), encoded_df], axis=1)
            dump(encoder, f"Training\\encoders\\encoder_{self.t}.pkl")
        
        if self.indicator =='S':
            loaded_encoder = load(f"Training\\encoders\\encoder_{self.t}.pkl")
            encoded_data = loaded_encoder.transform(X[self.config["cat_cols"]])
            encoded_df = pd.DataFrame(encoded_data, columns=loaded_encoder.get_feature_names_out(self.config["cat_cols"]), dtype=int)
            encoded_df.index = X.index
            result_df = pd.concat([X.drop(columns=self.config["cat_cols"]), encoded_df], axis=1)
        return result_df
    '''
    def labelencoding(self,X):
        if self.indicator =='T':
                # Apply Label Encoding to all categorical columns
            for col in categorical_columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col])
                    #label_encoders[col] = le  # Save the encoder
                    joblib.dump(le, f'Training\\encoders\\{col}_{self.t}_label_encoder.pkl')
   

    '''
          