# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_splash import SplashRequest
from dynamic_scraper.spiders.django_spider import DjangoSpider
from blog.models import Post, PostSite, PostItem


class PostSpider(DjangoSpider):
    name = 'post_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(PostSite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Post
        self.scraped_obj_item_class = PostItem
        super(PostSpider, self).__init__(self, *args, **kwargs)

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
