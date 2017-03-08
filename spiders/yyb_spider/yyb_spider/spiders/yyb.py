# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

import logging
import traceback
import json

class YybSpider(scrapy.Spider):
    name = "yyb"
    allowed_domains = ["qq.com"]

    def __init__(self, *args, **kwargs):
        super(YybSpider, self).__init__(*args, **kwargs)
        self.starts = [
            'http://sj.qq.com/myapp/category.htm?orgame=1',
            'http://sj.qq.com/myapp/category.htm?orgame=2',
        ]

    def start_requests(self):
        items = []
        try:
            for url in self.starts:
                items.append(Request(url=url, callback=self.parse_main))
        except Exception as e:
            logging.log(logging.ERROR, traceback.format_exc())

        return items

    def parse_main(self, response):
        items = []
        try:
            logging.log(logging.INFO, "parse url: %s"%response.request.url)
            tags = response.xpath('//div[@class="nav-menu"]//ul[@class="menu"]//li[starts-with(@id, "cate-")]')
            for tag in tags:
                applist = []
                type = tag.xpath('./a/text()').extract()[0]
                sub_url = "http://sj.qq.com/myapp/cate/appList.htm" + tag.xpath('./a/@href').extract()[0] + "&pageSize=20&pageContext=%s"
                items.append(Request(url=sub_url%(0), callback=self.parse_typepage, meta={'type':type, 'more_url':sub_url, 'total':0}))
                logging.log(logging.INFO, "type is: %s, sub_url is : %s"%(type, sub_url))

        except Exception as e:
            logging.log(logging.ERROR, traceback.format_exc())

        return items

    def parse_typepage(self, response):
        logging.log(logging.INFO, "parse sub-url: %s"%response.request.url)
        items = []
        data = json.loads(response.body)
        try:
            appinfo_list = data['obj']
            for appinfo in appinfo_list:
                info = {}
                appname = appinfo['appName']
                info['appname'] = appname
                info['type'] = response.request.meta['type']
                items.append(info)
                logging.log(logging.INFO, "appname is: %s, type is %s"%(appname, response.request.meta['type']))

            total = response.request.meta['total'] + len(items)
            if data['count'] != 0:
                items.append(Request(url=response.request.meta['more_url']%(total), callback=self.parse_typepage, meta={'type':response.request.meta['type'], 'more_url':response.request.meta['more_url'], 'total':total}))

        except Exception as e:
            logging.log(logging.ERROR, traceback.format_exc())

        return items



