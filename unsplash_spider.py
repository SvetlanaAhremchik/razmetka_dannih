import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from unsplash_scraper.items import UnsplashImageItem


class UnsplashSpider(CrawlSpider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/s/photos/nature']

    rules = (
        Rule(LinkExtractor(allow=r"/photos/.+"), callback='parse_image', follow=True),
        Rule(LinkExtractor(allow=r"/s/photos/"), follow=True),
    )

    def parse_image(self, response):
        item = UnsplashImageItem()
        item['image_url'] = response.css('img[src*="fit"]:first-child::attr(src)').get(default='').strip()
        item['title'] = response.css('h1::text').get(default='Untitled').strip()
        url_parts = response.url.split('/')
        item['category'] = url_parts[4] if len(url_parts) > 4 else 'Unknown'

        yield item