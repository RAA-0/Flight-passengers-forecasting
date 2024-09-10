
import joblib  
import pandas as pd
from Training.DataPreprocessing import DataPreProcessor
from Training.DataTrainer import DataTrain
import json


"""it works by providing it with a csv file of flights you'd like to predict their values """
        
def main():
    for config in extract_config():
        data = pd.read_csv(config["path"],index_col=False,parse_dates= config['date_columns'])
        training_data = pd.read_csv(config["result_path"],index_col=False)
        data.sort_values(by=config['index'])
        serving_data = data.tail(100)

        #Preprocess the data 
        processor = DataPreProcessor(config)
        transformed_data=processor.process(serving_data,"S")
        transformed_data = new_lag_features(training_data,transformed_data)
            

        #loading the models and predicting
            
        data_predictions = transformed_data.copy()
        copy = transformed_data.copy()
        for target in ["total","transfer_percentage"]:
            model_path = f"Training\\models\\lightgbm_model_{target}_{config['type']}1.pkl"
            model = joblib.load(model_path)
            transformed_data = copy.drop(columns=config[f"columns_to_drop_{target}"])
            predictions = model.predict(transformed_data)
            data_predictions[f'Predicted_{target}'] = predictions
        data_predictions.to_csv(f"Serving_predictions\\{config['type']}_pred.csv",index = False)
        print("done")
def extract_config():
    with open("config.json",'r') as f:
        config = json.load(f)
    dep_config = config.get("departure_config",{})
    arriv_config =config.get("arrival_config",{})
    return [dep_config,arriv_config]    

def new_lag_features(training_data,prediction_dataset):
    num_lags = [1, 2, 3]
    new_rows = []

    for index, row in prediction_dataset.iterrows():
        filtered_df = training_data[training_data['flt_number'] == row['flt_number']]
        sorted_df = filtered_df.sort_index(ascending=False)
        new_row = dict(row)
        for lag_col in ["total","transfer_percentage"]:
            for lag in num_lags:
                new_row[f'{lag_col}_lag{lag}'] = sorted_df.head(lag)[lag_col].values[lag-1]
            new_rows.append(new_row)

    prediction_dataset = pd.DataFrame(new_rows)
    prediction_dataset.columns = training_data.columns
    return prediction_dataset    

         
if __name__ == "__main__":
    main()







        



