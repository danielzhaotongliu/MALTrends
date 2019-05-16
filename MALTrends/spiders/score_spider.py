import scrapy
import requests
import locale
from datetime import datetime

class ScoreSpider(scrapy.Spider):
    name = 'score_spider'

    def start_requests(self):
        r = requests.get('https://api.jikan.moe/v3/anime/%s' % self.id)
        data = r.json()
        anime_urls = [
            data['url'],
            'https://myanimelist.net/anime/%s' % self.id
        ]
        for url in anime_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # did not use yield since generators can cause undefined behaviour
        # https://amir.rachum.com/blog/2017/03/03/generator-cleanup/
        stats = {}
        try:
            score = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
            score_count = response.xpath('//span[@itemprop="ratingCount"]/text()').get()
            stats['score'] = float(score)
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            stats['score_count'] = locale.atoi(score_count)
        except:
            pass
        
        if len(stats) > 0:
            stats['timestamp'] = response.meta['wayback_machine_time'].timestamp()
            return stats
            