# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class XueqiuStockReviewsSpiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="mydb",
            user="root",
            passwd="password",
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, items, spider):
        print(items)
        for item in items["item"]:
            # print(item)
            sql = "INSERT INTO comment(title, detail, time, href, code, author) VALUES(%s,%s,%s,%s,%s,%s)"
            try:
                self.cursor.execute(sql, (item['title'], item['detail'], item['time'], item['href'], items['code'], item['author']))
                self.cursor.connection.commit()
            except BaseException as e:
                print(e)
                print("相关评论已经存在")
                self.connect.rollback()
        return items
