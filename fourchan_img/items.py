# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    identityhash = scrapy.Field()


class ImageMongoItem(scrapy.Item):
    postnum = scrapy.Field()
    datetime = scrapy.Field()
    imgurl = scrapy.Field()
    identityhash = scrapy.Field()
    filenamehash = scrapy.Field()
