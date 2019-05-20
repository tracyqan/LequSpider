# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LequItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    create_time = scrapy.Field()
    active_time = scrapy.Field()
    last_login = scrapy.Field()
    last_activity = scrapy.Field()
    area = scrapy.Field()
    signature = scrapy.Field()
    friend_nums = scrapy.Field()
    reply_times = scrapy.Field()
    theme_nums = scrapy.Field()
    identity = scrapy.Field()
    uid = scrapy.Field()
    forum_money = scrapy.Field()

class ContentItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    public_time = scrapy.Field()
    read_count = scrapy.Field()
    reply_count = scrapy.Field()