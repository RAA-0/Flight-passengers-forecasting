from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from New_model.Scraping.abstract_scraper import AbstractScraper
from New_model.Scraping.Sports_.fixingSportsNewsForm import FormFixer
import json 
import time
import random 
import pandas as pd 
import ast 

class SportsScraper(AbstractScraper):
    def __init__(self):
       super().__init__("sports")

    def get_url(self,url):
        driver = super().get_url(url)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept"))
            )
            accept_button.click()
        except Exception as e:
            print("No cookie consent pop-up found or couldn't click the button:", e)
        time.sleep(random.uniform(2,5))
        return driver 

    
    def scrape_news(self):
        news=[]
        year_lists = defaultdict(lambda:defaultdict(defaultdict))
        urls = self.website_url
        for url in urls: 
            driver = self.get_url(url)
            lists = driver.find_elements(By.TAG_NAME,"p")
            
            for list in lists:
                news.append(list.text)
            
            news = [event for event in news if ("|" in event)&("Jump to" not in event)]        
        
            with open(self.file_path,"w") as w:
                json.dump(news,w,indent=4)

    def run(self):
        self.scrape_news()
    
    def fix_form(self):
        ff=FormFixer(self.file_path,self.df_path)
        ff.run()
    def detect_event(self,date):
        print("sports news detection...")
        def get_event(df,date_):
            events_on_day = []
            #year = date_.year
            #month = date_.month
            #day = date_.day
            matching_rows = df[ (pd.to_datetime(df['date']) == pd.to_datetime(date_))]
            if not matching_rows.empty:
                sport_event = matching_rows.iloc[0]['event']
                sport_event = ast.literal_eval(sport_event)  
                for event in sport_event:
                    for key, value in self.config[self.event]['impactful_event'].items():
                        if all(word in event.lower() for word in key):
                            events_on_day.append(value)
            else: events_on_day=[]
            return events_on_day 
        df = pd.read_csv(self.df_path)
        #df['date'] = pd.to_datetime(df[['year', 'month','day']])
        df['date']=pd.to_datetime(df['date'])
        max_date = df['date'].max()
        date = pd.to_datetime(date)
        if date<=max_date:
            events_on_day = get_event(df,date)
        else:
            self.run()
            events_on_day = get_event(df,date)
        return events_on_day
            