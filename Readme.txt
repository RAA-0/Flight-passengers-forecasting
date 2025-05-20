Aviation Passenger Forecasting with Event-Based Adjustment

This project forecasts aviation passenger numbers using a two-step approach:

- Baseline Model: A LightGBM model predicts the expected number of passengers for each flight.

- Event-Based Adjustment: For each flight date, an automated web scraping system collects news about external events (e.g., pandemics, sports events, political happenings) that could impact passenger numbers. These extracted events are used as additional features for a Prophet model, which predicts the percentage change to adjust the baseline forecast accordingly. This combined approach improves prediction accuracy by considering external factors.

Project Structure:

- TrainingManager.py
Uses DataTrainer and DataPreprocessing classes to preprocess data and train both models.
Trained models are saved under Training/models/.
Performance metrics (R² score and RMSE) for each model are stored in a CSV file for reference.

Note: The training process is time-consuming and has already been completed. The saved models and evaluation metrics are available in the repository.

- ServingManager.py
Loads sample datasets from a CSV file named to_be_predicted.csv.
Predicts total passengers and transfer percentage for the listed flights.
Saves predictions to CSV files in the Serving_predictions/ folder.

- New_model Directory
Contains code for training the Prophet model that predicts percentage changes based on extracted events and flight dates.
Includes a Scraping/ folder for automated web scraping of news articles based on dates.
The NewPredictor.py file (added to the serving folder) adjusts the baseline model’s predictions by applying the percentage change predicted by the Prophet model after event extraction.

Additional Features
Added static test cases with manually specified events on certain dates to evaluate the Prophet model’s prediction performance.

