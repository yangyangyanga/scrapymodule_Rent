import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from scrapymodule_Rent.clearSpace import clear_space, clear_space_str
from scrapymodule_Rent.getItem import get_item
# from scrapymodule.getTuition_fee import getTuition_fee
from scrapymodule_Rent.items import ScrapymoduleRentItem

class RentSpider(scrapy.Spider):
    name = "rent"
    start_urls = ["https://www.realestate.com.au/rent/in-sydney+cbd,+nsw/list-1"]

    for i in range(2, 20):
        url = "https://www.realestate.com.au/rent/in-sydney+cbd,+nsw/list-" + str(i)
        start_urls.append(url)
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        # print(response.url)
        links = response.xpath("//article//div[@class='listingInfo rui-clearfix']/div/h2[@class='rui-truncate']/a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # print(len(links))
        for link in links:
            url = "https://www.realestate.com.au" + link
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleRentItem)
        item['country'] = 'Australia'
        item['url'] = response.url
        print("===========================")
        print(response.url)
        try:
            # housing_type
            housing_type = response.xpath("//div[@id='listing_info']/ul[@class='info']/li[@class='property_info']/span[@class='propertyType']//text()").extract()
            clear_space(housing_type)
            item['housing_type'] = ''.join(housing_type)
            # print("item['housing_type']: ", item['housing_type'])

            # available_time
            available_time = response.xpath(
                "//div[@id='listing_info_secondary']/div[@class='available_date']/span//text()").extract()
            clear_space(available_time)
            item['available_time'] = ''.join(available_time)
            # print("item['available_time']: ", item['available_time'])

            # house_name
            house_name = response.xpath(
                "//div[@id='description']/p[@class='title']//text()").extract()
            clear_space(house_name)
            item['house_name'] = ''.join(house_name)
            # print("item['house_name']: ", item['house_name'])

            # room_type
            # lease
            # address
            address = response.xpath(
                "//div[@id='listing_address']/h1/span[@class='detail-address']//text()").extract()
            clear_space(address)
            item['address'] = ','.join(address)
            # print("item['address']: ", item['address'])

            # detaile_address   //div[@id='description']/h3[@class='address']
            detaile_address = response.xpath(
                "//div[@id='description']/h3[@class='address']//text()").extract()
            clear_space(detaile_address)
            item['detaile_address'] = ''.join(detaile_address)
            # print("item['detaile_address']: ", item['detaile_address'])

            # supporting_facilities
            supporting_facilities = response.xpath(
                "//div[@id='description']/p[@class='body']//text()").extract()
            clear_space(supporting_facilities)
            item['supporting_facilities'] = ''.join(supporting_facilities)
            # print("item['supporting_facilities']: ", item['supporting_facilities'])

            # price
            price = response.xpath(
                "//div[@id='listing_info']/ul[@class='info']/li[@class='price']/p[@class='priceText']//text()").extract()
            clear_space(price)
            item['price'] = ''.join(price)
            # print("item['price']: ", item['price'])

            # isRent
            # postal_code
            # picture
            picture = response.xpath(
                "//div[@id='mainPhoto']/div[@class='hero-image__image-wrapper']/a[@class='hero-image__link']/img[@class='hero-image__image']/@src").extract()
            clear_space(picture)
            item['picture'] = ''.join(picture)
            # print("item['picture']: ", item['picture'])

            # housing_introduce
            # supplier_type
            # supplier_name
            supplier_name = response.xpath(
                "//div[@class='branding-banner-content']/a/img[@class='logo']/@alt").extract()
            clear_space(supplier_name)
            item['supplier_name'] = ''.join(supplier_name)
            print("item['supplier_name']: ", item['supplier_name'])

            # supplier_logo //div[@class='branding-banner-content']/a/img[@class='logo']/@src
            supplier_logo = response.xpath(
                "//div[@class='branding-banner-content']/a/img[@class='logo']/@src").extract()
            clear_space(supplier_logo)
            item['supplier_logo'] = ''.join(supplier_logo)
            print("item['supplier_logo']: ", item['supplier_logo'])

            # contact_name
            contact_name = response.xpath(
                "//div[@class='agentContactInfo']/p//text()").extract()
            clear_space(contact_name)
            item['contact_name'] = ','.join(contact_name)
            print("item['contact_name']: ", item['contact_name'])

            # contact_phone
            contact_phone = response.xpath(
                "//div[@class='agentContactInfo']/ul/li/text()").extract()
            clear_space(contact_phone)
            item['contact_phone'] = ','.join(contact_phone)
            print("item['contact_phone']: ", item['contact_phone'])

            # contact_email

            # print(item)
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

