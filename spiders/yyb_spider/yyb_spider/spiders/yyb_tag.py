# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

import logging
import traceback
import json

class YybTagSpider(scrapy.Spider):
    name = "yyb_tag"
    allowed_domains = ["qq.com"]

    def __init__(self, *args, **kwargs):
        super(YybTagSpider, self).__init__(*args, **kwargs)
        self.starts = [
            'http://m5.qq.com/app/getappcategoryop.htm?categoryId=-9999',
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
        data = json.loads(response.body)
        try:
            type_list = data['obj']['appCategoryList']
            for info in type_list:
                type = info['categoryName']
                taglist = info['subCats']
                for taginfo in taglist:
                    cid = taginfo['subCatId']
                    tag = taginfo['subCatName']
                    base_url = 'http://m5.qq.com/app/applist.htm?listType=23&categoryType=2&categoryId=%s&pageSize=52&contextData=%s'%(cid, '')
                    items.append(Request(url=base_url, callback=self.parse_app, meta={'base_url':base_url, 'type':type, 'tag':tag}))
                
                    logging.log(logging.INFO, "type is: %s, tags is : %s"%(type, tag))

        except Exception as e:
            logging.log(logging.ERROR, traceback.format_exc())

        return items

    def parse_app(self, response):
        items = []
        type = response.request.meta['type']
        tag = response.request.meta['tag']
        data = json.loads(response.body)
        try:
            app_list = data['obj']['appList']
            for app in app_list:
                tags = [tag]
                appname = app['appName']
                tags.append(app['categoryName'])
                items.append({'appname':appname, 'type':type, 'tags':tags})
                logging.log(logging.INFO, "appname: %s - type is: %s - tags is : %s"%(appname, type, tags))

            if data['obj']['contextData'] != "":
                url = response.request.meta['base_url'] + data['obj']['contextData']
                items.append(Request(url=url, callback=self.parse_app, meta=response.request.meta))

        except Exception as e:
            logging.log(logging.ERROR, traceback.format_exc())

        return items
