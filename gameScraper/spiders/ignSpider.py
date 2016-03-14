# -*- coding: utf-8 -*-
import scrapy


class IgnspiderSpider(scrapy.Spider):
    name = "ignSpider"
    DOMAIN_NAME = 'http://www.ign.com'
    start_urls = (
        'http://www.ign.com/games/reviews/',
    )

    def parse(self, response):
        print("################################## begin parsing IGN game reviews ##################################")
        print(response)
        return scrapy.Request('http://www.ign.com/games/reviews', self.parse_reviews)

    def parse_reviews(self, response):
        print(response)

        nextpage_url = response.xpath('//*[@id="is-more-reviews"]/@data-start').extract()
        if len(nextpage_url) == 0:
            print("########################################## DONE ####################################################")
            return

        reviews_xpath = response.xpath('//*[@id="item-list"]/div[2]/div')
        for i in reviews_xpath:

            review = {}
            review['title'] = i.xpath('.//div[2]/div[1]/h3/a/text()').extract()[0].strip()
            review['rating'] = i.xpath('.//div[4]/div/a/span[1]/text()').extract()[0]
            review['genre'] = i.xpath('.//div[2]/p/span/text()').extract()[0].strip().split(',')
            review['platforms'] = i.xpath('.//div[2]/div[1]/h3/span/text()').extract()[0]
            review['review_url'] = self.DOMAIN_NAME + i.xpath('.//div[2]/div[1]/h3/a/@href').extract()[0]

            # print(review)
            yield review

        nextpage_url = 'http://www.ign.com/games/reviews?startIndex=' + nextpage_url[0]
        yield scrapy.Request(nextpage_url, self.parse_reviews)
