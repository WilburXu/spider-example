import logging

import scrapy
from news.items import NewsItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        "https://www.8btc.com/author/57476",
        "https://www.8btc.com/author/4",
    ]

    def __init__(self):
        self.mysqlObj = None

    def start_requests(self):
        # get start_urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath("//div[@class='article-item-warp']"):
            item = NewsItem()

            item['title'] = sel.xpath(".//div[@class='article-item__body']/h3/a/text()").get()
            if item['title'] is not None:
                item['title'] = str.strip(item['title'])

            item['source_url'] = response.urljoin(sel.xpath(".//div[@class='article-item__body']/h3/a/@href").get())
            if item['source_url'] is not None:
                item['source_url'] = str.strip(item['source_url'])

            item['excerpt'] = sel.xpath(".//div[@class='article-item__content']/text()").get()
            if item['excerpt'] is not None:
                item['excerpt'] = str.strip(item['excerpt'])

            item['cover_url'] = response.urljoin(sel.xpath(".//div[@class='article-item__body']/h3/a/@href").get())
            if item['cover_url'] is not None:
                item['cover_url'] = str.strip(item['cover_url'])

            item['author'] = sel.xpath(".//div[@class='article-item__author']/a[2]/text()").get()
            if item['author'] is not None:
                item['author'] = str.strip(item['author'])

            # check crawlInfo exists
            crawlInfo = self.mysqlObj.get_post_info(title=item['title'], author=item['author'])
            if crawlInfo is not None:
                logging.info("author: %s title: %s is exists" % (item['author'], item['title']))
                continue

            yield scrapy.Request(url=item['source_url'], meta={"item": item, "useSel": False}, callback=self.parse_content)

    def parse_content(self, response):
        item = response.meta['item']
        item['publish_time'] = str.strip(response.xpath("//div[@class='header__info']/span/time/text()").get())
        # item['author'] = str.strip(response.xpath("//div[@class='header__info']/span/a/text()").get())
        item['content'] = response.xpath("//div[@class='bbt-html']").get()
        yield item


