import scrapy
from NewsScrapper.items import NewsItem

# Creating the Spider logic for scrapping Almassa
class NewsSpider(scrapy.Spider):
    name = "news" 
    start_urls = ['https://almassaa.com/']

    def parse(self, response):
        news_url = response.css('.qma-linke::attr(href)').getall()
        for url in news_url:
            yield response.follow(url, callback = self.parse_news)
        
        
    def parse_news(self, response):
        items = NewsItem()
        self.log(f'Got response from {response.url}')
        
        title = response.css('.post-title::text').get()
        url = response.css('link[rel="canonical"]::attr(href)').get()
        date =  response.css('.post-date span::text').get()
        category = response.css('.item-cat a::text').get()
        thumbnail =  response.css('.featured-area ::attr(src)').get()
        content =  response.css('.entry-content p::text').getall()
        
        items['title'] = title
        items['url'] = url
        items['date'] = date
        items['category'] = category
        items['thumbnail'] = thumbnail
        items['content'] = content
        yield items