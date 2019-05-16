# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
from datetime import datetime as dt
from urllib.request import pathname2url

from scrapy import Request
from scrapy.http import Response
from scrapy.exceptions import IgnoreRequest
from scrapy import signals

# define custom downloader middleware for wayback machine
class WaybackMachineMiddleware:
    # class variables shared by all instances
    cdx_url_template = ('http://web.archive.org/cdx/search/cdx?url={url}'
                    '&output=json&fl=timestamp,original,statuscode,digest')
    snapshot_url_template = 'http://web.archive.org/web/{timestamp}id_/{original}'

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # let Wayback Machine requests pass through
        if request.meta.get('wayback_machine_url'):
            return
        if request.meta.get('wayback_machine_cdx_request'):
            return
        # otherwise request a CDX listing of available snapshots
        return self.build_cdx_request(request)

    def build_cdx_request(self, request):
        cdx_url = self.cdx_url_template.format(url=pathname2url(request.url))
        cdx_request = Request(cdx_url)
        cdx_request.meta['wayback_machine_original_request'] = request
        cdx_request.meta['wayback_machine_cdx_request'] = True
        return cdx_request

    def process_response(self, request, response, spider):
        meta = request.meta

        # parse CDX requests and schedule future snapshot requests
        if meta.get('wayback_machine_cdx_request'):
            snapshot_requests = self.build_snapshot_requests(response, meta)

            # treat empty listings as 404s
            if len(snapshot_requests) < 1:
                return Response(meta['wayback_machine_original_request'].url, status=404)

            # schedule all of the snapshots
            for snapshot_request in snapshot_requests:
                self.crawler.engine.schedule(snapshot_request, spider)

            # abort this request
            raise UnhandledIgnoreRequest

        # clean up snapshot responses
        if meta.get('wayback_machine_url'):
            return response.replace(url=meta['wayback_machine_original_request'].url)

        return response

class MaltrendsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaltrendsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
