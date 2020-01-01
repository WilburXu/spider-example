# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JinseItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    excerpt = scrapy.Field()
    source_url = scrapy.Field()
    content = scrapy.Field()
    cover_url = scrapy.Field()
