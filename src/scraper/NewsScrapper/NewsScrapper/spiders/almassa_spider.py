import scrapy
from ..items import NewsItem

# Creating the Spider logic for scrapping Almassa
class NewsSpider(scrapy.Spider):
    name = "news" 
    start_urls = ['https://almassaa.com/%D8%A7%D9%84%D9%82%D9%8A%D8%A7%D8%AF%D8%A9-%D8%A7%D9%84%D8%B9%D9%84%D9%8A%D8%A7-%D9%84%D9%84%D9%85%D9%86%D8%B7%D9%82%D8%A9-%D8%A7%D9%84%D8%AC%D9%86%D9%88%D8%A8%D9%8A%D8%A9-%D8%A8%D8%A3%D9%83%D8%A7/']

    def parse(self, response):
        items = NewsItem()
        self.log(f'Got response from {response.url}')
        
        title = response.css('.post-title::text').get(),
        url = response.css('link[rel="canonical"]::attr(href)').get()
        date =  response.css('.post-date span::text').get(),
        category = response.css('.item-cat a::text').get(),
        thumbnail =  response.css('.featured-area ::attr(src)').get(),
        content =  response.css('.entry-content p::text').getall(),
        
        items['title'] = title
        items['url'] = url
        items['date'] = date
        items['category'] = category
        items['thumbnail'] = thumbnail
        items['content'] = content
        yield items