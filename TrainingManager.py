import pandas as pd
import json
from Training.DataPreprocessing import DataPreProcessor
from Training.DataTrainer import DataTrain

"""it uses the DataTrainer and DataPreprocessing to build and save the models and predictions"""
        
def main():
    for config in extract_config():
        data = pd.read_csv(config["path"],index_col=False,parse_dates= config['date_columns'])
        #Preprocess the data 
        #preprocessor = DataPreProcessor(config)
        #transformed_data=preprocessor.preprocess(data,"T") #indicator for training phase
        transformed_data = pd.read_csv('data\\Transformed_data\\Transformed_arrival.csv')
    
        trainer = DataTrain(config,transformed_data)
        trainer.start_training()

def extract_config():
    with open("config.json",'r') as f:
        config = json.load(f)
    dep_config = config.get("departure_config",{})
    arriv_config =config.get("arrival_config",{})
    return [arriv_config]

if __name__ == "__main__":
    main()


        



