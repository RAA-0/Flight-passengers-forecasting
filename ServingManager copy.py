import pandas as pd 
import joblib
from New_model.Training.EventExtraction import EventFeatureExtractor

def main():
    p = EventFeatureExtractor()
    df = pd.read_csv('eval.csv')
    df=df.sort_values(by='ds')
    df.reset_index(drop=True, inplace=True)
    data=p.transform(df)

    events = ["corona","ramadan_season","hajj_season","new_years_eve","eid_al_adha","christmas_season"]
    #data_with_events = data[data['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events))]
    #data_with_events = data_with_events.copy()
    #data_without_events = data[~(data['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events)))]
    #data_without_events = data_without_events.copy()
    #data_with_events.reset_index(drop=True, inplace=True)
    #data_without_events.reset_index(drop=True,inplace=True)
    for target in ['arrival','departure']:
        #data_without_events.loc[:,f'Predicted_{target}_changes']=0
        model = joblib.load(f'New_model\\models\\prophet_{target}_model.joblib')
        predictions = model.predict(data)['yhat']
        data.loc[:,f'Predicted_{target}_changes']=predictions
    #df_ = pd.concat([data_with_events,data_without_events])
    #df_=df_.sort_values(by='ds')
    data[['ds','event','Predicted_arrival_changes','Predicted_departure_changes']].to_csv('eval_results.csv',index=False)
    
if __name__=='__main__':
    main()