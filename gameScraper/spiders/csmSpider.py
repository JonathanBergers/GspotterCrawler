# -*- coding: utf-8 -*-
import scrapy


class CsmspiderSpider(scrapy.Spider):
    name = "csmSpider"
    DOMAIN_NAME = 'https://www.commonsensemedia.org'
    start_urls = (
        'https://www.commonsensemedia.org/game-reviews',
    )

    def parse(self, response):
        print(response)
        last_page = response.css('.pager-last').xpath('.//a/@href').extract()[0].split('=')[1]

        print(last_page)

        for i in range(0, int(last_page)):
            yield scrapy.Request('https://www.commonsensemedia.org/game-reviews?page=' + str(i),
                                 self.parse_reviews)

    def parse_reviews(self, response):
        reviews_xpath = response.xpath('//*[@id="content"]/div/div/div[2]/div/div[4]/div/div/div[1]/div')
        for i in reviews_xpath:

            review = {}
            xpath_title = i.xpath('.//div[3]/div[2]/strong/a')
            xpath_rating = i.xpath('.//div[4]/div[2]/span/div')
            xpath_platform = i.xpath('.//div[6]/div[1]/em[2]/text()')

            review['review_url'] = self.DOMAIN_NAME + xpath_title.xpath('.//@href').extract()[0]
            review['title'] = xpath_title.xpath('.//text()')[0].extract()

            # get platforms
            platforms = []
            review['platforms'] = platforms
            for i in xpath_platform.extract()[0].split(','):
                platforms.append(i.strip())

            # get rating
            review_classes = xpath_rating.xpath('.//@class').extract()[0].split(' ')
            for j in review_classes:
                if j.startswith('rating-'):
                    review['rating'] = j.strip()[7:]
                    break
            # print(review)
            req = scrapy.Request(url=review['review_url'], callback=self.parse_review)
            req.meta['review'] = review
            yield req

        return

    def parse_review(self, response):
        review = response.meta['review']
        genre = response.css('.product-subtitle').xpath('div/ul/li[@class="last"]/a/text()').extract()[0]
        review['genre'] = genre
        return review
