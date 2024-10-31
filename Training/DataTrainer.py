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
        self.type = self.config['type']


    def split_data(self, target):
    
        y = self.data[target]
        X = self.data.drop(columns = self.config[f'columns_to_drop_{target}'])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        
        
        return X_train, X_test, y_train, y_test


    def lgb_model1(self):
        for target in self.config['Target']:
            X_train, X_test, y_train, y_test = self.split_data(target)
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

        return bst
    
    def lgb_model2(self):
        
        for target in self.config['Target']:
            X_train, X_test, y_train, y_test = self.split_data(target)
                          
            # Train LightGBM model
            model = lgb.LGBMRegressor(
                metric = self.config[target]['metric'],
                random_state=self.config['random_state'],
                learning_rate=self.config[target]['learning_rate'],
                boosting_type=self.config[target]['boosting_type'],
                #n_estimators=self.config[target]['n_estimators'],
                #colsample_bytree= self.config[target]['feature_fraction'],
                #min_split_gain=self.config[target]['min_gain_to_split'],
                max_depth=self.config[target]['max_depth'],
                num_leaves=self.config[target]['num_leaves'],
                #min_child_samples=self.config[target]['min_child_samples'],
                #reg_alpha = self.config[target]['lambda_l1'],
                #reg_lambda = self.config[target]['lambda_l2'],
                force_col_wise= True,
                #bagging_fraction = self.config[target]['bagging_fraction'],
                #bagging_freq = self.config[target]['bagging_freq'],
                #verbose = self.config[target]['verbose']
                )
            lgbm= model.fit(X_train, y_train)
        
            joblib.dump(lgbm, f'Training\\models\\lightgbm_model_{target}_{self.type}2.pkl')

        return lgbm
    
    def random_forest_model(self):
        X_train, X_test, y_train, y_test = self.split_data("Total")
        # Train Random Forest model
        model = RandomForestRegressor(
            n_estimators=self.config['n_estimators'], 
            random_state=self.config['random_state']
        )
        rf=model.fit(X_train, y_train)
        joblib.dump(rf, 'Training\\models\\RandomForest_model_{target}_{self.type}.pkl')

        return model
    
    
    def train_and_evaluate(self):

        targets = self.config['Target']
        for target in targets :
            
            #model = joblib.load(f"Training\\models\\lightgbm_model_{target}_{self.type}2.pkl")
            model = joblib.load(f"Training\\models\\lightgbm_model_{target}_{self.type}1.pkl")
            X_train, X_test, y_train, y_test = self.split_data(target)
            
            self.evaluate_model(model, X_test, y_test,X_train,y_train,target)
            
    
    def evaluate_model(self, model, X_test, y_test,X_train,y_train,target):
        ''' 
       #used this to check the training to see if there is oversampling 
        print(f"Training set evaluation: ")
        y_pred_train = model.predict(X_train)
        mse_training = mean_squared_error(y_train, y_pred_train)
        rmse_training = mse_training ** 0.5
        r2_training = r2_score(y_train, y_pred_train)

        print(f"For training Target: {target}:\n RMSE_training: {rmse_training}, R-squared_training: {r2_training}")
        '''

        # Make predictions on the testing set 
        y_pred = model.predict(X_test)
        y_pred = [max(0, pred) for pred in y_pred]

        # calculate r2 and rmse
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, y_pred)
        print(f"Target: {self.config['type']}_{target} :\n RMSE_testing: {rmse}, R-squared_testing: {r2}")

        lgb.plot_importance(model, max_num_features=5)
        plt.show()

        self.save_predictions_perfomance(y_test,y_pred,rmse,r2,target)
    
    def save_predictions_perfomance(self,y_test,y_pred,rmse,r2,target):
        # Store predictions in a CSV
        predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
        predictions_df.to_csv(f'data\\training_pred\\{target}_{self.type}_predictions.csv', index=False)

        # Store performance metrics in a JSON or CSV
        performance_metrics = {
            'R²': r2,
            'RMSE': rmse}
        #save performance metrics in a CSV
        metrics_df = pd.DataFrame([performance_metrics])
        metrics_df.to_csv(f'Training\\models\\{target}_{self.type}_performance_metrics.csv', index=False)

 