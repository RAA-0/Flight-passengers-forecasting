from New_model.Scraping.confernces_scraping import ConferenceScraping
from New_model.Scraping.disruptions_scraper import DisruptionsScraper
from New_model.Scraping.global_health_scraper import GlobalHealthScraper
from New_model.Scraping.sports_scraper import SportsScraper

class SFactory:
    @staticmethod
    def create_config(config_type):
        if config_type == "health":
            return GlobalHealthScraper()
        elif config_type == "disruption":
            return DisruptionsScraper()
        elif config_type == "sports":
            return SportsScraper()
        elif config_type == "conference":
            return ConferenceScraping()
        
        else:
            return None 