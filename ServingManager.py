
import joblib  
import pandas as pd
from Training.DataPreprocessing import DataPreProcessor
from Training.DataTrainer import DataTrain
import json
from object_models.pax_factory import PaxFactory
from serving.serving_data import DataServer
from serving.NewPredictor2 import NewPredictor
from New_model.Training.Preprocessingg import PreProcessor

        
def main():
    for flighttype in ['arrival','departure']:
        serving_config = PaxFactory.create_config(flighttype,'serving')
        serving_data = pd.read_csv(serving_config.serving_data_path,index_col=False,parse_dates= serving_config.date_columns)
        training_data = pd.read_csv(serving_config.training_result_path,index_col=False)
        serving_data.sort_values(by=serving_config.date_time_field)

        processor = DataPreProcessor(serving_config)
        transformed_data=processor.preprocess(serving_data)  
        transformed_data = new_lag_features(training_data,transformed_data)

        server = DataServer(serving_config,transformed_data)
        df = server.serve()

        df['ds'] = pd.to_datetime({'year': df['date_time_year'], 'month': df['date_time_month'], 'day':df['date_time_day_of_month']})
        
        p = PreProcessor(serving_config)
        df = p.preprocess(df)

        new_predictor = NewPredictor(df,serving_config)
        new_predictor.start_new_prediction()
        
        print("done")

def new_lag_features(training_data,prediction_dataset):
    num_lags = [1, 2, 3]
    new_rows = []

    for index, row in prediction_dataset.iterrows():
        filtered_df = training_data[training_data['flt_number'] == row['flt_number']]
        sorted_df = filtered_df.sort_index(ascending=False)
        new_row = dict(row)
        for lag_col in ["total","transfer_percentage"]:
            for lag in num_lags:
                if len(sorted_df) >= lag:
                    new_row[f'{lag_col}_lag{lag}'] = sorted_df.head(lag)[lag_col].values[lag-1]
                else:
                    new_row[f'{lag_col}_lag{lag}'] = None
        new_rows.append(new_row)

    prediction_dataset = pd.DataFrame(new_rows)
    prediction_dataset.columns = training_data.columns
    return prediction_dataset    

         
if __name__ == "__main__":
    main()







        



