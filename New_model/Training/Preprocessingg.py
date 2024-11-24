import json
from feature_engine.pipeline import Pipeline
from New_model.Training.EventDetection import EventDetector
from New_model.Training.EventExtraction import EventFeatureExtractor

class PreProcessor:
    def __init__(self,config):
        self.config = config 


    def preprocess(self,data):
        pipeln = Pipeline([("Event Detection",EventDetector(self.config)),
                          ("Feature Extraction",EventFeatureExtractor())])
        transformed_data = pipeln.fit_transform(data)

        return transformed_data