import scrapy
import requests

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
        items = []
        print response.css('')
        # for div in response.css('div')
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
