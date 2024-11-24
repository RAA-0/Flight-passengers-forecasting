from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from New_model.Scraping.abstract_scraper import AbstractScraper
import time 
import random 
from collections import defaultdict
import json 
import pandas as pd
import ast 

class DiwaliScraper(AbstractScraper):
    def __init__(self):
        super().__init__("diwali")
         
    def run (self,years):
        new_data = self.scrape_news(years)

    def scrape_news(self, years):
        new_df = pd.read_csv(self.df_path)
        for year in years:
            driver =super().get_url(self.website_url+str(year))
            date_cards = driver.find_elements(By.CLASS_NAME,"dpEventCard")
            for date_card in date_cards:
                day= date_card.find_element(By.CLASS_NAME,"dpEventDay").text
                month_year = date_card.find_element(By.CLASS_NAME,"dpSmallDate").text
                day = day.split("t")[0]
                day = day.split('s')[0]
                day = day.split('n')[0]
                day = day.split('r')[0]
                month_year = month_year.split(" ")
                df = pd.DataFrame({'year':[month_year[1]],'month':[self.mapping[month_year[0][:3]]],'day':[day]})
                new_df = pd.concat([new_df,df])
            
        new_df.to_csv(self.df_path,index=False)
        return new_df
              
    def detect_event(self,date_input):
        print("diwali detection....")
        events =[]
        df = pd.read_csv(self.df_path)
        date_input = pd.to_datetime(date_input)
        year = date_input.year
        month = date_input.month
        day = date_input.day
        def get_event():
            events =[]
            matching_rows = df[(df['year'].astype(int) == year) & (df['month'].astype(int)== month) & (df['day'].astype(int)== day) ]
            if not matching_rows.empty:
                events.append('diwali')

            return events

        df['date'] = pd.to_datetime(df[['year', 'month','day']])
        df['date']=pd.to_datetime(df['date'])
        max_date = df['date'].max()
        if year<=max_date.year:
            events = get_event()
        else:
            self.run([year])
            events = get_event()
        
        return events



