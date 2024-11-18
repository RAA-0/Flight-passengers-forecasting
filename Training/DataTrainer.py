from sklearn.model_selection import train_test_split
import pandas as pd 
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import joblib

class DataTrain:
    def __init__(self, config,data):
        self.config =config 
        self.data = data 
        self.type = self.config.type
    
    def start_training(self):
        targets = ['total','transfer_percentage']
        for target in targets:
            X_train, X_test, y_train, y_test,flight_id_train, flight_id_test  = self.split_data(target)
            y_pred = self.lgb_model1(X_train,X_test,y_train,y_test,target)
            self.evaluate_model(X_test,y_test,y_pred,flight_id_test,target)
    
    
    def split_data(self, target):
        flight_ids = self.data["flight_id"]
        y = self.data[target]
        X = self.data.drop(columns =self.config.columns_to_drop(target))

        X_train, X_test, y_train, y_test,flight_id_train, flight_id_test  = train_test_split(
            X, y,flight_ids, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test, flight_id_train, flight_id_test


    def lgb_model1(self,X_train, X_test, y_train, y_test,target):
        print("Building the model....")
    
        params = {
                'boosting_type': 'gbdt',
                'objective': 'regression',
                'metric': {'l2_root'},
                'train_metric': 'true',
                'num_leaves': 150,
                'max_depth': -1,
                'learning_rate': 0.01,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'bagging_freq': 4,
                'verbose': 0}
        print('training the model...')
        train_data = lgb.Dataset(X_train, label=y_train)

        valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

        num_round = 1000
        bst = lgb.train(
                params,
                train_data,
                num_round,
                valid_sets=[valid_data],
            )
        joblib.dump(bst, f'Training\\models\\lightgbm_model_{target}_{self.type}1.pkl')
        
        bst= joblib.load(f'Training\\models\\lightgbm_model_{target}_{self.type}1.pkl')
        y_pred = bst.predict(X_test, num_iteration=bst.best_iteration)
        return y_pred
    
    def evaluate_model(self, X_test, y_test,y_pred, flight_id_test,target):
        print("Evaluating the model....")
        y_pred = [max(0, pred) for pred in y_pred]
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, y_pred)
        print(f"Target: {self.config.type}_{target} :\n RMSE_testing: {rmse}, R-squared_testing: {r2}")
        self.save_predictions_perfomance(flight_id_test,X_test,y_test,y_pred,rmse,r2,target)
    
    def save_predictions_perfomance(self,flight_id_test,X_test,y_test,y_pred,rmse,r2,target):
        X_test_df = pd.DataFrame(X_test, columns=X_test.columns)
        predictions_df = pd.DataFrame({'flight_id':flight_id_test,f'{target}': y_test, f'Predicted_{target}': y_pred})
        predictions_df = pd.concat([predictions_df, X_test_df], axis=1)
        #predictions_df.to_csv(f'data\\testing_pred\\{target}_{self.type}_predictions.csv', index=False)
        performance_metrics = {'target':target,
            'R²': r2,
            'RMSE': rmse}
        metrics_df = pd.DataFrame([performance_metrics])
        #metrics_df.to_csv(f'Training\\models\\{target}_{self.type_performance_metrics.csv', index=False)
 