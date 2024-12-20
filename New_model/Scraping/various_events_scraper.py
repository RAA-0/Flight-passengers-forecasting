from selenium.webdriver.common.by import By
from New_model.Scraping.abstract_scraper import AbstractScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

class Scraper(AbstractScraper):
    def __init__(self):
        super().__init__()

    @property
    def website_url(self):
        return 'https://www.visitdubai.com/en/whats-on/dubai-events-calendar?tags='

    def scrape_news(self):
        driver = super().get_url(self.website_url)
        count=0
        while True:
            try:
                load_more_button = driver.find_element(By.CLASS_NAME, 'load-more').find_element(By.TAG_NAME,'button')
                load_more_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "event-item"))
                )
                count+=1
                print(count)
                time.sleep(5)  

            except Exception as e:
                print("No more news or an error occurred:", e)
                break
a = Scraper()
a.scrape_news()

 