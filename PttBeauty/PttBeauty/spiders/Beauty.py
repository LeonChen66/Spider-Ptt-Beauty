# -*- coding: utf-8 -*-
#encoding=utf-8
import scrapy
import logging
from PttBeauty.items import PttbeautyItem

def is_image(link):
    if(link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1):
       return True
    return False

class Beauty_Spider(scrapy.Spider):
    name = 'beauty_spider'
    _pages = 0
    Max_pages = 2
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Beauty/index.html']

    def parse(self,response):
        self._pages += 1
        for i, j in enumerate(response.css('div.r-ent div.title a').extract()):
            if '[正妹]' in j:
                url = response.urljoin(response.css('div.r-ent div.title a::attr(href)').extract()[i])
                print(url)
                yield scrapy.Request(url, callback=self.parse_post)

            if self._pages < self.Max_pages:
                next_page = response.xpath('//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                print(next_page[0].extract())
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('no next page')
            else:
                logging.warning('max page reached')

    def parse_post(self, response):
        item = PttbeautyItem()
        try:
            item['title'] = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
            total_score = 0
            for comment in response.css('div.push'):
                push_tag = comment.css('span.push-tag::text')[0].extract()
                if '推' in push_tag:
                    score = 1
                elif '噓' in push_tag:
                    score = -1
                else:
                    score = 0

                total_score += score

            if total_score > 99:
                total_score = 99

            item['push'] = total_score

            imgurls = []
            for img in response.xpath('//a/@href'):
                url = img.extract()
                if (is_image(url)):
                    imgurls.append(url)
            item['image_urls'] = imgurls

            yield item

        except:
            pass