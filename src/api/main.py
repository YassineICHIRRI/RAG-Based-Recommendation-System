from fastapi import FastAPI, HTTPException
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os

app = FastAPI()

# Set the Scrapy settings module
os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.scraper.NewsScrapper.settings'
runner = CrawlerRunner()

@app.get("/scrape/")
async def scrape_news():
    """
    Endpoint to trigger the scraping process.
    """
    try:
        deferred = runner.crawl("news")  # Matches the spider name
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)  # Avoids signal issues with FastAPI
        return {"status": "Scraping completed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
