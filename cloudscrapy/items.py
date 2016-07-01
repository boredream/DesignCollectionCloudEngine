# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UiItem(scrapy.Item):
    # 名称
    name = scrapy.Field()

    # 图片链接
    imgUrl = scrapy.Field()

    # 描述
    desc = scrapy.Field()

    # 来源网站名称
    srcTag = scrapy.Field()

    # 源链接
    srcLink = scrapy.Field()
