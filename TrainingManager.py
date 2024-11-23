import pandas as pd
import json
from Training.DataPreprocessing import DataPreProcessor
from Training.DataTrainer import DataTrain
from object_models.pax_factory import PaxFactory

        
def main():
    for flighttype in ['arrival','departure']:
        config = PaxFactory.create_config(flighttype,'training')
        data = pd.read_csv(config.data_path,index_col=False,parse_dates= config.date_columns)

        preprocessor = DataPreProcessor(config)
        transformed_data=preprocessor.preprocess(data)
        transformed_data = pd.read_csv(config.result_path)
    
        trainer = DataTrain(config,transformed_data)
        trainer.start_training()

if __name__ == "__main__":
    main()


        



