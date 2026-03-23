# -*- coding: utf-8 -*-
import scrapy
import hashlib
from fourchan_img.items import ImageItem

class FourchanImgageSpiderSpider(scrapy.Spider):
    name = 'fourchan_image_spider'
    allowed_domains = ['4chan.org', '4cdn.org']

    def start_requests(self):
        try:
            boards = self.settings.getlist('BOARDS')
            if not boards:
                boards = ['v', 'pol'] # Defaults
            max_pages = int(self.settings.get('MAX_PAGES_PER_BOARD', 2))
        except Exception as e:
            self.logger.error(f"Error reading settings: {e}")
            boards = ['v']
            max_pages = 1

        for board in boards:
            board = board.strip().lstrip('/')
            if not board:
                continue
            board_url = f"https://boards.4chan.org/{board}"
            for page in range(1, max_pages + 1):
                yield scrapy.Request(
                    url=f"{board_url}/{page}", 
                    callback=self.parse_board,
                    errback=self.handle_error
                )

    def parse(self, response):
        # This is no longer used as we override start_requests
        pass

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url} - {failure.value}")

    def parse_board(self, response):
        # Extract board title/shortname
        board_match = response.css("title::text").re(r"\/[a-z0-9]{1,}\/")
        board_short = board_match[0] if board_match else "unknown"

        # Find threads
        threads = response.css("span.summary a::attr(href)").extract()
        if not threads:
            # Fallback for boards without summaries or different layout
            threads = response.css("div.thread a.replylink::attr(href)").extract()

        for thread_path in threads:
            thread_url = response.urljoin(thread_path)
            yield scrapy.Request(
                url=thread_url, 
                callback=self.parse_thread,
                errback=self.handle_error
            )

    def parse_thread(self, response):
        currentboard = response.css("div.boardTitle::text").extract_first() or "unknown"

        for post in response.css("div.postContainer"):
            try:
                # Defensive extraction of post number
                postnum_info = post.css("span.postNum a::text").extract()
                if len(postnum_info) > 1:
                    postnum = postnum_info[1]
                elif postnum_info:
                    postnum = postnum_info[0]
                else:
                    postnum = "unknown"
                
                # Check for image link - skip if no image
                file_link = post.css("div.fileText a::attr(href)").extract_first()
                if not file_link:
                    continue

                # Ensure image URL is absolute and valid
                complete_image = response.urljoin(file_link)
                if not complete_image.startswith('http'):
                    self.logger.warning(f"Invalid image URL found in {response.url}: {complete_image}")
                    continue

                # Defensive metadata extraction
                datetime = post.css("span.dateTime::text").extract_first() or "unknown"
                posttext = "".join(post.css("blockquote.postMessage ::text").extract()).strip()

                # Generate secure hashes for internal tracking/deduplication
                tohash = f"{currentboard}{datetime}{posttext}{postnum}"
                identityhash = hashlib.sha256(tohash.encode()).hexdigest()
                filenamehash = hashlib.sha256(complete_image.encode()).hexdigest()

                item = ImageItem()
                item['postnum'] = postnum
                item['datetime'] = datetime
                item['imgurl'] = complete_image
                item['identityhash'] = identityhash
                item['filenamehash'] = filenamehash
                item['image_urls'] = [complete_image]
                item['board'] = currentboard
                item['thread_url'] = response.url

                yield item
            except Exception as e:
                self.logger.error(f"Error parsing post in {response.url}: {e}", exc_info=True)
                continue
