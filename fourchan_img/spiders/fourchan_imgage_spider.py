# -*- coding: utf-8 -*-
import scrapy
import hashlib
from fourchan_img.items import ImageMongoItem


class FourchanImgageSpiderSpider(scrapy.Spider):
    name = 'fourchan_image_spider'
    allowed_domains = ['4chan.org']
    start_urls = ['http://4chan.org/']

    def parse(self, response):
        for board in response.css("li a::attr(href) ").re(r"boards\.4chan\.org\/[a-z]{1,}"):
            page = 1

            while (page < 10):
                page += 1
                yield scrapy.Request(url="http://" + board + "/" + str(page), callback=self.parse_board)

    def parse_board(self, response):
        # iterate through threads
        board_short = response.css("title::text").re(r"\/[a-z]{1,}\/")

        for thread in response.css("span.summary a::attr(href)").extract():
            yield scrapy.Request(url="http://boards.4chan.org" + board_short[0] + thread, callback=self.parse_thread)

    def parse_thread(self, response):
        currentboard = response.css("div.boardTitle::text").extract_first()

        counter = 0

        # iterate through posts (using enumerate might be better)
        for post in response.css("div.postContainer"):
            postnum = post.css("span.postNum a::text").extract()
            datetime = post.css("span.dateTime::text").extract_first()
            posttext = post.css("blockquote.postMessage::text").extract_first()

            imgurls = response.css("div.fileText a::attr(href)").re(r"i\.4cdn\.org\/[a-z]{1,}\/[0-9]{1,}\.[a-z]{1,3}")
            complete_image = "http://" + imgurls[counter]

            tohash = str(currentboard) + str(datetime) + str(posttext)
            hobject = hashlib.sha256(tohash.encode())

            filenamehash = hashlib.sha1(str(complete_image).encode())

            # some metainfo for the image
            img_mongo_db = ImageMongoItem()
            img_mongo_db['postnum'] = postnum[1]
            img_mongo_db['datetime'] = datetime
            img_mongo_db['imgurl'] = complete_image
            img_mongo_db['identityhash'] = str(hobject.hexdigest())
            img_mongo_db['filenamehash'] = str(filenamehash.hexdigest())

            counter += 1

            yield img_mongo_db
            yield {'image_urls': [complete_image]}
