# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImageItem(scrapy.Item):
    # Image downloading fields (for ImagesPipeline)
    image_urls = scrapy.Field()
    images = scrapy.Field()

    # Metadata
    postnum = scrapy.Field()
    datetime = scrapy.Field()
    imgurl = scrapy.Field()
    identityhash = scrapy.Field()
    filenamehash = scrapy.Field()
    board = scrapy.Field()
    thread_url = scrapy.Field()
