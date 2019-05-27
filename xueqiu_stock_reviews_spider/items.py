# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XueqiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    item = scrapy.Field()

class item(scrapy.Item):
    title = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    href = scrapy.Field()
    author = scrapy.Field()
