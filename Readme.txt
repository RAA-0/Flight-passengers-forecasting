The New_model directory contains the code for training the new prophet model that predicts the percentage change based on the events and date.
It also contains a folder (Scraping) that allows us to scrape some websites and get news based on dates.
a new file (NewPredictor) added to the serving folder of the original project is used to do a new prediction after the first model finishes its prediction, based on a predicted percentage change from the trained prophet model after scraping and searching for events based on the date.
and lastly i added some cases where i statically added some events on specific dates and made the prophet model predict on these cases in order to evaluate its performance.

The link to the percentage change prediction model alone:
https://github.com/RAA-0/Percentage_changes_predictions.git

NOTE:
- must add the original datasets to the data/FlightML folder 
-must add the configurationn (airports, aircrafts, gdp_per_capita) to the Training/json_files folder 
- the training manager was already run. we can run it again to re-build the models and encoders 
- run the serving manager 


TrainingManager.py and SevingManager.py 
1. TrainingMAnager.py
This script utilizes the DataTrainer and DataPreprocessing classes to preprocess the data and train the required models. The trained models are stored in the Training/models directory. The performance metrics (R² score and RMSE) for each model are saved in a CSV file for reference.
Note: The training process has already been executed, and the trained models, along with their evaluation metrics, are saved, as the process takes some time.
2. ServingManager.py
This script reads some samples of the datasts to serve them (reads a CSV file named to_be_predicted). It predicts the total number of passengers and the transfer percentage for the flights in the file. the predictions are stored in a CSV file in the Serving_predictions folder.
