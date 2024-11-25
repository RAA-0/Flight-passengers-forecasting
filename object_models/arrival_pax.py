from object_models.abstract_pax import AbstractPax;

class ArrivalPax(AbstractPax):
    def __init__(self,phase):
        super().__init__(phase)

    @property
    def type(self):
        return 'arrival'
    
    @property
    def training_phase(self):
        return self.phase=='training' 
    
    @property
    def data_path(self):
        return self.config['arrival_data_PATH']
    
    @property
    def training_result_path(self):
        return self.config['arrival_result_PATH']

    @property
    def result_path(self):
        if self.training_phase:
            return self.config['arrival_result_PATH']
        else:
            return self.config['arrival_serving_result_PATH']

    @property
    def customized_path(self):
        return self.config['arrival_customized_PATH']

    @property
    def encoder_path(self):
        return self.config['arrival_encoder_path']
    
    @property
    def serving_data_path(self):
        return self.config['arrival_serving_PATH']
    
    @property
    def events_detected_result_path(self):
        return self.config['arrival_events_detected_PATH']
    
    def testing_pred_path(self,target):
        return self.config['arrival_testing_results'][target]
    
    @property    
    def date_time_field(self):
        return "SIBT"
    
    @property
    def date_columns(self):
        return super().date_columns
    
    @property
    def columns(self):
        return ['FLIGHTID','SIBT', 'REGISTRATION', 'FLIGHTNUMBER', 'ORIGINICAO', 'AIRLINE', 'AIRCRAFTTYPEICAO', 'TRANSFER_TOTAL', 'DISEMBARKING_TOTAL', 'TOTAL_TOTAL']
   
    @property
    def renamed_columns(self):
        return ['flight_id','date_time', 'code', 'flt_number', 'origin', 'airline', 'ac_type', 'transfer', 'disembarking', 'total']
    
    @property
    def distinct_column(self):
        return 'disembarking'
   
    @property
    def na_columns(self):
        return ['date_time', 'origin', 'airline', 'ac_type','capacity','GDP','disembarking','transfer']

    @property
    def columns_to_check(self):
        return ['origin', 'GDP']
    
    @property
    def values_to_drop(self):
        return ['LOCL', 'ZZZF', 'no data', 'None']
   
    @property
    def negative_columns(self):
        return ['disembarking', 'total']

    @property
    def extracted_column_names(self):
        return ['capacity', 'gdp']
 
    @property
    def percentage_columns(self):
        return ['total', 'transfer', 'transfer_percentage']
   
    @property
    def lag_columns(self):
        return ['total', 'transfer']
   
    @property
    def categorical_columns(self):
        return ['airline', 'ac_type', 'origin']
    
    def columns_to_drop(self,target):
        if target == 'total':
            return ['flight_id','code', 'flt_number', 'transfer', 'transfer_percentage', 'disembarking', 'total','transfer_percentage_lag1','transfer_percentage_lag2','transfer_percentage_lag3']
        if target=='transfer_percentage':
            return ['flight_id','code', 'flt_number', 'transfer', 'transfer_percentage', 'disembarking', 'total','total_lag1','total_lag2','total_lag3']

    @property
    def prophet_model_path(self):
        return self.config["arrival_prophet_model_PATH"]