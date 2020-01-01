# -*- coding: utf-8 -*-
import scrapy
from jinse.items import JinseItem


class JinseArticleSpider(scrapy.Spider):
    name = 'jinse-article'
    allowed_domains = ['jinse.com']
    start_urls = [
        'https://www.jinse.com/member/255249',
    ]

    def start_requests(self):
        # get start_urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        author = response.xpath(".//div[@class='member-info']/p[@class='member-name']/text()").get()
        for index, sel in enumerate(response.xpath(".//div[@class='article-main']/ol[@class='clear list']")):
            item = JinseItem()
            item['title'] = sel.xpath(".//a[@class='article-img']/@title").get()
            if item['title'] is not None:
                item['title'] = str.strip(item['title'])

            item['source_url'] = sel.xpath(".//a[@class='article-img']/@href").get()
            if item['source_url'] is not None:
                item['source_url'] = str.strip(item['source_url'])

            item['cover_url'] = sel.xpath(".//a[@class='article-img']/img/@src").get()
            if item['cover_url'] is not None:
                item['cover_url'] = str.strip(item['cover_url'])

            item['excerpt'] = sel.xpath("//ul/h3/following-sibling::li[1]/text()")[index].get()
            if item['excerpt'] is not None:
                item['excerpt'] = str.strip(item['excerpt'])

            if author is not None:
                item['author'] = str.strip(author)

            print (item)
