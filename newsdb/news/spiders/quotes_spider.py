import logging

import scrapy
from news.items import NewsItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        # 'https://www.8btc.com/author/14582',
        # 'https://www.8btc.com/author/46580',
        # 'https://www.8btc.com/author/47298',
        # 'https://www.8btc.com/author/48414',
        # 'https://www.8btc.com/author/49436',
        # 'https://www.8btc.com/author/3708',
        # 'https://www.8btc.com/author/48414',
        # 'https://www.8btc.com/author/14244',
        # 'https://www.8btc.com/author/4',
        # 'https://www.8btc.com/author/10094',
        # 'https://www.8btc.com/author/27334',
        # 'https://www.8btc.com/author/42945',
        # 'https://www.8btc.com/author/7965',
        # 'https://www.8btc.com/author/36907',
        # 'https://www.8btc.com/author/55654',
        # 'https://www.8btc.com/author/52104',
        # 'https://www.8btc.com/author/40165',
        # 'https://www.8btc.com/author/58671',
        # 'https://www.8btc.com/author/45694',
        # 'https://www.8btc.com/author/59058',
        # 'https://www.8btc.com/author/60082',
        # 'https://www.8btc.com/author/59750',
        # 'https://www.8btc.com/author/59850',
        # 'https://www.8btc.com/author/58835',
        # 'https://www.8btc.com/author/56566',
        # 'https://www.8btc.com/author/63692',
        # 'https://www.8btc.com/author/61087',
        # 'https://www.8btc.com/author/56794',
        # 'https://www.8btc.com/author/63797',
        # 'https://www.8btc.com/author/62171',
        # 'https://www.8btc.com/author/59344',
        # 'https://www.8btc.com/author/57035',
        # 'https://www.8btc.com/author/61038',
        # 'https://www.8btc.com/author/58928',
        # 'https://www.8btc.com/author/59329',
        # 'https://www.8btc.com/author/60751',
        # 'https://www.8btc.com/author/36068',
        # 'https://www.8btc.com/author/60097',
        # 'https://www.8btc.com/author/36520',
        # 'https://www.8btc.com/author/54271',
        # 'https://www.8btc.com/author/55206',
        # 'https://www.8btc.com/author/55873',
        # 'https://www.8btc.com/author/49226',
        # 'https://www.8btc.com/author/45691',
        # 'https://www.8btc.com/author/35864',
        # 'https://www.8btc.com/author/50919',
        # 'https://www.8btc.com/author/48261',
        # 'https://www.8btc.com/author/58269',
        'https://www.8btc.com/author/57476',
    ]

    def __init__(self):
        self.mysqlObj = None

    def start_requests(self):
        # get start_urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, meta={"useSel": True}, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath("//div[@class='article-item-warp']"):
            item = NewsItem()

            item['title'] = sel.xpath(".//div[@class='article-item__body']/h3/a/text()").get()
            if item['title'] is not None:
                item['title'] = str.strip(item['title'])

            item['source_url'] = response.urljoin(sel.xpath(".//div[@class='article-item__body']/h3/a/@href").get())
            if item['source_url'] is not None:
                item['source_url'] = str.strip(item['source_url'])

            item['cover_url'] = sel.xpath(".//div[@class='article-item__thumb']/a/img/@src").get()
            if item['cover_url'] is not None:
                item['cover_url'] = str.strip(item['cover_url'])

            item['excerpt'] = sel.xpath(".//div[@class='article-item__content']/text()").get()
            if item['excerpt'] is not None:
                item['excerpt'] = str.strip(item['excerpt'])

            item['author'] = sel.xpath(".//div[@class='article-item__author']/a[2]/text()").get()
            if item['author'] is not None:
                item['author'] = str.strip(item['author'])

            # check title & author not empty
            if (item['title'] is None) or (item['author'] is None) or (item['cover_url'] is None):
                continue

            # check crawlInfo exists
            crawlInfo = self.mysqlObj.get_post_info(title=item['title'], author=item['author'])
            if crawlInfo is not None:
                logging.info("author: %s title: %s is exists" % (item['author'], item['title']))
                continue

            yield scrapy.Request(url=item['source_url'], meta={"item": item, "useSel": False}, callback=self.parse_content)

    def parse_content(self, response):
        item = response.meta['item']
        item['publish_time'] = str.strip(response.xpath("//div[@class='header__info']/span/time/text()").get())
        item['content'] = response.xpath("//div[@class='bbt-html']").get()
        yield item
