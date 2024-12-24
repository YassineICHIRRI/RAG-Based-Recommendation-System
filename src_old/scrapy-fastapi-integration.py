from fastapi import FastAPI
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
import scrapy
from typing import Dict
import crochet
import logging
from twisted.internet.defer import inlineCallbacks

# Initialize crochet
crochet.setup()

app = FastAPI()

class ExampleSpider(scrapy.Spider):
    name = 'example_spider'
    
    def __init__(self, url=None, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.items = []
    
    def parse(self, response):
        item = {
            'title': response.css('h1::text').get(),
            'content': response.css('h2::span::text').getall(),
            'url': response.url
        }
        self.items.append(item)
        return item

class SpiderRunner:
    def __init__(self):
        self.items = []
        self.settings = get_project_settings()
        # Add settings to handle common issues
        self.settings.update({
            'ROBOTSTXT_OBEY': True,
            'USER_AGENT': 'Mozilla/5.0 (compatible; MyBot/1.0)',
            'DOWNLOAD_TIMEOUT': 15,
            'CONCURRENT_REQUESTS': 1
        })
        self.crawler = CrawlerRunner(self.settings)

    def spider_results(self, signal, sender, item, response, spider):
        self.items.append(item)

    @crochet.run_in_reactor
    @inlineCallbacks
    def crawl(self, spider_cls, url):
        self.items = []
        dispatcher.connect(self.spider_results, signal=signals.item_passed)
        
        try:
            yield self.crawler.crawl(spider_cls, url=url)
        except Exception as e:
            logging.error(f"Crawler error: {str(e)}")
            raise e
        
        return self.items

@app.post("/scrape/")
async def scrape(url: str):
    try:
        runner = SpiderRunner()
        # Use normal function call since crochet handles the async part
        results = runner.crawl(ExampleSpider, url)
        # Wait for the results with a timeout
        try:
            scraped_data = results.wait(timeout=30)
            return {
                "status": "success",
                "data": scraped_data,
                "url": url
            }
        except crochet.TimeoutError:
            return {
                "status": "error",
                "message": "Scraping timed out after 30 seconds",
                "url": url
            }
    except Exception as e:
        logging.error(f"Scraping error: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "url": url
        }
