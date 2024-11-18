from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from joblib import dump
from joblib import load
class FeaturePreProcessing:
    def __init__(self,config):
         self.config = config
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        print("encoding...")
        X = self.OneHotencoding(X)
        print("Encoding Done.")
        return X
    
    def OneHotencoding(self,X):
        if self.config.training_phase:
            print("training phase...")
            encoder = OneHotEncoder(sparse_output=False, dtype=int,handle_unknown='ignore')
            encoded_data = encoder.fit_transform(X[self.config.categorical_columns])
            encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(self.config.categorical_columns), dtype=int)
            encoded_df.index = X.index
            result_df = pd.concat([X.drop(columns=self.config.categorical_columns), encoded_df], axis=1)
            dump(encoder, self.config.encoder_path)
        
        else:
            loaded_encoder = load(self.config.encoder_path)
            encoded_data = loaded_encoder.transform(X[self.config.categorical_columns])
            encoded_df = pd.DataFrame(encoded_data, columns=loaded_encoder.get_feature_names_out(self.config.categorical_columns), dtype=int)
            encoded_df.index = X.index
            result_df = pd.concat([X.drop(columns=self.config.categorical_columns), encoded_df], axis=1)
        return result_df

          