import json
class AbstractPax:
    def __init__(self,phase):
        self.read_config_file()
        self.phase = phase 
    
    @property
    def data_path(self):
        return self._data_path
    
    @property
    def result_path(self):
        return self.result_path
    
    @property
    def customized_path(self):
        return self.customized_path
    
    @property
    def encoder_path(self):
        return self.encoder_path
    
    @property
    def aircraft_json_path(self):
        return self.config['aircraft_JSON_PATH']
    @property
    def airport_json_path(self):
        return self.config['airports_JSON_PATH']
    
    @property
    def gdp_json_path(self):
        return self.config['gdp_JSON_PATH']
    
    @property
    def date_time_field(self):
        return self._date_time_field
    
    @property
    def date_columns(self):
        return ['SIBT', 'EIBT', 'AIBT','SOBT', 'EOBT', 'AOBT']
    
    @property
    def columns(self):
        return []

    @property
    def renamed_columns(self):
        return []

    @property
    def illogical_order_cols(self):
        return []
    
    @property
    def na_columns(self):
        return []
  
    @property
    def columns_to_check(self):
        return []
    
    @property
    def values_to_drop(self):
        return []
   
    @property
    def negative_columns(self):
        return []
    
    @property
    def extracted_column_names(self):
        return []
 
    @property
    def percentage_columns(self):
        return []
    
    @property
    def encoding_method(self):
        return "onehot_encoding"
   
    @property
    def lag_columns(self):
        return []
    
    @property
    def categorical_columns(self):
        return []
    
    @property
    def dependent_variables(self):
        return []

    @property
    def use_encoder_model(self):
        return False
 
    @property
    def pareto_percentage(self):
        return 0.3
   
    @property
    def na_to_0_columns(self):
        return ["transfer"]
    
    @property
    def columns_to_keep(self):
        if self.phase == 'serving':
            return ['flight_id','ds','event','total','predicted_total','capacity']
        if self.phase =='evaluation':
            return ['ds','event']


    @property
    def evaluation_set(self):
        return self.config['prophet_evaluation_data_PATH']
    
    @property
    def evaluation_result(self):
        return self.config['prophet_evaluation_results_PATH']
    
    @property
    def evaluation_columns(self):
        return ['ds','event','Predicted_arrival_changes','Predicted_departure_changes']
    
    def read_config_file(self):
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        self.config = data
