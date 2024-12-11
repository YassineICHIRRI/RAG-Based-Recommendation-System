from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

def run_spider(spider_name: str):
    """
    Run the Scrapy spider with the specified name.
    """
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.scraper.NewsScrapper.settings'  
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name)
    process.start()

if __name__ == "__main__":
    run_spider("news")
