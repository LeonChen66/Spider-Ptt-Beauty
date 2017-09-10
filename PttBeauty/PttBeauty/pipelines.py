# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, os.path
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class PttbeautyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item': item})

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0[push]}/{1}'.format(item, image_guid)
        return filename

