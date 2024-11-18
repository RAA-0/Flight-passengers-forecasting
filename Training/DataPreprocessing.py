from Training.data_preprocessing.Cleaner import Cleaner
from Training.data_preprocessing.CustomizeData import CustomizeData
from Training.data_preprocessing.FeatureExtractor import FeatureExtractor
from Training.data_preprocessing.FeaturePreProcessing import FeaturePreProcessing
from sklearn.pipeline import Pipeline 
from feature_engine.datetime import DatetimeFeatures
import pandas as pd

class DataPreProcessor:
    def __init__(self,config):
        self.config = config

    def preprocess(self, data):
        dtf = DatetimeFeatures(
          variables="date_time",
          features_to_extract=[
              "year",
              "month",
              "hour",
              "day_of_month",
              "weekend",
          ],
      )
        
        pipeline = Pipeline([
            ("Customizing Data", CustomizeData(self.config)),
            ("Feature Engineering", FeatureExtractor(self.config)),
            ("Cleaning Data", Cleaner(self.config)),
            ("datetime_features", dtf),
            ("PreProcessing Data", FeaturePreProcessing(self.config)),
        ])

        transformed_data = pipeline.fit_transform(data)
        transformed_data.to_csv(self.config.result_path,index = False)
        
        print("PREprocessing done!")    
        return transformed_data
        