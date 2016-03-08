# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests


class GamescraperPipeline(object):
    def process_item(self, item, spider):
        r = requests.post('http://localhost:1337/review',
                          json={"title": item['title'], 'rating': item['rating'], 'genre': item['genre'],
                                'url': item['review_url'], 'platforms': item['platforms']})
        print(r)
        return item
