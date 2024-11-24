import pandas as pd 
import joblib
from New_model.Training.EventExtraction import EventFeatureExtractor
from New_model.Training.Preprocessingg import PreProcessor
from object_models.pax_factory import PaxFactory

def main():
    arrival_config = PaxFactory.create_config('arrival','evaluation')
    eval_df = pd.read_csv(arrival_config.evaluation_set)
    p = EventFeatureExtractor()
    #p = PreProcessor(arrival_config)
    eval_df=eval_df.sort_values(by='ds')
    eval_df.reset_index(drop=True, inplace=True)
    #data = p.preprocess(eval_df)
    data = p.transform(eval_df)
    eval_data = data.copy()
    arrival_model = joblib.load(arrival_config.prophet_model_path)
    arrival_predictions = arrival_model.predict(data)['yhat']
    eval_data.loc[:,f'Predicted_arrival_changes']=arrival_predictions

    departure_config = PaxFactory.create_config('departure','evaluation')
    departure_model = joblib.load(departure_config.prophet_model_path)
    departure_predictions = departure_model.predict(data)['yhat']
    eval_data.loc[:,f'Predicted_departure_changes']=departure_predictions

    eval_data[arrival_config.evaluation_columns].to_csv(arrival_config.evaluation_result,index=False)
    
if __name__=='__main__':
    main()