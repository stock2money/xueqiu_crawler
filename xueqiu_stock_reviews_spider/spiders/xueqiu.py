# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import time
from scrapy.http import Request
from xueqiu_stock_reviews_spider.items import XueqiuItem, item
import requests
import json

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    xueqiu_url = 'https://xueqiu.com/'
    review_urls = []
    codes = []
    comment_url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={symbol}&hl=0&source=user&sort=time&page=1&q={q}'


    def __init__(self):
        info = pd.read_csv("data/stocks.csv", header=0, delimiter=",")
        self.codes = info["code"]
        for code in info["code"]:
            if code[-5:] == "XSHE":
                code = "SZ" + code[:-5]
            else:
                code = "SH" + code[:-5]
            url = self.comment_url.format(symbol=code, q=code)
            self.review_urls.append(url)

    # 用start_requests()方法,代替start_urls
    def start_requests(self):  
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(self.xueqiu_url, meta={'cookiejar': 1}, callback=self.parse)]

    def parse(self, response):
        for i, url in enumerate(self.review_urls):
            request = scrapy.Request(url=url, meta={'cookiejar':response.meta['cookiejar']}, callback=self.parseHref)
            request.meta['code'] = self.codes[i]
            yield request


    def parseHref(self, response):
        code = response.meta['code']
        items = XueqiuItem()
        items["code"] = code
        items["item"] = []
        stocks_comment = json.loads(response.text)['list']
        for stock in stocks_comment:
            comment = item()
            try:
                comment["detail"] = stock.get('text').strip()
                comment["href"] = stock.get('source_link').strip()
                comment["author"] = stock.get('user').get('screen_name').strip()
                ts = int(stock.get('created_at')) / 1000
                comment["time"] = "发布与 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                if stock.get('title') == None:
                    comment["title"] = comment["author"] + "的行情评论"
                else:
                    comment["title"] = stock.get('title').strip()
                items["item"].append(comment)
            except BaseException as e:
                print(e)
        yield items

