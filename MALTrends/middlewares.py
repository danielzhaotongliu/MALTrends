# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
from datetime import datetime, timezone
from urllib.request import pathname2url

from scrapy import Request
from scrapy.http import Response
from scrapy.exceptions import IgnoreRequest
from scrapy import signals

class UnhandledIgnoreRequest(IgnoreRequest):
    pass

# more information of the Wayback CDX Server API at: 
# https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md

# define custom downloader middleware for wayback machine
class WaybackMachineMiddleware:
    # class variables shared by all instances
    cdx_url_template = ('http://web.archive.org/cdx/search/cdx?url={url}'
                    '&output=json&fl=timestamp,original,statuscode,digest')
    snapshot_url_template = 'http://web.archive.org/web/{timestamp}id_/{original}'
    timestamp_format = '%Y%m%d%H%M%S'

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # let Wayback Machine requests pass through without modification
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

        # set flag such that the next new request will pass through
        # the middleware unscathed and reach Wayback CDX server
        cdx_request.meta['wayback_machine_cdx_request'] = True
        return cdx_request

    def process_response(self, request, response, spider):
        # shallow copy from https://docs.scrapy.org/en/latest/topics/request-response.html
        meta = request.meta

        # parse CDX requests and schedule future snapshot requests
        if meta.get('wayback_machine_cdx_request'):
            snapshot_requests = self.build_snapshot_requests(response, meta)

            # treat empty listings as 404s
            if len(snapshot_requests) < 1:
                return Response(meta['wayback_machine_original_request'].url, status=404)

            # schedule all of the snapshots
            for snapshot_request in snapshot_requests:
                # TODO: might be unstable https://github.com/scrapy/scrapy/issues/542
                self.crawler.engine.schedule(snapshot_request, spider)

            # abort this request
            raise UnhandledIgnoreRequest

        # clean up snapshot responses
        if meta.get('wayback_machine_url'):
            return response.replace(url=meta['wayback_machine_original_request'].url)

        return response

    def build_snapshot_requests(self, response, meta):
        assert meta.get('wayback_machine_cdx_request'), 'Not a CDX request meta.'
        
        # parse the CDX snapshot data
        try:
            data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            data = []
        if len(data) < 2:
            return []
        keys, rows = data[0], data[1:]

        def build_dict(row):
            new_dict = {}
            for i, key in enumerate(keys):
                if key == 'timestamp':
                    try:
                        time = datetime.strptime(row[i], self.timestamp_format)
                        new_dict['datetime'] = time.replace(tzinfo=timezone.utc)
                    except ValueError:
                        # this means an error in the date string
                        new_dict['datetime'] = None
                new_dict[key] = row[i]
            return new_dict

        snapshots = list(map(build_dict, rows))
        snapshots = self.filter_snapshots(snapshots)

        # construct the requests
        snapshot_requests = []
        for snapshot in snapshots:
            # update the url to point to the snapshot
            url = self.snapshot_url_template.format(**snapshot)
            original_request = meta['wayback_machine_original_request']
            snapshot_request = original_request.replace(url=url)

            # attach extension specify metadata to the request
            snapshot_request.meta.update({
                'wayback_machine_original_request': original_request,
                'wayback_machine_url': snapshot_request.url,
                'wayback_machine_time': snapshot['datetime'],
            })

            snapshot_requests.append(snapshot_request)

        return snapshot_requests

    def filter_snapshots(self, snapshots):
        pass


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
