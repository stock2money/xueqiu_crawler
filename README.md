# 雪球股票评论爬取

> ```
> https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={symbol}&hl=0&source=user&sort=time&page={page}&_={real_time}
> ```



## Environment

- Python3 + Scrapy + MySQL



## Usage

```
# xinlang_stock_reviews_spider

scrapy crawl xueqiu
```



## Note

* 相应股票评论只爬取前十条
* 关于`cookies`相关，直接爬取相应评论信息是不行的，需要先访问一次主页`https://xueqiu.com/`，此时返回将携带一临时使用的`cookies`，此时再携带该`cookies`进行爬取数据
