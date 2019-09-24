# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjetappartItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    prix = scrapy.Field()
    pro = scrapy.Field()
    url = scrapy.Field()
    type_bien = scrapy.Field()
    description = scrapy.Field()
    surface_bien = scrapy.Field()
    terrasse = scrapy.Field()
    garage = scrapy.Field()
    piscine = scrapy.Field()
