import json 

class WeatherFeaturesExtractor():

    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self

    def transform(self,X):
       X = self.extract_weather_features(X)
       return X


    def extract_weather_features(self,X): 
        with open ('Training\\Json_files\\new_weather.json','r') as w:
            data = json.load(w)
        pressure= []
        temperature=[]
        wind_speed = []

        for index,row in X.iterrows():
            year = str(row['date_time_year'])
            month = str(row['date_time_month']).zfill(2)
            day = str(row["date_time_day_of_month"]).zfill(2)
            time = str(row["date_time_hour"]).zfill(2)
            if time in data[year][month][day]:  #there are certain times that don't have data 
                pressure.append(float(data[year][month][day][time].get("Pressure",None)))
                temperature.append(int(data[year][month][day][time].get("Temperature",None)))
                wind_speed.append(int(data[year][month][day][time].get("Wind Speed",None)))
            else:
                #i tried to fill their values with previous time since they don't quite differ
                '''
                new_time =str(int(time) - 1).zfill(2)
                pressure.append(float(data[year][month][day][new_time].get("Pressure",None)))
                temperature.append(int(data[year][month][day][new_time].get("Temperature",None)))
                wind_speed.append(int(data[year][month][day][new_time].get("Wind Speed",None)))
                '''
                #and i tried to leave them as missing values 
                pressure.append(None)
                temperature.append(None)
                wind_speed.append(None)

        X["pressure"] = pressure
        X["temperature"] = temperature
        X["wind_speed"] = wind_speed

        return X
        