import scrapy
import requests

class ScoreSpider(scrapy.Spider):
    name = 'score_spider'
    
    def start_requests(self):
        pass
        
    def parse(self, response):
        pass