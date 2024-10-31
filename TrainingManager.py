import pandas as pd
import json
from Training.DataPreprocessing import DataPreProcessor
from Training.DataTrainer import DataTrain

"""it uses the DataTrainer and DataPreprocessing to build and save the models and predictions"""
        
def main():
    for config in extract_config():
        data = pd.read_csv(config["path"],index_col=False,parse_dates= config['date_columns'])
        #Preprocess the data 
        processor = DataPreProcessor(config)
        transformed_data=processor.process(data,"T") #indicator for training phase
            
        #Training the models 
        trainer = DataTrain(config,transformed_data)

        #build a model for both targets 
        trainer.lgb_model1()
        #trainer.lgb_model2() #both gave the same answer 

        #train and evaluate each model 
        trainer.train_and_evaluate()

def extract_config():
    with open("config.json",'r') as f:
        config = json.load(f)
    dep_config = config.get("departure_config",{})
    arriv_config =config.get("arrival_config",{})
    return [arriv_config,dep_config]

if __name__ == "__main__":
    main()


        



