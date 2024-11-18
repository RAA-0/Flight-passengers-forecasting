from New_model.event_type_model.news_event import NewsEvent
from New_model.event_type_model.religious_event import ReligiousEvent
import pandas as pd 


class EventDetector:
    def __init__(self,config):
        self.config = config
        self.news_event = NewsEvent()
        self.recurrent_event = ReligiousEvent()

    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        event_list=[]
        classes = [self.recurrent_event,self.news_event]
        for _,row in X.iterrows():
            event=[]
            for event_config in classes:
                event.extend(event_config.detect_event(pd.to_datetime(row['ds'])))
            event_list.append(event)
        X['event']=event_list
        X[self.config.columns_to_keep].to_csv(self.config.events_detected_result_path,index=False)
        return X[self.config.columns_to_keep]
        
