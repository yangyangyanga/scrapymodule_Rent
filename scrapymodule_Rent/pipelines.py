# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapymodule_Rent.insert_mysql import InsertMysql

class ScrapymoduleRentPipeline(InsertMysql):
    def process_item(self, item, spider):
        sql = "insert into rent(housing_type, available_time, house_name, room_type, car_spaces, lease, address, detaile_address," \
              " supporting_facilities, price, isRent, postal_code, picture, housing_introduce, supplier_type, supplier_name, " \
              "supplier_logo, country, city, contact_name, contact_phone, contact_email, url) values(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (item["housing_type"], item["available_time"], item["house_name"], item["room_type"],item['car_spaces'],
                                      item["lease"], item["address"], item["detaile_address"], item["supporting_facilities"],
                                      item["price"], item["isRent"], item["postal_code"], item["picture"], item["housing_introduce"],
                                      item["supplier_type"], item["supplier_name"], item["supplier_logo"], item["country"], item["city"],
                                      item["contact_name"], item["contact_phone"], item["contact_email"], item["url"]))
            self.db.commit()
            print("数据插入成功")
        except Exception as e:
            self.db.rollback()
            print("数据插入失败：%s" % (str(e)))
            with open("./mysqlerror/rent.txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n========================")
        # self.close()
        return item
