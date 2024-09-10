NOTE:
You have to add a folder called data that contains the following :
- data/FlightML that contains the original datasets
- data/training_pred 
- data/customized_data
- data/Transformed_data 


TrainingManager.py and SevingManager.py 
1. TrainingMAnager.py
This script utilizes the DataTrainer and DataPreprocessing classes to preprocess the data and train the required models. The trained models are stored in the Training/models directory. The performance metrics (R² score and RMSE) for each model are saved in a CSV file for reference.
Note: The training process has already been executed, and the trained models, along with their evaluation metrics, are saved, as the process takes some time.
2. ServingManager.py
This script reads some samples of the datasts to serve them (reads a CSV file named to_be_predicted). It predicts the total number of passengers and the transfer percentage for the flights in the file. the predictions are stored in a CSV file in the Serving_predictions folder.