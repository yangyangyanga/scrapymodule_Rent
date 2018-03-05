# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapymoduleRentItem(scrapy.Item):
    housing_type = scrapy.Field()
    available_time = scrapy.Field()
    house_name = scrapy.Field()
    room_type = scrapy.Field()
    car_spaces = scrapy.Field()
    lease = scrapy.Field()
    address = scrapy.Field()
    detaile_address = scrapy.Field()
    supporting_facilities = scrapy.Field()
    price = scrapy.Field()
    isRent = scrapy.Field()
    postal_code = scrapy.Field()
    picture = scrapy.Field()
    housing_introduce = scrapy.Field()
    supplier_type = scrapy.Field()
    supplier_name = scrapy.Field()
    supplier_logo = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    contact_name = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_email = scrapy.Field()
    url = scrapy.Field()
