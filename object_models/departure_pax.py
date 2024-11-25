from object_models.abstract_pax import AbstractPax;

class DeparturePax(AbstractPax):
    def __init__(self,phase):
        super().__init__(phase)

    @property 
    def type(self):
        return 'departure'
    @property
    def training_phase(self):
        return self.phase=='training' 
    @property
    def data_path(self):
        return self.config['departure_data_PATH']
    @property
    def training_result_path(self):
        return self.config['departure_result_PATH']
    @property
    def result_path(self):
        if self.training_phase:
            return self.config['departure_result_PATH']
        else:
            return self.config['departure_serving_result_PATH']
    
    @property
    def customized_path(self):
        return self.config['departure_customized_PATH']
    
    @property
    def encoder_path(self):
        return self.config['departure_encoder_path']
    
    @property
    def serving_data_path(self):
        return self.config['departure_serving_PATH']
    
    @property
    def events_detected_result_path(self):
        return self.config['departure_events_detected_PATH']
    
    def testing_pred_path(self,target):
        return self.config['departure_testing_results'][target]
    @property    
    def date_time_field(self):
        return "SOBT"
    
    @property
    def date_columns(self):
        return super().date_columns
    
    @property
    def columns(self):
        return ['FLIGHTID','SOBT', 'REGISTRATION', 'FLIGHTNUMBER', 'DESTINATIONICAO', 'AIRLINE', 'AIRCRAFTTYPEICAO', 'TRANSFER_TOTAL', 'JOINING_TOTAL', 'TOTAL_TOTAL']
   
    @property
    def renamed_columns(self):
        return ['flight_id','date_time', 'code', 'flt_number', 'destination', 'airline', 'ac_type', 'transfer', 'joining', 'total']
   
    @property 
    def distinct_column(self):
        return 'joining'


    @property
    def na_columns(self):
        return ['date_time', 'destination', 'airline','ac_type','capacity','joining', 'transfer', 'total_lag1', 'total_lag2', 'total_lag3', 'transfer_percentage_lag1', 'transfer_percentage_lag2', 'transfer_percentage_lag3']

    @property
    def columns_to_check(self):
        return ['destination']
    
    @property
    def values_to_drop(self):
        return ['LOCL', 'ZZZF', 'no data', 'None']
   
    @property
    def negative_columns(self):
        return ['joining', 'total']

    @property
    def extracted_column_names(self):
        return ['capacity', 'gdp']
 
    @property
    def percentage_columns(self):
        return ['total', 'joining', 'joining_percentage']
   
    @property
    def lag_columns(self):
        return ['total', 'joining']
   
    @property
    def categorical_columns(self):
        return ['airline', 'ac_type', 'destination']
    

    def columns_to_drop(self,target):
        if target == 'total':
            return ['flight_id','code', 'flt_number', 'transfer', 'transfer_percentage', 'joining', 'total', 'transfer_percentage_lag1', 'transfer_percentage_lag2', 'transfer_percentage_lag3']
        if target=='transfer_percentage':
            return ['flight_id','code', 'flt_number', 'transfer', 'transfer_percentage', 'joining', 'total', 'total_lag1', 'total_lag2', 'total_lag3']
    
    @property
    def prophet_model_path(self):
        return self.config["departure_prophet_model_PATH"]