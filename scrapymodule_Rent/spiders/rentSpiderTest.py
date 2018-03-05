from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapymodule_Rent.clearSpace import clear_space
from scrapymodule_Rent.getItem import get_item
from scrapymodule_Rent.items import ScrapymoduleRentItem
import re

class RentSpiderTest(CrawlSpider):
    name = 'rentTest'
    # start_urls = ["https://www.realestate.com.au/rent/in-sydney,+nsw+2000/list-1"]
    # start_urls = ["https://www.realestate.com.au/rent/in-brisbane+-+greater+region,+qld/list-1"]
    # start_urls = ["https://www.realestate.com.au/rent/in-adelaide,+sa+5000/list-1"]
    # start_urls = ["https://www.realestate.com.au/rent/in-melbourne,+vic+3000/list-1"]
    # start_urls = ["https://www.realestate.com.au/rent/in-canberra+-+greater+region,+act/list-1"]
    start_urls = ["https://www.realestate.com.au/rent/in-perth+-+greater+region,+wa/list-1"]

    rules = (
        # Rule(page_link, callback='get_programme_link', follow=True),
        # Rule(LinkExtractor(allow=r'/list\-\d+'), follow=True, callback='test'),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='results']/div[@class='resultCtrls rui-clearfix'][1]/div[@class='checkboxP']/ul[@class='linkList horizontalLinkList pagination']/li[@class='nextLink']/a"), follow=True, callback='testpage'),
        Rule(LinkExtractor(restrict_xpaths="//article//div[@class='listingInfo rui-clearfix']/div/h2[@class='rui-truncate']/a"), follow=False, callback='testdetail'),
    )

    # def parse_start_url(self, response):
    #     print("", response.url)
    # def test(self, response):
    #     print("test: ============", response.url)
    # def testpage(self, response):
    #     print("testpage: ============",response.url)

    def testdetail(self, response):
        item = get_item(ScrapymoduleRentItem)
        item['country'] = 'Australia'
        item['city'] = 'Perth'
        item['url'] = response.url
        print("===========================")
        print(response.url)
        try:
            # housing_type
            housing_type = response.xpath(
                "//div[@id='listing_info']/ul[@class='info']/li[@class='property_info']/span[@class='propertyType']//text()").extract()
            clear_space(housing_type)
            item['housing_type'] = ''.join(housing_type)
            print("item['housing_type']: ", item['housing_type'])

            # available_time
            available_time = response.xpath(
                "//div[@id='listing_info_secondary']/div[@class='available_date']/span//text()").extract()
            clear_space(available_time)
            # print("available_time: ", available_time)
            available_timeDict = {"Jan": "01",
                                    "Feb": "02",
                                    "Mar": "03",
                                    "Apr": "04",
                                    "May": "05",
                                    "Jun": "06",
                                    "Jul": "07",
                                    "Aug": "08",
                                    "Sep": "09",
                                    "Oct": "10",
                                    "Nov": "11",
                                    "Dec": "12",}
            if available_time[0] == "Available Now":
                item['available_time'] = 'now'
            else:
                available_timetmp = available_time[0].split(" ")[-1]
                # print(available_timetmp)
                available_timetmp1 = available_timetmp.split("-")
                # print("available_timetmp1: ====", available_timetmp1)
                available_timeResult = "20" + available_timetmp1[-1] + "-" + available_timeDict[available_timetmp1[1]] + "-" + available_timetmp1[0]
                item['available_time'] = available_timeResult
            # print("item['available_time']: ", item['available_time'])

            # house_name
            house_name = response.xpath(
                "//div[@id='description']/p[@class='title']//text()").extract()
            clear_space(house_name)
            item['house_name'] = ''.join(house_name)
            # print("item['house_name']: ", item['house_name'])

            # room_type
            room_typeCarspaces = response.xpath(
                "//div[@id='features']/div/div[@class='featureList']/ul[1]/li//text()").extract()
            clear_space(room_typeCarspaces)
            # print("room_typeCarspaces: ", room_typeCarspaces)
            if item['housing_type'] == "Studio":
                item['room_type'] = 'Studio'
            else:
                room_type = ''
                if "Bedrooms:" in room_typeCarspaces:
                    room_typeIndex1 = room_typeCarspaces.index("Bedrooms:")
                    room_type1 = room_typeCarspaces[room_typeIndex1+1]
                    room_type = room_type1
                if "Bathrooms:" in room_typeCarspaces:
                    room_typeIndex2 = room_typeCarspaces.index("Bathrooms:")
                    room_type2 = room_typeCarspaces[room_typeIndex2+1]
                    room_type = room_type + "-" + room_type2
                item['room_type'] = room_type
            # print("item['room_type']: ", item['room_type'])

            if "Garage Spaces:" in room_typeCarspaces:
                carIndex = room_typeCarspaces.index("Garage Spaces:")
                item['car_spaces'] = room_typeCarspaces[carIndex+1]
            elif "Open Car Spaces:" in room_typeCarspaces:
                carIndex = room_typeCarspaces.index("Open Car Spaces:")
                item['car_spaces'] = room_typeCarspaces[carIndex+1]
            # print("item['car_spaces']: ", item['car_spaces'])


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

            opentime = response.xpath("//a[@itemprop='events']//text()").extract()
            opentime = ' '.join(opentime)
            if len(opentime) != 0:
                opentimePrefixx = response.xpath("//div[@id='inspectionTimes']/h3//text()").extract()
                clear_space(opentimePrefixx)
                opentime = ''.join(opentimePrefixx) + opentime
            # supporting_facilities
            housing_introduce = response.xpath(
                "//div[@id='description']/p[@class='body']//text()").extract()
            clear_space(housing_introduce)
            feacture = response.xpath(
                "//div[@id='features']//text()").extract()
            clear_space(feacture)
            floorplans = response.xpath(
                "//div[@id='floorplans']//text()").extract()
            clear_space(floorplans)
            housing_introduce = opentime + ' '.join(housing_introduce) + ''.join(feacture) + ''.join(floorplans)
            item['housing_introduce'] = housing_introduce
            # print("item['housing_introduce']: ", item['housing_introduce'])

            # price
            price = response.xpath(
                "//div[@id='listing_info']/ul[@class='info']/li[@class='price']/p[@class='priceText']//text()").extract()
            clear_space(price)
            item['price'] = ''.join(price)
            # print("item['price']: ", item['price'])

            # isRent
            # postal_code
            # picture
            pictureJs = response.xpath("//script").extract()
            # print("pictureJs: ", pictureJs)
            pictureJsStr = ''.join(pictureJs)
            pictureSrc = re.findall(r'{src:\"[\w\/\.]*jpg\"', pictureJsStr)
            # print("pictureSrc:========== ", pictureSrc)
            # print(len(pictureSrc))
            for index in range(len(pictureSrc)):
                pictureSrc[index] = pictureSrc[index].strip('{src:').strip('"')
                pictureSrc[index] = "https://i3.au.reastatic.net/800x600-resize,extend,r=33,g=40,b=46" + pictureSrc[index]
            # print("pictureSrc:==========11 ", pictureSrc)
            item['picture'] = ';'.join(pictureSrc)
            # print("item['picture']: ", item['picture'])

            # housing_introduce
            # supplier_type
            # supplier_name
            supplier_name = response.xpath(
                "//div[@id='agentInfoExpanded']/div/a/img[@class='logo']/@alt|//div[@id='agentInfoExpanded']/div[1]/text()").extract()
            clear_space(supplier_name)
            item['supplier_name'] = ''.join(supplier_name)
            # print("item['supplier_name']: ", item['supplier_name'])

            # supplier_logo //div[@class='branding-banner-content']/a/img[@class='logo']/@src
            supplier_logo = response.xpath(
                "//div[@id='agentInfoExpanded']/div/a/img[@class='logo']/@src").extract()
            clear_space(supplier_logo)
            item['supplier_logo'] = ''.join(supplier_logo)
            # print("item['supplier_logo']: ", item['supplier_logo'])

            # contact_name
            contact_name = response.xpath(
                "//div[@class='agentContactInfo'][1]/p//text()").extract()
            clear_space(contact_name)
            if len(contact_name) != 0:
                item['contact_name'] = contact_name[0]
            print("item['contact_name']: ", item['contact_name'])

            # contact_phone
            contact_phone = response.xpath(
                "//div[@class='agentContactInfo']/ul/li/text()").extract()
            clear_space(contact_phone)
            if len(contact_phone) != 0:
                item['contact_phone'] = contact_phone[0]
            print("item['contact_phone']: ", item['contact_phone'])

            # contact_email

            # print(item)
            yield item
        except Exception as e:
            with open("./error/rentSpider.txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)


