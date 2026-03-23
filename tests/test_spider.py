import os
import unittest
import hashlib
from scrapy.http import HtmlResponse
from fourchan_img.spiders.fourchan_image_spider import FourchanImgageSpiderSpider
from fourchan_img.items import ImageItem

class MockSettings:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict
    def getlist(self, name):
        return self.settings_dict.get(name, [])
    def get(self, name, default=None):
        return self.settings_dict.get(name, default)

class FourchanSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = FourchanImgageSpiderSpider()
        self.spider.settings = MockSettings({
            'BOARDS': ['v'],
            'MAX_PAGES_PER_BOARD': 1
        })

    def _get_response_from_file(self, filename, url='https://boards.4chan.org/v/thread/123456789'):
        path = os.path.join(os.path.dirname(__file__), 'responses', filename)
        with open(path, 'rb') as f:
            content = f.read()
        return HtmlResponse(url=url, body=content, encoding='utf-8')

    def test_start_requests(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, 'https://boards.4chan.org/v/1')

    def test_parse_thread(self):
        response = self._get_response_from_file('thread.html')
        results = list(self.spider.parse_thread(response))

        # We expect 1 item because one post has an image, one doesn't
        self.assertEqual(len(results), 1)
        item = results[0]

        self.assertIsInstance(item, ImageItem)
        self.assertEqual(item['postnum'], '123456789')
        self.assertEqual(item['datetime'], '03/22/26(Sun)12:00:00')
        # The boardTitle in thread.html is "/v/ - Video Games"
        self.assertEqual(item['board'], '/v/ - Video Games')
        self.assertEqual(item['imgurl'], 'https://i.4cdn.org/v/123456789.jpg')
        
        # Verify hashes are SHA-256 (length 64)
        self.assertEqual(len(item['identityhash']), 64)
        self.assertEqual(len(item['filenamehash']), 64)

if __name__ == '__main__':
    unittest.main()
